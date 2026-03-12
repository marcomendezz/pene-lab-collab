# Visual Upgrade — Animation Snippets (Jarvis Research)
**Date:** 2026-03-11
**Status:** Ready for integration

## 1. Animated Gradient Mesh Background (Pure CSS)
Replace the flat `#0d1117` body background with a subtle animated gradient.

```css
body {
    background: #0d1117;
    position: relative;
    overflow: hidden;
}
body::before {
    content: '';
    position: fixed;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle at 20% 50%, rgba(88, 166, 255, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(216, 168, 255, 0.06) 0%, transparent 50%),
                radial-gradient(circle at 50% 80%, rgba(126, 231, 135, 0.05) 0%, transparent 50%);
    animation: meshMove 20s ease-in-out infinite alternate;
    z-index: 0;
    pointer-events: none;
}
@keyframes meshMove {
    0%   { transform: translate(0, 0) rotate(0deg); }
    33%  { transform: translate(-2%, 1%) rotate(1deg); }
    66%  { transform: translate(1%, -1%) rotate(-0.5deg); }
    100% { transform: translate(-1%, 2%) rotate(0.5deg); }
}
/* Make sure all content is above the background */
.header, .container { position: relative; z-index: 1; }
```

## 2. Glassmorphism Panels
Replace the current flat panels with frosted glass effect.

```css
.panel {
    background: rgba(22, 27, 34, 0.7);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(48, 54, 61, 0.6);
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.panel:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
    border-color: rgba(88, 166, 255, 0.2);
}
.header {
    background: rgba(22, 27, 34, 0.8);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
}
```

## 3. Chat Message Animations
Smooth entrance for new messages.

```css
@keyframes msgSlideIn {
    from {
        opacity: 0;
        transform: translateY(12px) scale(0.97);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}
.chat-msg {
    animation: msgSlideIn 0.35s cubic-bezier(0.16, 1, 0.3, 1);
    transition: background 0.2s ease;
}
.chat-msg:hover {
    background: rgba(13, 17, 23, 0.8);
}
```

## 4. Typing Indicator (3 bouncing dots)
Show when a bot or human is typing.

```css
.typing-indicator {
    display: flex;
    align-items: center;
    padding: 8px 12px;
    gap: 4px;
}
.typing-indicator .dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #8b949e;
    animation: typingBounce 1.4s infinite ease-in-out;
}
.typing-indicator .dot:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator .dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes typingBounce {
    0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
    30% { transform: translateY(-6px); opacity: 1; }
}
```

HTML for typing indicator:
```html
<div class="typing-indicator">
    <div class="dot"></div>
    <div class="dot"></div>
    <div class="dot"></div>
    <span style="margin-left:6px; color:#8b949e; font-size:12px;">Bot is thinking...</span>
</div>
```

## 5. Notification Toast (New Message Alert)
Pure CSS + JS toast that appears when new messages arrive.

```css
.toast {
    position: fixed;
    bottom: 24px;
    right: 24px;
    background: rgba(22, 27, 34, 0.95);
    backdrop-filter: blur(12px);
    border: 1px solid #30363d;
    border-left: 3px solid #58a6ff;
    border-radius: 8px;
    padding: 12px 20px;
    color: #c9d1d9;
    font-size: 13px;
    z-index: 200;
    transform: translateX(120%);
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    max-width: 320px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}
.toast.show { transform: translateX(0); }
.toast .toast-title { font-weight: 600; color: #58a6ff; font-size: 12px; margin-bottom: 4px; }
```

```javascript
function showToast(agent, message) {
    let toast = document.getElementById('toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'toast';
        toast.className = 'toast';
        document.body.appendChild(toast);
    }
    toast.innerHTML = `<div class="toast-title">${agent}</div>${message.substring(0, 80)}${message.length > 80 ? '...' : ''}`;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 4000);
}
```

## 6. Commit Feed Slide-In Animation

```css
@keyframes commitSlide {
    from { opacity: 0; transform: translateX(-20px); }
    to { opacity: 1; transform: translateX(0); }
}
.commit {
    animation: commitSlide 0.3s ease-out;
    animation-fill-mode: both;
}
.commit:nth-child(1) { animation-delay: 0s; }
.commit:nth-child(2) { animation-delay: 0.05s; }
.commit:nth-child(3) { animation-delay: 0.1s; }
.commit:nth-child(4) { animation-delay: 0.15s; }
.commit:nth-child(5) { animation-delay: 0.2s; }
```

## 7. Pulse Dot for Live Status

```css
.dot {
    position: relative;
}
.dot::after {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    border-radius: 50%;
    background: #3fb950;
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(2.5); opacity: 0; }
    100% { transform: scale(1); opacity: 0; }
}
```

## 8. Google Fonts (Inter + JetBrains Mono)
Add to `<head>`:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

```css
body { font-family: 'Inter', -apple-system, sans-serif; }
.sha, code, .chat-input input { font-family: 'JetBrains Mono', monospace; }
```

---

## Integration Priority
1. **Gradient mesh background** — biggest visual impact, easy to add
2. **Glassmorphism panels** — transforms the whole feel
3. **Message animations** — makes chat feel alive
4. **Google Fonts** — instant polish
5. **Toast notifications** — functional + cool
6. **Typing indicator** — nice to have
7. **Commit slide-in** — cherry on top
8. **Pulse dot** — subtle but premium

All snippets are pure CSS/JS, zero dependencies. Copy-paste ready.
