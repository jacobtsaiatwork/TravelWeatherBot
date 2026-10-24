# Windows 工作排程器腳本 (每日 07:40 AM 與 17:40 PM 自動推播，含平日與週末)
# 支援雙模式：
# 1. 若傳入 -RunDispatch，則檢查 GitHub Actions 最近 60 分鐘內是否已執行，若無則透過 API 自動觸發雲端推播
# 2. 若直接執行本腳本，則自動在 Windows 工作排程器註冊每日定時任務

param (
    [switch]$RunDispatch
)

if ($RunDispatch) {
    $cred = "protocol=https`nhost=github.com`n" | git credential fill
    $token = ($cred | Where-Object { $_ -match "^password=" }) -replace "^password=", ""
    if (-not $token) {
        Write-Error "未找到 GitHub Token，無法觸發雲端排程。"
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
        Write-Host "✅ 已透過 GitHub API 觸發今日通勤天氣推播！" -ForegroundColor Green
    } else {
        Write-Host "ℹ️ 最近 90 分鐘內已有推播紀錄，跳過重複觸發。" -ForegroundColor Yellow
    }
    exit 0
}

$TaskName = "CommuteWeatherBrief"
$ScriptPath = Join-Path $PSScriptRoot "scheduler.ps1"

Write-Host ">>> 準備註冊每日自動推播排程 (含週末): $TaskName" -ForegroundColor Cyan

# 建立觸發條件：每天早上 07:40 AM 與傍晚 17:40 PM (週一至週日每天執行)
$TriggerMorning = New-ScheduledTaskTrigger -Daily -At 07:40AM
$TriggerEvening = New-ScheduledTaskTrigger -Daily -At 05:40PM

# 建立動作：以 PowerShell 背景執行本腳本之 -RunDispatch 模式
$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$ScriptPath`" -RunDispatch" -WorkingDirectory $PSScriptRoot

# 設定若錯過時間 (例如電腦剛開機/休眠喚醒) 則自動補執行
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -TaskName $TaskName -Trigger @($TriggerMorning, $TriggerEvening) -Action $Action -Settings $Settings -Description "每日 (含週末) 07:40 與 17:40 通勤天氣與路況自動推播" -Force | Out-Null

Write-Host ">>> 成功註冊排程！每天 (週一至週日) 07:40 與 17:40 將自動推播。" -ForegroundColor Green
