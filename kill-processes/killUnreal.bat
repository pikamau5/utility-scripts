@echo off
setlocal enabledelayedexpansion

rem Add process names (without .exe) to the list below, separated by a space
set "process_list=UnrealEditor"

for %%p in (%process_list%) do (
    echo Killing process: %%p.exe
    taskkill /IM %%p.exe /F /T >nul 2>&1
)

echo All specified processes have been killed.
