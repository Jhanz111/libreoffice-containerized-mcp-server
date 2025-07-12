@echo off
REM LibreOffice MCP Server v2.5.2 Run Script - Windows
REM Revolutionary Template System Edition

echo Starting LibreOffice MCP Server v2.5.2...
echo Platform: Windows
echo Container Runtime: podman
echo Documents Path: K:Code Dev WorkObsidian BM Vault 2Developmentibreoffice mcp serverimage build filesibreoffice-documents
echo.

podman run --rm -i ^
  -a stdin -a stdout ^
  -v "K:Code Dev WorkObsidian BM Vault 2Developmentibreoffice mcp serverimage build filesibreoffice-documents:/home/libreoffice/Documents" ^
  localhost/libreoffice-mcp-server:v2.5.2-template-system 2>logs\mcp-server-error.log

if %ERRORLEVEL% neq 0 (
    echo ERROR: Container failed to start
    echo Check logs\mcp-server-error.log for details
    pause
    exit /b 1
)
