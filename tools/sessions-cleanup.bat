@echo off
chcp 65001 >nul
title OpenClaw Session Cleanup
echo ========================================
echo    OpenClaw Session Cleanup Tool
echo ========================================
echo.
node "%USERPROFILE%\.openclaw\workspace\tools\sessions-cleanup.js"
echo.
echo ========================================
if %ERRORLEVEL% EQU 0 (
    echo ✅ Cleanup completed successfully.
) else (
    echo ❌ Cleanup failed with error code %ERRORLEVEL%.
)
echo.
pause
