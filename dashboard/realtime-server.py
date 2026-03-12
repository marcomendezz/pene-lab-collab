"""
Pene Lab Realtime Chat Server
WebSocket + HTTP server for instant messaging
All messages also saved to Git repo chat files
Run: python realtime-server.py
Access: http://localhost:4010
"""
import asyncio
import json
import http.server
import threading
import subprocess
import os
from datetime import datetime
from pathlib import Path

try:
    import websockets
    HAS_WS = True
except ImportError:
    HAS_WS = False

REPO = Path(__file__).parent.parent
BOT_CHAT = REPO / "shared-context" / "chat.md"
HUMAN_CHAT = REPO / "shared-context" / "human-chat.md"
GIT = r"C:\Program Files\Git\cmd\git.exe"
WS_PORT = 4011
HTTP_PORT = 4010

# Connected WebSocket clients
clients = set()
messages_bot = []
messages_human = []

def load_messages():
    global messages_bot, messages_human
    for f, store in [(BOT_CHAT, messages_bot), (HUMAN_CHAT, messages_human)]:
        store.clear()
        if f.exists():
            for line in f.read_text(encoding='utf-8').split('\n'):
                import re
                m = re.match(r'^\[(.+?)\]\s+(\w+):\s+(.+)$', line)
                if m:
                    store.append({'time': m.group(1), 'agent': m.group(2), 'text': m.group(3)})

def save_message(channel, name, text):
    f = HUMAN_CHAT if channel == 'human' else BOT_CHAT
    ts = datetime.now().strftime("%Y-%m-%d %H:%M CST")
    line = f"\n[{ts}] {name.upper()}: {text}\n"
    with open(f, 'a', encoding='utf-8') as fh:
        fh.write(line)
    # Git commit + push async
    try:
        subprocess.run([GIT, 'add', str(f)], cwd=str(REPO), capture_output=True, timeout=5)
        subprocess.run([GIT, 'commit', '-m', f'[{name}] {text[:40]}'], cwd=str(REPO), capture_output=True, timeout=5)
        subprocess.run([GIT, 'push'], cwd=str(REPO), capture_output=True, timeout=10)
    except:
        pass
    return {'time': ts, 'agent': name.upper(), 'text': text}

async def ws_handler(websocket):
    clients.add(websocket)
    try:
        # Send current state
        load_messages()
        await websocket.send(json.dumps({
            'type': 'init',
            'bot': messages_bot[-50:],
            'human': messages_human[-50:]
        }))
        async for raw in websocket:
            data = json.loads(raw)
            if data.get('type') == 'message':
                channel = data.get('channel', 'human')
                name = data.get('name', 'Anon')
                text = data.get('text', '')
                if text:
                    msg = save_message(channel, name, text)
                    # Broadcast to all clients
                    broadcast = json.dumps({'type': 'message', 'channel': channel, 'msg': msg})
                    await asyncio.gather(*[c.send(broadcast) for c in clients if c.open])
    except:
        pass
    finally:
        clients.discard(websocket)

# Git poll — pull every 3 seconds and broadcast changes
async def git_poller():
    last_bot = ""
    last_human = ""
    while True:
        try:
            subprocess.run([GIT, 'pull', '--rebase'], cwd=str(REPO), capture_output=True, timeout=10)
            bot_content = BOT_CHAT.read_text(encoding='utf-8') if BOT_CHAT.exists() else ""
            human_content = HUMAN_CHAT.read_text(encoding='utf-8') if HUMAN_CHAT.exists() else ""
            
            if bot_content != last_bot or human_content != last_human:
                last_bot = bot_content
                last_human = human_content
                load_messages()
                update = json.dumps({
                    'type': 'refresh',
                    'bot': messages_bot[-50:],
                    'human': messages_human[-50:]
                })
                if clients:
                    await asyncio.gather(*[c.send(update) for c in clients if c.open])
        except:
            pass
        await asyncio.sleep(3)

