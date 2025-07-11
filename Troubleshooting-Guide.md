# LibreOffice MCP Server - Troubleshooting Guide

## 🔧 Common Issues and Solutions

This guide helps resolve the most frequently encountered issues with the LibreOffice MCP Server.

## 🚀 Installation Issues

### Container Build Failures

**Problem**: Build script fails with "image not found" error

```
Error: No such image: localhost/libreoffice-mcp-server:v2.5.2-template-system
```

**Solutions:**

1. **Verify Container Runtime**:
    
    ```bash
    # Check if Podman/Docker is running
    podman version
    # or
    docker version
    ```
    
2. **Rebuild Container**:
    
    ```bash
    cd "Image Build Files"
    ./build-libreoffice-mcp-v2.5.2.sh
    ```
    
3. **Check Build Logs**:
    
    ```bash
    # Run build with verbose output
    podman build --progress=plain -f Containerfile -t localhost/libreoffice-mcp-server:v2.5.2-template-system .
    ```
    

### Permission Denied Errors

**Problem**: Container cannot access document directory

```
Error: Permission denied accessing /home/libreoffice/documents
```

**Solutions:**

1. **Set Directory Permissions**:
    
    ```bash
    # Linux/macOS
    chmod 755 "LibreOffice MCP Documents"
    chown -R $(id -u):$(id -g) "LibreOffice MCP Documents"
    
    # Windows (PowerShell as Administrator)
    icacls "LibreOffice MCP Documents" /grant Everyone:F
    ```
    
2. **Verify Volume Mount**:
    
    ```json
    {
      "mcpServers": {
        "libreoffice-mcp": {
          "args": [
            "-v", "/absolute/path/to/documents:/home/libreoffice/documents"
          ]
        }
      }
    }
    ```
    
3. **SELinux Issues (Linux)**:
    
    ```bash
    # Add SELinux context if needed
    setsebool -P container_manage_cgroup true
    chcon -Rt svirt_sandbox_file_t "LibreOffice MCP Documents"
    ```
    

## 🖥️ Windows Performance Issues

### GPU Acceleration and Skia Rendering Problems

**Problem**: Severe performance degradation on Windows systems - slow document operations, window lag, unresponsive LibreOffice container

**Symptoms:**

- Document operations taking 3-5x longer than expected benchmarks
- Window dragging and interface interactions are sluggish
- Container appears to hang during document processing
- High CPU usage with low actual throughput

**Root Cause**: Windows LibreOffice Skia rendering conflicts with container virtualization

**Solutions:**

1. **Disable Skia Rendering (Recommended)**:
    
    **In LibreOffice (if accessible):**
    
    - Tools → Options → LibreOffice → View
    - **Uncheck**: "Use Skia for all rendering"
    - **Uncheck**: "Force Skia software rendering"
    - Restart LibreOffice/container
    
    **Via Container Configuration:**
    
    ```json
    "args": [
      "run", "--rm", "-i", "-a", "stdin", "-a", "stdout",
      "-e", "SAL_DISABLE_SKIA=1",
      "-v", "path:/home/libreoffice/Documents",
      "localhost/libreoffice-mcp-server:v2.5.2-template-system"
    ]
    ```
    
2. **Alternative: Force Software Rendering**:
    
    ```json
    "args": [
      "run", "--rm", "-i", "-a", "stdin", "-a", "stdout", 
      "-e", "SAL_USE_VCLPLUGIN=gen",
      "-e", "SAL_DISABLE_SKIA=1",
      "-v", "path:/home/libreoffice/Documents",
      "localhost/libreoffice-mcp-server:v2.5.2-template-system"
    ]
    ```
    
3. **Container GPU Access (Advanced)**:
    
    ```json
    "--device=/dev/dxg",  // Windows WSL2 GPU access
    "--gpus=all"         // If using Docker with GPU support
    ```
    

**Performance Verification:**

After applying the fix, you should see:

- Document operations return to expected benchmarks (2-7 seconds)
- Smooth window interactions and responsive interface
- Normal CPU usage patterns during document processing

**Common Settings That Reset:**

Windows updates and LibreOffice updates may re-enable Skia rendering:

- Check after Windows updates
- Verify after LibreOffice container rebuilds
- Monitor performance if operations suddenly slow down

**Quick Test:**

```bash
# Test document creation speed after fix
time echo '{"tool": "create_writer_document", "args": {"filename": "performance_test", "content": "Testing performance after Skia fix"}}' | podman run --rm -i localhost/libreoffice-mcp-server:v2.5.2-template-system
```

Expected result: Operation should complete in 2-5 seconds, not 10-15+ seconds.

**Note**: This issue is Windows-specific due to container graphics virtualization conflicts. Linux and macOS systems typically don't experience this Skia rendering problem.

## 🖥️ Claude Desktop Configuration

### MCP Server Not Appearing

**Problem**: LibreOffice tools don't appear in Claude Desktop

**Diagnostic Steps:**

1. **Verify Config File Location**:
    
    - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
    - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
    - Linux: `~/.config/Claude/claude_desktop_config.json`
2. **Check JSON Syntax**:
    
    ```bash
    # Validate JSON syntax
    python -m json.tool claude_desktop_config.json
    ```
    
3. **Verify Container Access**:
    
    ```bash
    # Test container manually
    podman run --rm -i localhost/libreoffice-mcp-server:v2.5.2-template-system
    ```
    

**Solutions:**

1. **Complete Config Example**:
    
    ```json
    {
      "mcpServers": {
        "libreoffice-mcp": {
          "command": "podman",
          "args": [
            "run", "--rm", "-i", "-a", "stdin", "-a", "stdout",
            "-v", "/path/to/documents:/home/libreoffice/documents",
            "localhost/libreoffice-mcp-server:v2.5.2-template-system"
          ]
        }
      }
    }
    ```
    
2. **Restart Sequence**:
    
    ```bash
    # 1. Close Claude Desktop completely
    # 2. Wait 10 seconds
    # 3. Restart Claude Desktop
    # 4. Verify tools appear in new conversation
    ```
    

### Connection Timeouts

**Problem**: Tool calls timeout or hang indefinitely

**Solutions:**

1. **Increase Timeout**:
    
    ```json
    "args": [
      "run", "--rm", "-i", "-a", "stdin", "-a", "stdout",
      "--timeout=60",
      "-v", "path:/home/libreoffice/documents",
      "localhost/libreoffice-mcp-server:v2.5.2-template-system"
    ]
    ```
    
2. **Check System Resources**:
    
    ```bash
    # Monitor during operation
    htop
    # or
    docker stats
    ```
    
3. **Container Restart**:
    
    ```bash
    # Stop all containers
    podman stop $(podman ps -q)
    # Restart Claude Desktop
    ```
    

## ⚡ Performance Issues

### Slow Document Processing

**Problem**: Operations take longer than expected benchmarks

**Diagnostic:**

```bash
# Check container resource usage
podman stats

# Monitor system resources
top
# or
htop
```

**Solutions:**

1. **Increase Container Memory**:
    
    ```json
    "args": [
      "run", "--rm", "-i", "-a", "stdin", "-a", "stdout",
      "--memory=2g",
      "--memory-swap=4g",
      "-v", "path:/home/libreoffice/documents",
      "image"
    ]
    ```
    
2. **Optimize Document Directory**:
    
    - Use SSD storage for documents
    - Keep document directory clean
    - Limit directory size to <1000 files
3. **System Optimization**:
    
    - Close unnecessary applications
    - Ensure 4GB+ free RAM
    - Use SSD storage for best performance
    - Disable real-time antivirus scanning on document directory

### Memory Issues

**Problem**: Container runs out of memory with large documents

**Solutions:**

1. **Increase Memory Limits**:
    
    ```json
    "--memory=4g",
    "--memory-swap=8g"
    ```
    
2. **Process Documents in Chunks**:
    
    ```
    Instead of: "Process this 500-page document"
    Use: "Split this document by chapters, then process each section"
    ```
    
3. **Monitor Memory Usage**:
    
    ```bash
    # Watch memory consumption
    watch -n 1 'podman stats --no-stream'
    ```
    

## 📄 Document-Specific Issues

### File Format Problems

**Problem**: "Unsupported format" or conversion errors

**Supported Formats:**

- **Input**: .odt, .ods, .odp, .doc, .docx, .xls, .xlsx, .ppt, .pptx
- **Output**: .pdf, .odt, .ods, .docx, .xlsx, .html, .txt

**Solutions:**

1. **Convert Format First**:
    
    ```
    Convert the document to ODT format, then perform the operation
    ```
    
2. **Check File Integrity**:
    
    ```bash
    # Verify file is not corrupted
    file "document.odt"
    ```
    
3. **Manual Conversion**:
    
    - Open in LibreOffice Desktop
    - Save As → target format
    - Retry operation

### Template System Issues

**Problem**: Template creation or application fails

**Common Causes:**

1. **Placeholder Format Mismatch**:
    
    ```
    Template uses: {{name}}
    Application specifies: %name%
    Solution: Match placeholder formats
    ```
    
2. **Missing Placeholders**:
    
    ```
    Error: Placeholder 'company' not found in template
    Solution: Verify placeholder names exactly match
    ```
    
