# Windows Task Scheduler Script (Daily 07:40 AM & 17:40 PM, Monday-Sunday)
param (
    [switch]$RunDispatch
)

if ($RunDispatch) {
    $cred = "protocol=https`nhost=github.com`n" | git credential fill
    $token = ($cred | Where-Object { $_ -match "^password=" }) -replace "^password=", ""
    if (-not $token) {
        Write-Error "GitHub Token not found."
        exit 1
    }
    $headers = @{
        "Authorization" = "Bearer $token"
        "User-Agent"    = "PowerShell-CommuteWeatherBrief"
        "Accept"        = "application/vnd.github+json"
    }
    $runsResp = Invoke-RestMethod -Uri "https://api.github.com/repos/jacobtsaiatwork/TravelWeatherBot/actions/runs?per_page=3" -Headers $headers
    $nowUtc = (Get-Date).ToUniversalTime()
    $recentRun = $false
    foreach ($run in $runsResp.workflow_runs) {
        $createdTime = [DateTime]::Parse($run.created_at).ToUniversalTime()
        if (($nowUtc - $createdTime).TotalMinutes -lt 90 -and $run.conclusion -ne "failure") {
            $recentRun = $true
            break
        }
    }
    if (-not $recentRun) {
        Invoke-RestMethod -Method Post -Uri "https://api.github.com/repos/jacobtsaiatwork/TravelWeatherBot/actions/workflows/daily_brief.yml/dispatches" -Headers $headers -Body (@{ ref = "main" } | ConvertTo-Json) -ContentType "application/json"
        Write-Host "[OK] Triggered daily brief via GitHub Actions API." -ForegroundColor Green
    } else {
        Write-Host "[SKIP] A successful run already occurred within the last 90 minutes." -ForegroundColor Yellow
    }
    exit 0
}

$TaskName = "CommuteWeatherBrief"
$ScriptPath = Join-Path $PSScriptRoot "scheduler.ps1"

Write-Host ">>> Registering daily scheduled task (Mon-Sun): $TaskName" -ForegroundColor Cyan

$TriggerMorning = New-ScheduledTaskTrigger -Daily -At 07:40AM
$TriggerEvening = New-ScheduledTaskTrigger -Daily -At 05:40PM

$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$ScriptPath`" -RunDispatch" -WorkingDirectory $PSScriptRoot

$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -TaskName $TaskName -Trigger @($TriggerMorning, $TriggerEvening) -Action $Action -Settings $Settings -Description "Daily 07:40 and 17:40 Commute Weather Brief (including weekends)" -Force | Out-Null

Write-Host ">>> Successfully registered '$TaskName' (Daily at 07:40 AM and 17:40 PM, including weekends)." -ForegroundColor Green
