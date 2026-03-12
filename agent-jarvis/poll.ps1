$git = "C:\Program Files\Git\bin\git.exe"
$repoDir = "C:\Users\vielc\OneDrive\Desktop\pene-lab-collab"
$chatFile = "$repoDir\shared-context\chat.md"
$lastLineCount = 0

function Git-Run($args_str) {
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $git
    $psi.Arguments = $args_str
    $psi.UseShellExecute = $false
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.WorkingDirectory = $repoDir
    $p = [System.Diagnostics.Process]::Start($psi)
    $out = $p.StandardOutput.ReadToEnd()
    $err = $p.StandardError.ReadToEnd()
    $p.WaitForExit()
    return "$out$err"
}

# Get initial line count
if (Test-Path $chatFile) {
    $lastLineCount = (Get-Content $chatFile -Encoding UTF8).Count
}

Write-Output "$(Get-Date -Format 'HH:mm:ss') Polling started. Last lines: $lastLineCount"

while ($true) {
    try {
        # Pull latest
        $pullResult = Git-Run "pull --rebase origin main"
        
        if (Test-Path $chatFile) {
            $lines = Get-Content $chatFile -Encoding UTF8
            $currentCount = $lines.Count
            
            if ($currentCount -gt $lastLineCount) {
                # New lines detected
                $newLines = $lines[$lastLineCount..($currentCount-1)]
                $lastLineCount = $currentCount
                
                foreach ($line in $newLines) {
                    # Check if it's a message (not from Jarvis)
                    if ($line -match '^\[.+?\]\s+(\w+):\s+(.+)$') {
                        $agent = $matches[1]
                        $msg = $matches[2]
                        
                        if ($agent -ne "JARVIS") {
                            Write-Output "$(Get-Date -Format 'HH:mm:ss') NEW from $agent : $msg"
                            # Output for the parent process to pick up
                            Write-Output "NEW_MSG|$agent|$msg"
                        }
                    }
                }
            }
        }
    } catch {
        Write-Output "$(Get-Date -Format 'HH:mm:ss') Error: $_"
    }
    
    Start-Sleep -Seconds 10
}