def get_dashboard_html():
    ws_url = "ws://localhost:4011"
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pene Lab — Live Dashboard</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI',sans-serif;background:#0d1117;color:#c9d1d9;height:100vh;display:flex;flex-direction:column}}
.header{{background:#161b22;border-bottom:1px solid #30363d;padding:12px 24px;display:flex;align-items:center;justify-content:space-between}}
.header h1{{font-size:20px;background:linear-gradient(90deg,#00d2ff,#7b2ff7);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.header .info{{font-size:12px;color:#8b949e;display:flex;align-items:center;gap:12px}}
.dot{{width:8px;height:8px;border-radius:50%;display:inline-block;margin-right:4px}}
.dot.on{{background:#3fb950;box-shadow:0 0 6px #3fb950}}
.dot.off{{background:#f85149}}
.name-sel{{background:#0d1117;border:1px solid #30363d;border-radius:6px;padding:4px 8px;color:#c9d1d9;font-size:12px}}

.main{{flex:1;display:grid;grid-template-columns:1fr 1fr;gap:0;overflow:hidden}}
.panel{{display:flex;flex-direction:column;border-right:1px solid #30363d;overflow:hidden}}
.panel:last-child{{border-right:none}}
.panel-header{{padding:10px 16px;background:#161b22;border-bottom:1px solid #30363d;font-weight:600;font-size:14px}}
.chat-area{{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:10px}}

.msg{{display:flex;gap:8px;animation:fadeIn .2s ease}}
@keyframes fadeIn{{from{{opacity:0;transform:translateY(4px)}}to{{opacity:1;transform:translateY(0)}}}}
.av{{width:36px;height:36px;border-radius:50%;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:bold;border:2px solid}}
.av.jarvis{{background:#1a2744;border-color:#00d2ff;color:#00d2ff}}
.av.hermes{{background:#2a1a44;border-color:#7b2ff7;color:#7b2ff7}}
.av.gonzalo{{background:#1a2a3a;border-color:#f0883e;color:#f0883e}}
.av.marco{{background:#1a3a2a;border-color:#7ee787;color:#7ee787}}
.av.system{{background:#2a2a2a;border-color:#8b949e;color:#8b949e}}
.bub{{flex:1;padding:8px 12px;border-radius:12px;border-top-left-radius:2px;background:#0d1117;border:1px solid #21262d}}
.bub.jarvis{{border-color:#00d2ff33;background:#0d1520}}
.bub.hermes{{border-color:#7b2ff733;background:#150d20}}
.bub.gonzalo{{border-color:#f0883e33;background:#1a150d}}
.bub.marco{{border-color:#7ee78733;background:#0d1a15}}
.bub .nm{{font-weight:700;font-size:12px;margin-bottom:2px}}
.bub.jarvis .nm{{color:#00d2ff}}
.bub.hermes .nm{{color:#7b2ff7}}
.bub.gonzalo .nm{{color:#f0883e}}
.bub.marco .nm{{color:#7ee787}}
.bub .tm{{color:#8b949e;font-size:10px;float:right}}
.bub .tx{{font-size:13px;line-height:1.5}}

.input-bar{{display:flex;padding:8px;border-top:1px solid #30363d;gap:6px}}
.input-bar input{{flex:1;background:#0d1117;border:1px solid #30363d;border-radius:6px;padding:8px 12px;color:#c9d1d9;font-size:13px;outline:none}}
.input-bar input:focus{{border-color:#00d2ff}}
.input-bar button{{background:linear-gradient(135deg,#00d2ff,#7b2ff7);color:white;border:none;border-radius:6px;padding:8px 14px;cursor:pointer;font-weight:600;font-size:13px}}

@media(max-width:768px){{.main{{grid-template-columns:1fr;grid-template-rows:1fr 1fr}}}}
</style>
</head>
<body>
<div class="header">
<h1>PENE LAB</h1>
<div class="info">
<span><span class="dot" id="ws-dot"></span><span id="ws-status">Connecting...</span></span>
<select class="name-sel" id="my-name">
<option value="Gonzalo">Gonzalo</option>
<option value="Marco">Marco</option>
</select>
</div>
</div>
<div class="main">
<div class="panel">
<div class="panel-header">🤖 Bot Chat</div>
<div class="chat-area" id="bot-chat"></div>
</div>
<div class="panel">
<div class="panel-header">💬 Human Chat</div>
<div class="chat-area" id="human-chat"></div>
<div class="input-bar">
<input type="text" id="msg-in" placeholder="Escribe un mensaje..." onkeydown="if(event.key==='Enter')send()">
<button onclick="send()">Send</button>
</div>
</div>
</div>
<script>
const AV={{jarvis:'J',hermes:'H',gonzalo:'G',marco:'M',system:'S'}};
const LB={{jarvis:'Jarvis',hermes:'Hermes',gonzalo:'Gonzalo',marco:'Marco',system:'System'}};
function cls(a){{const l=a.toLowerCase();return['jarvis','hermes','gonzalo','marco','system'].includes(l)?l:'human'}}
function esc(t){{const d=document.createElement('div');d.textContent=t;return d.innerHTML}}
function mkMsg(m){{const c=cls(m.agent);return`<div class="msg"><div class="av ${{c}}">${{AV[c]||m.agent[0]}}</div><div class="bub ${{c}}"><div class="nm">${{esc(LB[c]||m.agent)}} <span class="tm">${{esc(m.time)}}</span></div><div class="tx">${{esc(m.text)}}</div></div></div>`}}

function render(id,msgs){{const el=document.getElementById(id);const atBot=el.scrollTop+el.clientHeight>=el.scrollHeight-30;el.innerHTML=msgs.map(mkMsg).join('');if(atBot)el.scrollTop=el.scrollHeight}}

let ws;
function connect(){{
ws=new WebSocket('{ws_url}');
const dot=document.getElementById('ws-dot'),st=document.getElementById('ws-status');
ws.onopen=()=>{{dot.className='dot on';st.textContent='Live'}};
ws.onclose=()=>{{dot.className='dot off';st.textContent='Reconnecting...';setTimeout(connect,2000)}};
ws.onerror=()=>{{dot.className='dot off';st.textContent='Error'}};
ws.onmessage=(e)=>{{
const d=JSON.parse(e.data);
if(d.type==='init'||d.type==='refresh'){{render('bot-chat',d.bot);render('human-chat',d.human)}}
if(d.type==='message'){{
const el=document.getElementById(d.channel==='bot'?'bot-chat':'human-chat');
el.insertAdjacentHTML('beforeend',mkMsg(d.msg));
el.scrollTop=el.scrollHeight;
}}
}};
}}
connect();

function send(){{const i=document.getElementById('msg-in'),m=i.value.trim();if(!m||!ws||ws.readyState!==1)return;const name=document.getElementById('my-name').value;ws.send(JSON.stringify({{type:'message',channel:'human',name:name,text:m}}));i.value='';i.focus()}}
</script>
</body>
</html>'''

class HTTPHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            html = get_dashboard_html()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    def log_message(self, *args): pass

def run_http():
    server = http.server.HTTPServer(('0.0.0.0', HTTP_PORT), HTTPHandler)
    print(f"HTTP server on http://localhost:{HTTP_PORT}")
    server.serve_forever()

async def main():
    # Start HTTP in thread
    threading.Thread(target=run_http, daemon=True).start()
    
    if HAS_WS:
        print(f"WebSocket server on ws://localhost:{WS_PORT}")
        async with websockets.serve(ws_handler, '0.0.0.0', WS_PORT):
            await git_poller()
    else:
        print("websockets not installed. Run: pip install websockets")
        print("Falling back to HTTP-only mode")
        while True:
            await asyncio.sleep(3600)

if __name__ == '__main__':
    print("Pene Lab Realtime Server starting...")
    asyncio.run(main())
