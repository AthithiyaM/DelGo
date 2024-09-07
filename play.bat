@echo off
setlocal

REM Get the directory of the current script
set "DIR=%~dp0"
set "PYTHON_SCRIPT_PATH=%DIR%code\human_v_bot.py"

REM Check if python3 is in the PATH
where python3 >nul 2>nul
if %errorlevel% equ 0 (
    echo python3 found, launching script
    python3 "%PYTHON_SCRIPT_PATH%"
    goto :end
)

REM Check if python is in the PATH
where python >nul 2>nul
if %errorlevel% equ 0 (
    echo python found, launching script
    python "%PYTHON_SCRIPT_PATH%"
    goto :end
)

REM If neither python3 nor python is found
echo ERROR: python cannot be found!

:end
pause
