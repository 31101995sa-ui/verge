@echo off
setlocal EnableExtensions DisableDelayedExpansion
title VERGE - Local Scientific Mission Control

rem Start from the location of this launcher, not the Explorer working directory.
pushd "%~dp0" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Cannot open the folder containing Start_VERGE.cmd.
    goto :fail_without_folder
)

set "VERGE_ROOT=%CD%"
set "VERGE_PYTHON=%VERGE_ROOT%\.venv\Scripts\python.exe"
set "VERGE_PORT=8527"

echo ===========================================================
echo   VERGE - Verified Evidence and Risk-Governed Exploration
echo   Local launcher - scientific dashboard and Gemini demo
echo ===========================================================
echo.

if not exist "%VERGE_PYTHON%" (
    echo [ERROR] The prepared Python environment was not found:
    echo   "%VERGE_PYTHON%"
    echo Create or restore the project's .venv before using this launcher.
    goto :fail
)
if not exist "%VERGE_ROOT%\app.py" (
    echo [ERROR] app.py was not found beside Start_VERGE.cmd.
    goto :fail
)
if not exist "%VERGE_ROOT%\src\gemini_panel.py" (
    echo [ERROR] src\gemini_panel.py was not found.
    goto :fail
)
if not exist "%VERGE_ROOT%\data\releases\FLEX-R1-SAMPLE-20261114-v1.0\FLEX_R1_D7_manifest_v1.json" (
    echo [ERROR] FLEX D7 release manifest is missing.
    goto :fail
)
if not exist "%VERGE_ROOT%\data\releases\BASSII-R5-TABLE2_1-20261114-v1.0\BASS_II_R5_D7_manifest_v1.json" (
    echo [ERROR] BASS-II D7 release manifest is missing.
    goto :fail
)

rem Check only existing packages. Never install or upgrade anything silently.
"%VERGE_PYTHON%" -c "import streamlit, pandas, plotly" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Streamlit, pandas or Plotly is unavailable in .venv.
    echo Review the project's requirements and installation instructions.
    goto :fail
)
"%VERGE_PYTHON%" -c "import google.genai" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Gemini SDK is unavailable in .venv.
    echo The deterministic FLEX and BASS-II tools can still be used.
    echo Gemini interpretation will need the optional dependencies.
)

rem Do not start another server or terminate an unknown process on this port.
"%VERGE_PYTHON%" -c "import os,socket,sys; p=int(os.environ['VERGE_PORT']); s=socket.socket(); s.settimeout(0.75); busy=(s.connect_ex(('127.0.0.1',p))==0); s.close(); sys.exit(1 if busy else 0)" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Port %VERGE_PORT% is already in use on 127.0.0.1.
    echo Close your existing local server if it is yours, then retry.
    echo No process has been terminated by this launcher.
    goto :fail
)

rem This environment variable exists only in this launcher and its child process.
set "VERGE_ENABLE_GEMINI_LOCAL=1"

echo [INFO] Starting on http://127.0.0.1:%VERGE_PORT%
echo [INFO] The default browser should open automatically once Streamlit starts.
echo [INFO] Keep this window open while you use VERGE.
echo [INFO] Press Ctrl+C here to stop this server.
echo [INFO] Gemini requires your own API key and Internet access.
echo.

rem The server runs directly in this console. Never use START or detach it.
"%VERGE_PYTHON%" -m streamlit run app.py --server.address=127.0.0.1 --server.port=%VERGE_PORT% --server.headless=false --server.showEmailPrompt=false --browser.serverAddress=127.0.0.1
set "VERGE_EXIT=%ERRORLEVEL%"
echo.
echo [INFO] Streamlit ended with exit code %VERGE_EXIT%.
echo [INFO] If the browser stays open, its page will no longer be served.
popd
pause
endlocal & exit /b %VERGE_EXIT%

:fail
echo.
echo [INFO] No new VERGE server has been launched.
popd
endlocal
pause
exit /b 1

:fail_without_folder
echo.
endlocal
pause
exit /b 1
