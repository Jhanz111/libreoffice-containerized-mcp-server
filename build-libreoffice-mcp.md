@echo off
REM LibreOffice MCP Server v2.5.2 Build Script - Windows

echo Building LibreOffice MCP Server v2.5.2...
echo Platform: Windows
echo.

podman build ^
  --file Containerfile.libreoffice-mcp-v2.5.2 ^
  --tag localhost/libreoffice-mcp-server:v2.5.2-template-system ^
  --build-arg BUILD_DATE="%date% %time%" ^
  --build-arg VERSION="v2.5.2-template-system" ^
  --progress=plain .

if %ERRORLEVEL% neq 0 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo ✅ Build completed successfully!
echo Image: localhost/libreoffice-mcp-server:v2.5.2-template-system
pause
