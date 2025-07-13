
# LibreOffice MCP Server Installation Guide

## 🚀 Complete Setup Instructions

This guide walks you through installing and configuring the LibreOffice MCP Server v2.5.2 Revolutionary Template System from start to finish.

## 📋 Prerequisites

## 📋 System Requirements

### Operating System Requirements

Your system must meet the minimum requirements for your operating system **plus** additional resources for containerization and LibreOffice processing.

#### Windows Requirements

**Windows 11:**

- **CPU**: 1 GHz+ processor with 2+ cores (64-bit)
- **RAM**: 4 GB minimum
- **Storage**: 64 GB available space
- **Additional**: TPM 2.0, UEFI firmware, DirectX 12 compatible graphics

**Windows 10:**

- **CPU**: 1 GHz+ processor (32-bit or 64-bit)
- **RAM**: 2 GB (64-bit) or 1 GB (32-bit)
- **Storage**: 20 GB (64-bit) or 16 GB (32-bit) available space
- **Graphics**: DirectX 9 with WDDM 1.0 driver

#### macOS Requirements

**macOS Sonoma (14.0+) or Ventura (13.0+):**

- **RAM**: 8 GB minimum (16 GB recommended for optimal performance)
- **Storage**: 35 GB available space
- **Compatible Models**: Mac models from 2018+ (Intel) or Apple Silicon Macs

**macOS Monterey (12.0+):**

- **RAM**: 4 GB minimum (8 GB recommended)
- **Storage**: 35 GB available space
- **Compatible Models**: Mac models from 2015+ (final version supporting some older models)

#### Linux Requirements

**Ubuntu 20.04 LTS / 22.04 LTS / 24.04 LTS:**

- **CPU**: 2 GHz dual-core processor minimum
- **RAM**: 4 GB minimum (8 GB recommended)
- **Storage**: 25 GB available space
- **Graphics**: Graphics card with 1024×768 resolution

**Other Linux Distributions:**

- **RHEL/CentOS 8+**: Similar to Ubuntu requirements
- **Fedora 35+**: 2 GB RAM minimum, 4 GB recommended
- **Debian 11+**: 2 GB RAM minimum, 4 GB recommended

### LibreOffice MCP Server Additional Requirements

**Beyond OS minimums, add these requirements for our containerized system:**

#### Recommended Configuration

- **RAM**: +2 GB above OS minimum (for container operation)
- **Storage**: +3 GB available space (for container images and documents)
- **CPU**: Multi-core processor recommended for document processing performance

#### Minimum Viable Configuration

- **Total RAM**: 6 GB (OS + 2 GB for containers)
- **Total Storage**: 5 GB available space (2 GB container + 2 GB documents + 1 GB workspace)
- **CPU**: 2+ cores for reasonable performance

#### Optimal Performance Configuration

- **Total RAM**: 8 GB+ (smooth operation with large documents)
- **Total Storage**: 10 GB+ available space (multiple templates, document library)
- **CPU**: 4+ cores for fast document processing
- **Storage Type**: SSD recommended for best I/O performance

### Container Runtime Requirements

**Podman (Recommended) or Docker:**

- **Supported on**: Windows 10/11, macOS 10.15+, Linux (all major distributions)
- **Additional RAM**: 1-2 GB for container runtime
- **Virtualization**: Hardware virtualization support (Intel VT-x/AMD-V)

### Hardware Compatibility Notes

#### Performance Scaling

- **2-4 GB RAM**: Basic document operations (slower performance)
- **4-8 GB RAM**: Standard document workflows (good performance)
- **8+ GB RAM**: Complex documents and templates (optimal performance)

#### Storage Considerations

- **HDD**: Functional but slower document processing
- **SSD**: Recommended for responsive performance
- **Available Space**: 5 GB minimum, 10+ GB recommended for active use

#### Architecture Support

- **x64/AMD64**: Full support on all platforms
- **ARM64**: Supported on Apple Silicon Macs and ARM64 Linux
- **x86 (32-bit)**: Not supported (requires 64-bit OS)

### Virtual Machine Requirements

**If running in a VM, increase requirements:**

- **RAM**: +1 GB above recommendations
- **CPU**: Allocate 2+ cores to VM
- **Storage**: +2 GB for VM overhead
- **Virtualization**: Nested virtualization may be required for containers

### Required Software

#### 1. Container Runtime

**Choose ONE of the following:**

**Option A: Podman (Recommended)**

