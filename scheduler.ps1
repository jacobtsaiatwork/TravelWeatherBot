# Windows 工作排程器註冊腳本 (晨間通勤秘書 07:40)
# 執行方式：以 PowerShell 執行本腳本即可自動建立排程

$TaskName = "CommuteWeatherBrief"
$PythonExe = (Get-Command python).Source
$ScriptPath = Join-Path $PSScriptRoot "commute_brief.py"

Write-Host ">>> 準備註冊工作排程: $TaskName" -ForegroundColor Cyan
Write-Host "Python 直譯器: $PythonExe"
Write-Host "腳本路徑: $ScriptPath"

# 建立觸發條件：每週一至週五 07:40 AM
$Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday, Tuesday, Wednesday, Thursday, Friday -At 07:40AM

# 建立動作：執行 python commute_brief.py
$Action = New-ScheduledTaskAction -Execute $PythonExe -Argument "`"$ScriptPath`"" -WorkingDirectory $PSScriptRoot

# 註冊排程
Register-ScheduledTask -TaskName $TaskName -Trigger $Trigger -Action $Action -Description "每日晨間 07:40 通勤天氣與路況自動推播" -Force

Write-Host ">>> 成功註冊排程！可在 Windows 工作排程器中查看 '$TaskName'。" -ForegroundColor Green
