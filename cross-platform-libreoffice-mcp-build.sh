#!/bin/bash
# LibreOffice MCP Server v2.5.2 Cross-Platform Build Script
# Revolutionary Template System Edition - World's First AI-Powered Template Management
#
# Builds the complete 15-tool LibreOffice MCP Server with:
# - Document Creation & Intelligence Tools  
# - Revolutionary Template System (Apply, Create, List, Style Transfer)
# - Advanced Operations (Compare, Merge, Split, Analysis)
# - Cross-Platform Container Support
#
# Supports: Linux, macOS, Windows (Git Bash/WSL2)
# Version: v2.5.2-template-system
# Container: Ubuntu 24.04 + LibreOffice + Python 3.12 + MCP Protocol

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Build configuration
IMAGE_NAME="libreoffice-mcp-server"
VERSION="v2.5.2-template-system"
FULL_IMAGE_NAME="${IMAGE_NAME}:${VERSION}"
CONTAINERFILE="Containerfile.libreoffice-mcp-v2.5.2"
PYTHON_SERVER="libreoffice_mcp_server.py"

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

# Print colored output functions
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

# Display build banner
show_banner() {
    clear
    print_header "╔════════════════════════════════════════════════════════════════╗"
    print_header "║           LibreOffice MCP Server v2.5.2 Builder               ║"
    print_header "║             Revolutionary Template System                      ║"
    print_header "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    print_status "Platform: ${PLATFORM}"
    print_status "Container Runtime: ${CONTAINER_CMD:-"Not detected"}"
    print_status "Build Target: ${FULL_IMAGE_NAME}"
    echo ""
}

# Check build prerequisites
check_prerequisites() {
    print_step "Checking build prerequisites..."
    
    local missing_deps=()
    local warnings=()
    
    # Check for container runtime
    if [ -z "$CONTAINER_CMD" ]; then
        missing_deps+=("Container runtime (Docker or Podman)")
    else
        # Test container runtime
        if ! $CONTAINER_CMD --version &> /dev/null; then
            missing_deps+=("Working container runtime (${CONTAINER_CMD} not responding)")
        fi
    fi
    
    # Check for required files
    if [ ! -f "${CONTAINERFILE}" ]; then
        missing_deps+=("Containerfile: ${CONTAINERFILE}")
    fi
    
    if [ ! -f "${PYTHON_SERVER}" ]; then
        missing_deps+=("Python server: ${PYTHON_SERVER}")
    fi
    
    # Check available disk space (cross-platform)
    if command -v df &> /dev/null; then
        case "$PLATFORM" in
            "Linux"|"macOS")
                AVAILABLE_KB=$(df . | tail -1 | awk '{print $4}')
                ;;
            "Windows")
                # Git Bash df might work differently
                AVAILABLE_KB=$(df . 2>/dev/null | tail -1 | awk '{print $4}' || echo "unknown")
                ;;
        esac
        
        if [ "$AVAILABLE_KB" != "unknown" ] && [ "$AVAILABLE_KB" -lt 2000000 ]; then
            warnings+=("Low disk space: ~$((AVAILABLE_KB/1024))MB available, recommend 2GB+ for LibreOffice build")
        fi
    fi
    
    # Report missing dependencies
    if [ ${#missing_deps[@]} -gt 0 ]; then
        print_error "Missing build prerequisites:"
        for dep in "${missing_deps[@]}"; do
            echo "  ❌ $dep"
        done
        echo ""
        print_status "Please install missing prerequisites and run build again."
        exit 1
    fi
    
    # Report warnings
    if [ ${#warnings[@]} -gt 0 ]; then
        for warning in "${warnings[@]}"; do
            print_warning "$warning"
        done
        echo ""
    fi
    
    print_status "✅ Build prerequisites satisfied"
}

# Get cross-platform build timestamp
get_build_timestamp() {
    case "$PLATFORM" in
        "Linux"|"macOS")
            date -u +'%Y-%m-%dT%H:%M:%SZ'
            ;;
        "Windows")
            # Git Bash should support this, fallback to simple date
            date -u +'%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || date +'%Y-%m-%d %H:%M:%S UTC'
            ;;
        *)
            date +'%Y-%m-%d %H:%M:%S'
            ;;
    esac
}

# Get VCS reference (if in git repo)
get_vcs_ref() {
    if command -v git &> /dev/null && git rev-parse --git-dir &> /dev/null; then
        git rev-parse --short HEAD 2>/dev/null || echo "local"
    else
        echo "local"
    fi
}

# Pre-build cleanup
cleanup_previous_build() {
    print_step "Pre-build cleanup..."
    
    if $CONTAINER_CMD image exists ${FULL_IMAGE_NAME} 2>/dev/null; then
        print_status "Removing existing image: ${FULL_IMAGE_NAME}"
        $CONTAINER_CMD rmi ${FULL_IMAGE_NAME} 2>/dev/null || true
        print_status "✅ Cleanup completed"
    else
        print_status "✅ No existing image to clean up"
    fi
}

# Display build information
show_build_info() {
    print_step "Build Configuration"
    echo ""
    echo "  📋 Build Details:"
    echo "    Image Name: ${FULL_IMAGE_NAME}"
    echo "    Platform: ${PLATFORM}"
    echo "    Container Runtime: ${CONTAINER_CMD}"
    echo "    Containerfile: ${CONTAINERFILE}"
    echo "    Python Server: ${PYTHON_SERVER}"
    echo "    Build Date: $(get_build_timestamp)"
    echo "    VCS Reference: $(get_vcs_ref)"
    echo ""
    echo "  🚀 Revolutionary Features:"
    echo "    • 15-Tool Complete Document Intelligence System"
    echo "    • Revolutionary Template Management (Apply, Create, List, Style Transfer)"
    echo "    • Cross-platform Container Support"
    echo "    • Modern COPY-based Build Architecture"
    echo "    • Template-aware Style Transfer with Placeholder Preservation"
    echo ""
}