3. **Encoding Issues**:
    
    ```
    Solution: Ensure UTF-8 encoding for all documents
    ```
    

**Debug Steps:**

1. **List Template Details**:
    
    ```
    Show me the details of my template including all placeholders
    ```
    
2. **Test with Simple Template**:
    
    ```
    Create a simple template with just one placeholder for testing
    ```
    
3. **Verify Placeholder Syntax**:
    
    - Mustache: `{{placeholder}}`
    - Percent: `%placeholder%`
    - Dollar: `$placeholder$`

## 🔍 Debugging Tools

### Container Inspection

**View Container Logs**:

```bash
# Get container ID
podman ps

# View logs
podman logs <container_id>

# Follow logs in real-time
podman logs -f <container_id>
```

**Interactive Container Access**:

```bash
# Enter running container
podman exec -it <container_id> /bin/bash

# Check LibreOffice status
ps aux | grep soffice

# Test UNO connection
netstat -an | grep 2002
```

### System Diagnostics

**Check Dependencies**:

```bash
# Verify Python environment
python3 --version

# Check required packages
pip list | grep -E "(mcp|uno|libreoffice)"

# Verify LibreOffice installation
/opt/libreoffice/program/soffice --version
```

**Performance Monitoring**:

```bash
# Monitor resource usage
top -p $(pgrep -f libreoffice)

# Check disk space
df -h

# Network connectivity
netstat -tulpn | grep 2002
```

## 🛠️ Advanced Troubleshooting

### Clean Reinstall

**Complete System Reset**:

```bash
# 1. Stop all containers
podman stop $(podman ps -aq)

# 2. Remove containers
podman rm $(podman ps -aq)

# 3. Remove images
podman rmi localhost/libreoffice-mcp-server:v2.5.2-template-system

# 4. Clean build cache
podman system prune -a

# 5. Rebuild from scratch
cd "Image Build Files"
./build-libreoffice-mcp-v2.5.2.sh
```

**Reset Claude Desktop Config**:

```bash
# Backup current config
cp claude_desktop_config.json claude_desktop_config.json.backup

# Create minimal config
cat > claude_desktop_config.json << EOF
{
  "mcpServers": {}
}
EOF

# Restart Claude Desktop
# Add LibreOffice MCP config back
```

### Container Build Debugging

**Manual Build Process**:

```bash
# Build with maximum verbosity
podman build \
  --progress=plain \
  --no-cache \
  -f Containerfile \
  -t localhost/libreoffice-mcp-server:v2.5.2-template-system \
  .

# Test individual build steps
podman run --rm -it ubuntu:24.04 /bin/bash
```

**Build Environment Issues**:

```bash
# Check available space
df -h

# Verify network connectivity
curl -I https://download.libreoffice.org/

# Check proxy settings (if applicable)
env | grep -i proxy
```

## 📊 Performance Baselines

### Expected Performance Metrics

|Operation|Normal|Slow|Critical|
|---|---|---|---|
|Document Creation|2-5 seconds|>10 seconds|Check resources|
|Document Reading|1-3 seconds|>8 seconds|Optimize file size|
|Template Creation|3-7 seconds|>15 seconds|Check placeholders|
|Template Application|3-5 seconds|>12 seconds|Verify data|
|Style Transfer|5-10 seconds|>20 seconds|Limit style types|

### Resource Usage Baselines

|Resource|Normal|High|Critical|
|---|---|---|---|
|Memory|500MB-1GB|>2GB|>4GB|
|CPU|20-60%|>80%|>95%|
|Disk I/O|Low-Medium|High sustained|Very High|

## 📞 Getting Additional Help

### Information to Collect

When reporting issues, please provide:

1. **System Information**:
    
    ```bash
    uname -a # OS version
    podman version # Container runtime
    claude --version # Claude Desktop version
    ```
    
2. **Error Details**:
    
    - Complete error messages
    - Steps to reproduce
    - Expected vs actual behavior
    - Time when issue occurred
3. **Log Files**:
    
    ```bash
    # Container logs
    podman logs <container_id> > container.log
    
    # System logs (Linux)
    journalctl -u podman > system.log
    ```
    
4. **Configuration**:
    
    - Claude Desktop config (sanitized)
    - Container build logs
    - Document samples (if relevant)

### Support Channels

- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Check `/docs` directory for detailed guides
- **Community Discussions**: GitHub Discussions for community support
- **Performance Issues**: Include system specifications and benchmarks

---

**🔧 Most issues can be resolved by following this guide systematically. Start with the basic checks and work through to advanced debugging as needed.**