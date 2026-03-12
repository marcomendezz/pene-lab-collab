# Jarvis Watchdog — Monitors repo for new messages and alerts via Telegram
# Runs every 3 seconds, checks chat.md and human-chat.md for new content
# If new messages found from Hermes/Gonzalo/Marco, triggers OpenClaw notification

$git = "C:\Program Files\Git\cmd\git.exe"
$repo = "C:\Users\vielc\OneDrive\Desktop\pene-lab-collab"
$lastBotHash = ""
$lastHumanHash = ""
$chatFile = Join-Path $repo "shared-context\chat.md"
$humanFile = Join-Path $repo "shared-context\human-chat.md"
$tasksFile = Join-Path $repo "shared-context\tasks.md"

function Get-FileHash2($path) {
    if (Test-Path $path) { return (Get-FileHash $path -Algorithm MD5).Hash }
    return ""
}

Write-Host "Jarvis Watchdog started — monitoring every 3 seconds"

while ($true) {
    try {
        # Pull latest
        & $git -C $repo pull --rebase 2>&1 | Out-Null
        
        # Check bot chat
        $currentBotHash = Get-FileHash2 $chatFile
        if ($currentBotHash -ne $lastBotHash -and $lastBotHash -ne "") {
            $lastLine = (Get-Content $chatFile -Tail 3) -join " "
            if ($lastLine -match "HERMES:" -or $lastLine -match "GONZALO:" -or $lastLine -match "MARCO:") {
                # New message not from Jarvis — need to respond
                $alertFile = Join-Path $repo "agent-jarvis\pending-response.txt"
                $lastLine | Set-Content $alertFile
                Write-Host "[$(Get-Date -Format 'HH:mm:ss')] NEW BOT CHAT — needs response"
            }
        }
        $lastBotHash = $currentBotHash
        
        # Check human chat
        $currentHumanHash = Get-FileHash2 $humanFile
        if ($currentHumanHash -ne $lastHumanHash -and $lastHumanHash -ne "") {
            $lastLine = (Get-Content $humanFile -Tail 3) -join " "
            if ($lastLine -match "GONZALO:" -or $lastLine -match "MARCO:") {
                $alertFile = Join-Path $repo "agent-jarvis\pending-human.txt"
                $lastLine | Set-Content $alertFile
                Write-Host "[$(Get-Date -Format 'HH:mm:ss')] NEW HUMAN CHAT — needs response"
            }
        }
        $lastHumanHash = $currentHumanHash
        
        # Check tasks — any uncompleted?
        if (Test-Path $tasksFile) {
            $openTasks = (Get-Content $tasksFile | Where-Object { $_ -match "^\- \[ \] JARVIS:" }).Count
            if ($openTasks -gt 0) {
                Write-Host "[$(Get-Date -Format 'HH:mm:ss')] $openTasks open tasks assigned to Jarvis"
            }
        }
    } catch {
        # Silent retry
    }
    
    Start-Sleep -Seconds 3
}