# Execute the container build
run_build() {
    print_step "Starting container build..."
    echo ""
    
    local build_start=$(date +%s 2>/dev/null || echo "0")
    local build_args=(
        "--file" "${CONTAINERFILE}"
        "--tag" "${FULL_IMAGE_NAME}"
        "--build-arg" "BUILD_DATE=$(get_build_timestamp)"
        "--build-arg" "VCS_REF=$(get_vcs_ref)"
        "--build-arg" "VERSION=${VERSION}"
        "--progress=plain"
        "."
    )
    
    print_status "Executing: $CONTAINER_CMD build ${build_args[*]}"
    echo ""
    
    # Execute build with proper error handling
    if $CONTAINER_CMD build "${build_args[@]}"; then
        local build_end=$(date +%s 2>/dev/null || echo "0")
        local build_duration=$((build_end - build_start))
        
        echo ""
        print_header "╔════════════════════════════════════════════════════════════════╗"
        print_header "║                    Build Successful! ✅                        ║"
        print_header "╚════════════════════════════════════════════════════════════════╝"
        echo ""
        
        # Display build results
        print_status "🎉 LibreOffice MCP Server v2.5.2 Template System built successfully!"
        if [ "$build_duration" -gt 0 ]; then
            print_status "⏱️  Build Duration: ${build_duration} seconds"
        fi
        echo ""
        
        # Show image information
        print_step "Image Information:"
        if $CONTAINER_CMD images ${FULL_IMAGE_NAME} --format "table" &> /dev/null; then
            $CONTAINER_CMD images ${FULL_IMAGE_NAME} --format "table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.Created}}\t{{.Size}}" 2>/dev/null || true
        fi
        
        # Get image ID for reference
        local image_id
        image_id=$($CONTAINER_CMD images ${FULL_IMAGE_NAME} --format "{{.ID}}" 2>/dev/null | head -1)
        if [ -n "$image_id" ]; then
            echo ""
            print_status "📋 Image ID: ${image_id}"
            print_status "📦 Full Name: ${FULL_IMAGE_NAME}"
        fi
        
        echo ""
        print_step "🌟 Revolutionary Template System Features Built:"
        echo "  📝 template_apply: Apply templates with dynamic placeholder replacement"
        echo "  🏗️  template_create: Convert documents into reusable templates with metadata"
        echo "  📚 template_list: Smart template discovery and library management"
        echo "  🎨 enhanced_style_transfer: Professional formatting workflows"
        echo "  🔥 Complete template ecosystem with multiple placeholder formats"
        echo "  ⚡ Template-aware style transfer preserving placeholders"
        echo ""
        
        print_step "🎯 Next Steps:"
        echo "  1. Run setup script if not already done: ./libreoffice-mcp-setup.sh"
        echo "  2. Add configuration to your AI client (see claude-desktop-config-template.json)"
        echo "  3. Test the Revolutionary Template System workflows"
        echo "  4. Place documents in ./libreoffice-documents/ for processing"
        echo "  5. Experience the world's first AI-powered Template Management System!"
        echo ""
        
        print_status "🎊 REVOLUTIONARY TEMPLATE SYSTEM BUILD COMPLETE!"
        
        return 0
    else
        local build_exit_code=$?
        
        echo ""
        print_header "╔════════════════════════════════════════════════════════════════╗"
        print_header "║                     Build Failed! ❌                          ║"
        print_header "╚════════════════════════════════════════════════════════════════╝"
        echo ""
        
        print_error "❌ Build failed with exit code: ${build_exit_code}"
        echo ""
        
        print_step "🔧 Troubleshooting Recommendations:"
        echo "  1. Check container runtime: $CONTAINER_CMD --version"
        echo "  2. Verify file integrity: ls -la ${CONTAINERFILE} ${PYTHON_SERVER}"
        echo "  3. Check Python syntax: python3 -m py_compile ${PYTHON_SERVER}"
        echo "  4. Ensure sufficient disk space (2GB+ recommended)"
        echo "  5. Check container build logs above for specific errors"
        echo "  6. Verify network connectivity for package downloads"
        echo ""
        
        print_step "🔄 Alternative Options:"
        echo "  • Try building with verbose output: $CONTAINER_CMD build --progress=plain"
        echo "  • Check for other running containers consuming resources"
        echo "  • Consider building with --no-cache for clean build"
        echo "  • Ensure antivirus isn't interfering with container operations"
        echo ""
        
        print_status "💡 If issues persist, please report at:"
        print_status "   https://github.com/basicmachines-co/libreoffice-mcp-server/issues"
        
        return 1
    fi
}

# Main build function
main() {
    # Initialize
    detect_platform
    show_banner
    
    # Pre-build validation
    check_prerequisites
    cleanup_previous_build
    show_build_info
    
    # Confirmation prompt
    echo ""
    read -p "🚀 Ready to build LibreOffice MCP Server v2.5.2 Template System? (y/N): " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_status "Build cancelled by user"
        exit 0
    fi
    
    echo ""
    
    # Execute build
    if run_build; then
        echo ""
        print_status "🎉 Build process completed successfully!"
        exit 0
    else
        echo ""
        print_error "❌ Build process failed!"
        exit 1
    fi
}

# Script entry point
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi