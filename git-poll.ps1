# Git Poll Script - Pull every 10 seconds
# Run: powershell -ExecutionPolicy Bypass -File git-poll.ps1

$git = "C:\Program Files\Git\cmd\git.exe"
$repo = "C:\Users\vielc\OneDrive\Desktop\pene-lab-collab"

Write-Host "Git poller started - pulling every 10 seconds from $repo"
Write-Host "Press Ctrl+C to stop"

while ($true) {
    $result = & $git -C $repo pull --rebase 2>&1 | Out-String
    $ts = Get-Date -Format "HH:mm:ss"
    if ($result -notmatch "Already up to date") {
        Write-Host "[$ts] NEW CHANGES: $result" -ForegroundColor Green
    }
    Start-Sleep -Seconds 10
}