- **Windows**: Download from [podman.io](https://podman.io/getting-started/installation)
- **macOS**: `brew install podman` or download installer
- **Linux**: Use distribution package manager
    
    ```bash
    # Ubuntu/Debiansudo apt update && sudo apt install podman# RHEL/CentOS/Fedorasudo dnf install podman
    ```
    

**Option B: Docker**

- Download from [docker.com](https://www.docker.com/products/docker-desktop/)
- Follow platform-specific installation instructions

#### 2. Claude Desktop

- Download from [claude.ai](https://claude.ai/download)
- Install and complete initial setup
- Ensure you can open and use Claude Desktop

#### 3. Git (Optional but Recommended)

- **Windows**: [git-scm.com](https://git-scm.com/download/win)
- **macOS**: `brew install git` or Xcode Command Line Tools
- **Linux**: Usually pre-installed, or `sudo apt install git`

## 📥 Installation Steps

### Step 1: Download the Project

#### Option A: Download ZIP (Easiest)

1. Go to the [GitHub repository](https://github.com/Jhanz111/libreoffice-containerized-mcp-server)
2. Click the green **"<> Code"** button
3. Select **"Download ZIP"**
4. Extract the ZIP file to your desired location

#### Option B: Git Clone

```bash
git clone https://github.com/Jhanz111/libreoffice-containerized-mcp-server.git
cd libreoffice-containerized-mcp-server
```

### Step 2: Create Document Directory

Create a directory where LibreOffice will read and write documents:

**Windows (PowerShell):**

```powershell
# Navigate to project directory
cd "path\to\libreoffice-containerized-mcp-server"

# Create documents directory
New-Item -ItemType Directory -Name "LibreOffice MCP Documents" -Force
```

**macOS/Linux:**

```bash
# Navigate to project directory
cd /path/to/libreoffice-containerized-mcp-server

# Create documents directory
mkdir -p "LibreOffice MCP Documents"
```

### Step 3: Build the Container

#### Windows (PowerShell)

```powershell
# Navigate to Image Build Files
cd "Image Build Files"

# Build the container (single line for PowerShell 7.5 compatibility)
podman build --file Containerfile.libreoffice-mcp-v2.5.2 --tag libreoffice-mcp-server:v2.5.2-template-system --build-arg BUILD_DATE="$(Get-Date -Format 'yyyy-MM-ddTHH:mm:ssZ')" --build-arg VERSION="v2.5.2-template-system" --progress=plain .
```

#### macOS/Linux

```bash
# Navigate to Image Build Files
cd "Image Build Files"

# Make scripts executable
chmod +x *.sh

# Run the build script
./cross-platform-libreoffice-mcp-build.sh
```

**Expected Build Time:** 3-8 minutes depending on internet speed and system performance.

### Step 4: Test the Container

Verify the container was built successfully:

**Windows (PowerShell):**

```powershell
# List built images
podman images | findstr libreoffice-mcp-server

# Test run (should show server startup)
podman run --rm -it localhost/libreoffice-mcp-server:v2.5.2-template-system
```

**macOS/Linux:**

```bash
# List built images
podman images | grep libreoffice-mcp-server

# Test run (should show server startup)
podman run --rm -it localhost/libreoffice-mcp-server:v2.5.2-template-system
```

**Success Indicators:**

- Container starts without errors
- Shows "LibreOffice MCP Server v2.5.2" startup message
- No error messages about missing dependencies

### Step 5: Configure Claude Desktop

#### Locate Configuration File

**Windows:**

```
%APPDATA%\Claude\claude_desktop_config.json
```

**macOS:**

```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**

```
~/.config/Claude/claude_desktop_config.json
```

#### Update Configuration

**IMPORTANT:** Replace `/absolute/path/to/project` with your actual project directory path.

**Windows Configuration:**

```json
{
  "mcpServers": {
    "libreoffice-mcp": {
      "command": "podman",
      "args": [
        "run", "--rm", "-i", "-a", "stdin", "-a", "stdout",
        "-v", "C:\\absolute\\path\\to\\project\\LibreOffice MCP Documents:/home/libreoffice/Documents",
        "localhost/libreoffice-mcp-server:v2.5.2-template-system"
      ]
    }
  }
}
```

**macOS/Linux Configuration:**

```json
{
  "mcpServers": {
    "libreoffice-mcp": {
      "command": "podman",
      "args": [
        "run", "--rm", "-i", "-a", "stdin", "-a", "stdout",
        "-v", "/absolute/path/to/project/LibreOffice MCP Documents:/home/libreoffice/Documents",
        "localhost/libreoffice-mcp-server:v2.5.2-template-system"
      ]
    }
  }
}
```

#### Path Configuration Examples

**Windows Example:**

```json
"-v", "C:\\Users\\YourName\\Documents\\libreoffice-containerized-mcp-server\\LibreOffice MCP Documents:/home/libreoffice/Documents"
```

**macOS Example:**

```json
"-v", "/Users/YourName/Documents/libreoffice-containerized-mcp-server/LibreOffice MCP Documents:/home/libreoffice/Documents"
```

**Linux Example:**

```json
"-v", "/home/yourname/Documents/libreoffice-containerized-mcp-server/LibreOffice MCP Documents:/home/libreoffice/Documents"
```

### Step 6: Restart Claude Desktop

1. **Close Claude Desktop completely**
2. **Wait 10 seconds**
3. **Restart Claude Desktop**
4. **Open a new conversation**

## ✅ Verification

### Test Basic Functionality

In a new Claude Desktop conversation, try:

```
Create a test document with the text "Hello World from LibreOffice MCP Server!"
```

**Expected Result:**

- Document created successfully
- File appears in your "LibreOffice MCP Documents" directory
- No error messages

### Test Template System

```
Create a simple invoice template with placeholders for company_name and amount
```

**Expected Result:**

- Template created with {{company_name}} and {{amount}} placeholders
- Success message with template details

### Test Document Reading

```
Read the contents of the test document we just created
```

**Expected Result:**

- Document content displayed
- Metadata information shown

## 🛠️ Troubleshooting

### Container Build Issues

**Problem:** Build fails with "permission denied"

```bash
# Solution: Fix permissions
sudo chown -R $USER:$USER /path/to/project
```

**Problem:** "No space left on device"

```bash
# Solution: Clean up container cache
podman system prune -a
```

### Claude Desktop Issues

**Problem:** Tools don't appear in Claude Desktop

**Solutions:**

1. **Verify JSON syntax:**
    
    ```bash
    # Test JSON validity
    python -m json.tool claude_desktop_config.json
    ```
    
2. **Check path format:**
    
    - Use forward slashes on all platforms in JSON
    - Ensure absolute paths are correct
    - Verify document directory exists
3. **Restart sequence:**
    
    - Close Claude Desktop completely
    - Wait 10 seconds
    - Restart Claude Desktop

**Problem:** Connection timeout errors

**Solutions:**

1. **Increase container memory:**
    
    ```json
    "args": [
      "run", "--rm", "-i", "-a", "stdin", "-a", "stdout",
      "--memory=2g",
      "-v", "path:/home/libreoffice/Documents",
      "localhost/libreoffice-mcp-server:v2.5.2-template-system"
    ]
    ```
    
2. **Check system resources:**
    
    ```bash
    # Monitor resource usage
    htop
    # or
    top
    ```
    

### Performance Issues

**Windows GPU/Skia Rendering Fix:** If operations are slow, add environment variable:

```json
"args": [
  "run", "--rm", "-i", "-a", "stdin", "-a", "stdout",
  "-e", "SAL_DISABLE_SKIA=1",
  "-v", "path:/home/libreoffice/Documents",
  "localhost/libreoffice-mcp-server:v2.5.2-template-system"
]
```

## 🚀 Next Steps

### Explore the Tools

Try these commands to explore the full capability:

1. **List all available tools:**
    
    ```
    What LibreOffice tools are available?
    ```
    
2. **Create a business template:**
    
    ```
    Create a professional business letter template with placeholders for recipient, sender, and message content
    ```
    
3. **Document analysis:**
    
    ```
    Create a sample document and then analyze its structure
    ```
    

### Advanced Usage

- **Template Library:** Build a collection of reusable templates
- **Document Workflows:** Automate report generation and formatting
- **Style Management:** Create consistent document formatting across projects
- **Batch Processing:** Handle multiple documents efficiently

## 📚 Additional Resources

- **[API Documentation](API-Documentation.md):** Complete tool reference
- **[Troubleshooting Guide](Troubleshooting-Guide.md):** Comprehensive problem solving
- **[GitHub Repository](https://github.com/Jhanz111/libreoffice-containerized-mcp-server):** Source code and issues
- **[README](README.md):** Project overview and features

## 🎯 Support

If you encounter issues:

1. **Check the [Troubleshooting Guide](Troubleshooting-Guide.md)**
2. **Verify all prerequisites are installed**
3. **Test container manually before Claude Desktop integration**
4. **Report issues on [GitHub](https://github.com/Jhanz111/libreoffice-containerized-mcp-server/issues)**

---

**🎉 Congratulations! You now have the world's first AI-powered LibreOffice template management system ready to transform your document workflows!**