#!/bin/bash
# Universal LibreOffice MCP Server v2.5.2 Setup Script
# Revolutionary Template System Edition - World's First AI-Powered Template Management
#
# Creates complete project structure for the 15-tool LibreOffice MCP Server:
# - Document Creation & Intelligence Tools
# - Revolutionary Template System (Apply, Create, List, Style Transfer)  
# - Advanced Operations (Compare, Merge, Split, Analysis)
# - Cross-Platform Installation Automation
#
# Supports: Linux, macOS, and Windows (via Git Bash/WSL)
# Version: v2.5.2-template-system
# Features: Universal setup, platform detection, automated configuration

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Script configuration
SCRIPT_VERSION="v2.5.2-template-system"
PROJECT_NAME="libreoffice-mcp-server"
CONTAINER_IMAGE="${PROJECT_NAME}:${SCRIPT_VERSION}"
DOCS_DIR_NAME="libreoffice-documents"

# Platform detection
detect_platform() {
    case "$(uname -s)" in
        Linux*)     PLATFORM="Linux";;
        Darwin*)    PLATFORM="macOS";;
        CYGWIN*|MINGW*|MSYS*) PLATFORM="Windows";;
        *)          PLATFORM="Unknown";;
    esac
    
    # Detect container runtime
    if command -v podman &> /dev/null; then
        CONTAINER_CMD="podman"
    elif command -v docker &> /dev/null; then
        CONTAINER_CMD="docker"
    else
        CONTAINER_CMD=""
    fi
}

# Print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${PURPLE}$1${NC}"
}

print_step() {
    echo -e "${CYAN}[STEP]${NC} $1"
}

# Display banner
show_banner() {
    clear
    print_header "╔════════════════════════════════════════════════════════════════╗"
    print_header "║               LibreOffice MCP Server Setup                    ║"
    print_header "║                Revolutionary Template System                   ║"
    print_header "║                      Version ${SCRIPT_VERSION}                    ║"
    print_header "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    print_status "Platform: ${PLATFORM}"
    print_status "Container Runtime: ${CONTAINER_CMD:-"Not detected"}"
    echo ""
}

# Check prerequisites
check_prerequisites() {
    print_step "Checking prerequisites..."
    
    local missing_deps=()
    
    # Check for container runtime
    if [ -z "$CONTAINER_CMD" ]; then
        missing_deps+=("Container runtime (Docker or Podman)")
    fi
    
    # Check for git (usually available)
    if ! command -v git &> /dev/null; then
        missing_deps+=("Git")
    fi
    
    # Platform-specific checks
    case "$PLATFORM" in
        "Windows")
            if ! command -v bash &> /dev/null; then
                missing_deps+=("Bash (Git Bash or WSL recommended)")
            fi
            ;;
        "Linux")
            # Most Linux systems should be fine
            ;;
        "macOS")
            # macOS should have most tools by default
            ;;
    esac
    
    if [ ${#missing_deps[@]} -gt 0 ]; then
        print_error "Missing prerequisites:"
        for dep in "${missing_deps[@]}"; do
            echo "  - $dep"
        done
        echo ""
        print_status "Please install the missing prerequisites and run this script again."
        print_status "Installation guides:"
        print_status "  - Docker: https://docs.docker.com/get-docker/"
        print_status "  - Podman: https://podman.io/getting-started/installation"
        exit 1
    fi
    
    print_status "✅ All prerequisites found"
}

# Create project structure
create_project_structure() {
    print_step "Creating project structure..."
    
    # Get current directory
    SETUP_DIR="$(pwd)"
    
    # Create documents directory
    if [ ! -d "$DOCS_DIR_NAME" ]; then
        mkdir -p "$DOCS_DIR_NAME"
        print_status "Created documents directory: $DOCS_DIR_NAME"
    else
        print_status "Documents directory already exists: $DOCS_DIR_NAME"
    fi
    
    # Create logs directory for troubleshooting
    if [ ! -d "logs" ]; then
        mkdir -p "logs"
        print_status "Created logs directory"
    fi
    
    # Set permissions based on platform
    case "$PLATFORM" in
        "Linux"|"macOS")
            chmod 755 "$DOCS_DIR_NAME"
            chmod 755 "logs"
            ;;
    esac
    
    print_status "✅ Project structure created"
}

# Generate platform-specific run script
generate_run_script() {
    print_step "Generating platform-specific run script..."
    
    local run_script_name
    case "$PLATFORM" in
        "Windows") run_script_name="run-libreoffice-mcp.bat" ;;
        *) run_script_name="run-libreoffice-mcp.sh" ;;
    esac
    
    # Get absolute path to documents directory
    local docs_path
    case "$PLATFORM" in
        "Windows")
            # Convert to Windows format for compatibility
            docs_path="$(cygpath -w "$(pwd)/$DOCS_DIR_NAME" 2>/dev/null || echo "$(pwd)/$DOCS_DIR_NAME")"
            ;;
        *)
            docs_path="$(pwd)/$DOCS_DIR_NAME"
            ;;
    esac
    
    # Generate run script
    if [ "$PLATFORM" = "Windows" ]; then
        # Windows batch file
        cat > "$run_script_name" << 'EOL'
@echo off
REM LibreOffice MCP Server v2.5.2 Run Script - Windows
REM Revolutionary Template System Edition

echo Starting LibreOffice MCP Server v2.5.2...
echo Platform: Windows
echo Container Runtime: %CONTAINER_CMD%
echo Documents Path: %DOCS_PATH%
echo.

%CONTAINER_CMD% run --rm -i ^
  -a stdin -a stdout ^
  -v "%DOCS_PATH%:/home/libreoffice/Documents" ^
  localhost/%IMAGE_NAME% 2>logs\mcp-server-error.log

if %ERRORLEVEL% neq 0 (
    echo ERROR: Container failed to start
    echo Check logs\mcp-server-error.log for details
    pause
    exit /b 1
)
EOL
        
        # Set environment variables in batch file
        sed -i "s|%CONTAINER_CMD%|$CONTAINER_CMD|g" "$run_script_name"
        sed -i "s|%DOCS_PATH%|$docs_path|g" "$run_script_name"
        sed -i "s|%IMAGE_NAME%|$CONTAINER_IMAGE|g" "$run_script_name"
        
    else
        # Unix shell script
        cat > "$run_script_name" << EOL
#!/bin/bash
# LibreOffice MCP Server v2.5.2 Run Script - $PLATFORM
# Revolutionary Template System Edition

echo "Starting LibreOffice MCP Server v2.5.2..."
echo "Platform: $PLATFORM"
echo "Container Runtime: $CONTAINER_CMD"
echo "Documents Path: $docs_path"
echo ""

# Run container with proper volume mounting
exec $CONTAINER_CMD run --rm -i \\
  -a stdin -a stdout \\
  -v "$docs_path:/home/libreoffice/Documents" \\
  localhost/$CONTAINER_IMAGE 2>logs/mcp-server-error.log
EOL
        chmod +x "$run_script_name"
    fi
    
    print_status "✅ Created run script: $run_script_name"
}

# Generate build script
generate_build_script() {
    print_step "Generating build script..."
    
    local build_script_name
    case "$PLATFORM" in
        "Windows") build_script_name="build-libreoffice-mcp.bat" ;;
        *) build_script_name="build-libreoffice-mcp.sh" ;;
    esac
    
    if [ "$PLATFORM" = "Windows" ]; then
        # Windows batch file
        cat > "$build_script_name" << 'EOL'
@echo off
REM LibreOffice MCP Server v2.5.2 Build Script - Windows

echo Building LibreOffice MCP Server v2.5.2...
echo Platform: Windows
echo.

%CONTAINER_CMD% build ^
  --file Containerfile.libreoffice-mcp-v2.5.2 ^
  --tag localhost/%IMAGE_NAME% ^
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
echo Image: localhost/%IMAGE_NAME%
pause
EOL
        
        sed -i "s|%CONTAINER_CMD%|$CONTAINER_CMD|g" "$build_script_name"
        sed -i "s|%IMAGE_NAME%|$CONTAINER_IMAGE|g" "$build_script_name"
        
    else
        # Unix shell script
        cat > "$build_script_name" << EOL
#!/bin/bash
# LibreOffice MCP Server v2.5.2 Build Script - $PLATFORM

echo "Building LibreOffice MCP Server v2.5.2..."
echo "Platform: $PLATFORM"
echo ""

$CONTAINER_CMD build \\
  --file Containerfile.libreoffice-mcp-v2.5.2 \\
  --tag localhost/$CONTAINER_IMAGE \\
  --build-arg BUILD_DATE="\$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \\
  --build-arg VERSION="v2.5.2-template-system" \\
  --progress=plain .

if [ \$? -ne 0 ]; then
    echo "ERROR: Build failed"
    exit 1
fi

echo ""
echo "✅ Build completed successfully!"
echo "Image: localhost/$CONTAINER_IMAGE"
EOL
        chmod +x "$build_script_name"
    fi
    
    print_status "✅ Created build script: $build_script_name"
}

# Create configuration template
create_config_template() {
    print_step "Creating configuration template..."
    
    local config_template="claude-desktop-config-template.json"
    
    # Get absolute path for the run script
    local run_script_path
    case "$PLATFORM" in
        "Windows")
            run_script_path="$(cygpath -w "$(pwd)/run-libreoffice-mcp.bat" 2>/dev/null || echo "$(pwd)/run-libreoffice-mcp.bat")"
            ;;
        *)
            run_script_path="$(pwd)/run-libreoffice-mcp.sh"
            ;;
    esac
    
    cat > "$config_template" << EOF
{
  "mcpServers": {
    "libreoffice-mcp": {
      "command": "$CONTAINER_CMD",
      "args": [
        "run", "--rm", "-i",
        "-a", "stdin", "-a", "stdout",
        "-v", "$(pwd)/$DOCS_DIR_NAME:/home/libreoffice/Documents",
        "localhost/$CONTAINER_IMAGE"
      ]
    }
  }
}
EOF
    
    print_status "✅ Created configuration template: $config_template"
}

# Generate platform-specific installation instructions
generate_instructions() {
    print_step "Generating installation instructions..."
    
    local instructions_file="INSTALLATION-${PLATFORM}.md"
    
    cat > "$instructions_file" << EOF
# LibreOffice MCP Server v2.5.2 Installation Guide
## Platform: $PLATFORM

### Quick Start
1. Build the container: \`$([ "$PLATFORM" = "Windows" ] && echo "./build-libreoffice-mcp.bat" || echo "./build-libreoffice-mcp.sh")\`
2. Add configuration to your AI client (see Configuration section below)
3. Start using the Revolutionary Template System!

### Project Structure
\`\`\`
$(pwd)/
├── $DOCS_DIR_NAME/                    # Documents working directory
├── logs/                              # Error logs and debugging
├── $([ "$PLATFORM" = "Windows" ] && echo "run-libreoffice-mcp.bat" || echo "run-libreoffice-mcp.sh")           # Platform-specific run script
├── $([ "$PLATFORM" = "Windows" ] && echo "build-libreoffice-mcp.bat" || echo "build-libreoffice-mcp.sh")         # Platform-specific build script
└── claude-desktop-config-template.json # Configuration template
\`\`\`

### Configuration for Claude Desktop

#### Configuration File Location:
EOF

    # Add platform-specific config locations
    case "$PLATFORM" in
        "macOS")
            echo "- macOS: \`~/Library/Application Support/Claude/claude_desktop_config.json\`" >> "$instructions_file"
            ;;
        "Windows")
            echo "- Windows: \`%APPDATA%\\Claude\\claude_desktop_config.json\`" >> "$instructions_file"
            ;;
        "Linux")
            echo "- Linux: \`~/.config/claude/claude_desktop_config.json\`" >> "$instructions_file"
            ;;
    esac
    
    cat >> "$instructions_file" << EOF

#### Configuration Content:
Copy the content from \`claude-desktop-config-template.json\` to your Claude Desktop configuration file.

### Other AI Clients
For other MCP-compatible clients, use the container run command:
\`\`\`bash
$CONTAINER_CMD run --rm -i \\
  -a stdin -a stdout \\
  -v "$(pwd)/$DOCS_DIR_NAME:/home/libreoffice/Documents" \\
  localhost/$CONTAINER_IMAGE
\`\`\`

### Revolutionary Template System Features
- **template_apply**: Apply templates with placeholder replacement
- **template_create**: Convert documents to reusable templates
- **template_list**: Smart template discovery and management
- **enhanced_style_transfer**: Professional formatting workflows

### Testing
1. Place test documents in \`$DOCS_DIR_NAME/\`
2. Ask your AI: "List available LibreOffice tools"
3. Try: "Create a template from my document and apply it with new data"

### Troubleshooting
- Check \`logs/mcp-server-error.log\` for container errors
- Ensure $CONTAINER_CMD is running: \`$CONTAINER_CMD --version\`
- Verify documents directory permissions
- Test container manually: \`$([ "$PLATFORM" = "Windows" ] && echo "./run-libreoffice-mcp.bat" || echo "./run-libreoffice-mcp.sh")\`

### Support
- Repository: https://github.com/basicmachines-co/libreoffice-mcp-server
- Issues: https://github.com/basicmachines-co/libreoffice-mcp-server/issues
- Documentation: https://github.com/basicmachines-co/libreoffice-mcp-server/wiki
EOF
    
    print_status "✅ Created installation guide: $instructions_file"
}

# Main setup function
main() {
    show_banner
    
    # Platform detection
    detect_platform
    
    # Run setup steps
    check_prerequisites
    create_project_structure
    generate_run_script
    generate_build_script
    create_config_template
    generate_instructions
    
    # Final summary
    echo ""
    print_header "╔════════════════════════════════════════════════════════════════╗"
    print_header "║                    Setup Complete!                            ║"
    print_header "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    print_status "LibreOffice MCP Server v2.5.2 setup completed for $PLATFORM"
    print_status "Container Runtime: $CONTAINER_CMD"
    echo ""
    print_step "Next Steps:"
    echo "  1. $([ "$PLATFORM" = "Windows" ] && echo "./build-libreoffice-mcp.bat" || echo "./build-libreoffice-mcp.sh") - Build the container"
    echo "  2. Add configuration to your AI client using claude-desktop-config-template.json"
    echo "  3. Place documents in $DOCS_DIR_NAME/ for processing"
    echo "  4. Start using the Revolutionary Template System!"
    echo ""
    print_status "📖 See INSTALLATION-${PLATFORM}.md for detailed instructions"
    print_status "🚀 Enjoy the world's first AI-powered Template Management System!"
}

# Run main function
main "$@"