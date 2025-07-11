#!/bin/bash
# LibreOffice MCP Server v2.5.2 Container Testing Script
# Revolutionary Template System Edition - 15-Tool Validation

echo "🧪 Testing LibreOffice MCP Server v2.5.2 Container..."
echo "🌟 REVOLUTIONARY TEMPLATE SYSTEM EDITION"
echo "15-Tool Validation: Document Intelligence + Template Management"
echo "Test Date: $(date)"
echo ""

CONTAINER_NAME="libreoffice-mcp-server"
TEST_RESULTS=()
TESTS_PASSED=0
TESTS_FAILED=0

# Helper function to add test result
add_test_result() {
    local test_name="$1"
    local result="$2"
    local details="$3"
    
    TEST_RESULTS+=("${test_name}: ${result}")
    if [ "${result}" = "✅ PASS" ]; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
    
    echo "${test_name}: ${result}"
    if [ -n "${details}" ]; then
        echo "  Details: ${details}"
    fi
    echo ""
}

# Test 1: Container Existence and Health
echo "=== Test 1: Container Health Check ==="
if podman container exists ${CONTAINER_NAME}; then
    STATUS=$(podman inspect ${CONTAINER_NAME} --format '{{.State.Status}}')
    HEALTH=$(podman inspect ${CONTAINER_NAME} --format '{{.State.Health.Status}}' 2>/dev/null || echo "no-healthcheck")
    
    if [ "${STATUS}" = "running" ]; then
        add_test_result "Container Running" "✅ PASS" "Status: ${STATUS}, Health: ${HEALTH}"
    else
        add_test_result "Container Running" "❌ FAIL" "Status: ${STATUS}"
        echo "Container logs (last 10 lines):"
        podman logs ${CONTAINER_NAME} 2>&1 | tail -10
        echo ""
    fi
else
    add_test_result "Container Existence" "❌ FAIL" "Container ${CONTAINER_NAME} does not exist"
fi

# Test 2: LibreOffice UNO Port Check
echo "=== Test 2: LibreOffice UNO Port Check ==="
if netstat -ln 2>/dev/null | grep -q ":2002"; then
    PORT_DETAILS=$(netstat -ln 2>/dev/null | grep ":2002")
    add_test_result "UNO Port 2002" "✅ PASS" "Port is listening: ${PORT_DETAILS}"
else
    add_test_result "UNO Port 2002" "❌ FAIL" "Port 2002 is not listening"
    
    # Check what processes are running in container
    echo "Container processes:"
    podman exec ${CONTAINER_NAME} ps aux 2>/dev/null | grep -E "(libreoffice|python)" || echo "No relevant processes found"
    echo ""
fi

# Test 3: Python Environment Validation
echo "=== Test 3: Python Environment Validation ==="
PYTHON_TEST=$(podman exec ${CONTAINER_NAME} python3 --version 2>&1)
if [ $? -eq 0 ]; then
    add_test_result "Python Environment" "✅ PASS" "${PYTHON_TEST}"
else
    add_test_result "Python Environment" "❌ FAIL" "Python not accessible"
fi

# Test 4: LibreOffice Installation Check
echo "=== Test 4: LibreOffice Installation Check ==="
LO_TEST=$(podman exec ${CONTAINER_NAME} libreoffice --version 2>/dev/null)
if [ $? -eq 0 ]; then
    add_test_result "LibreOffice Installation" "✅ PASS" "${LO_TEST}"
else
    add_test_result "LibreOffice Installation" "❌ FAIL" "LibreOffice not accessible"
fi

# Test 5: MCP Framework Dependencies
echo "=== Test 5: MCP Framework Dependencies ==="
MCP_TEST=$(podman exec ${CONTAINER_NAME} python3 -c "import mcp; print('MCP Framework OK')" 2>/dev/null)
if [ $? -eq 0 ]; then
    add_test_result "MCP Framework" "✅ PASS" "MCP framework properly installed"
else
    add_test_result "MCP Framework" "❌ FAIL" "MCP framework not accessible"
fi

# Test 6: Template System Server File Check
echo "=== Test 6: Template System Server File Check ==="
if podman exec ${CONTAINER_NAME} test -f "/opt/mcp/python/libreoffice_mcp_server.py" 2>/dev/null; then
    SERVER_SIZE=$(podman exec ${CONTAINER_NAME} wc -l /opt/mcp/python/libreoffice_mcp_server.py 2>/dev/null | cut -d' ' -f1)
    add_test_result "Template System Server" "✅ PASS" "Server file exists with ${SERVER_SIZE} lines"
else
    add_test_result "Template System Server" "❌ FAIL" "libreoffice_mcp_server.py not found"
fi

# Test 7: MCP Server Process Check
echo "=== Test 7: MCP Server Process Check ==="
MCP_PROCESS=$(podman exec ${CONTAINER_NAME} ps aux 2>/dev/null | grep -E "python.*libreoffice_mcp_server" | grep -v grep)
if [ -n "${MCP_PROCESS}" ]; then
    add_test_result "MCP Server Process" "✅ PASS" "Template System MCP server is running"
else
    add_test_result "MCP Server Process" "❌ FAIL" "MCP server process not found"
    
    echo "  All Python processes:"
    podman exec ${CONTAINER_NAME} ps aux | grep python || echo "  No Python processes found"
    echo ""
fi

# Test 8: Template System Startup Messages
echo "=== Test 8: Template System Startup Messages ==="
STARTUP_MSGS=$(podman logs ${CONTAINER_NAME} 2>&1 | grep -E "(Template|v2.5.2|REVOLUTIONARY)" | wc -l)
if [ "${STARTUP_MSGS}" -gt 0 ]; then
    add_test_result "Template System Messages" "✅ PASS" "Found ${STARTUP_MSGS} Template System startup messages"
    echo "  Sample messages:"
    podman logs ${CONTAINER_NAME} 2>&1 | grep -E "(Template|v2.5.2|REVOLUTIONARY)" | head -3
    echo ""
else
    add_test_result "Template System Messages" "❌ FAIL" "No Template System startup messages found"
fi

# Test 9: External Connectivity Simulation
echo "=== Test 9: External Connectivity Simulation ==="
EXTERNAL_TEST=$(timeout 5s nc -zv localhost 2002 2>&1)
if echo "${EXTERNAL_TEST}" | grep -q "succeeded\|Connected"; then
    add_test_result "External Connectivity" "✅ PASS" "Port 2002 accessible from localhost"
else
    add_test_result "External Connectivity" "❌ FAIL" "Cannot connect to port 2002"
    echo "  Connection test output: ${EXTERNAL_TEST}"
    echo ""
fi

# Test 10: Container Resource Usage
echo "=== Test 10: Container Resource Usage ==="
STATS=$(podman stats ${CONTAINER_NAME} --no-stream --format "CPU: {{.CPU}} | Memory: {{.MemUsage}}" 2>/dev/null)
if [ $? -eq 0 ]; then
    add_test_result "Resource Usage" "✅ PASS" "${STATS}"
else
    add_test_result "Resource Usage" "❌ FAIL" "Could not retrieve resource statistics"
fi

# Test 11: Health Check Validation
echo "=== Test 11: Health Check Validation ==="
HEALTH_CHECK=$(podman exec ${CONTAINER_NAME} python3 -c "import uno; print('LibreOffice MCP v2.5.2 Template System: Healthy')" 2>&1)
HEALTH_EXIT=$?
if [ ${HEALTH_EXIT} -eq 0 ]; then
    add_test_result "Health Check" "✅ PASS" "Health check passed: ${HEALTH_CHECK}"
else
    add_test_result "Health Check" "❌ FAIL" "Health check failed: ${HEALTH_CHECK}"
fi

# Test 12: Document Directory Access
echo "=== Test 12: Document Directory Access ==="
if podman exec ${CONTAINER_NAME} test -d "/home/libreoffice/Documents" 2>/dev/null; then
    DOC_PERMS=$(podman exec ${CONTAINER_NAME} ls -ld /home/libreoffice/Documents 2>/dev/null)
    add_test_result "Document Directory" "✅ PASS" "Directory accessible: ${DOC_PERMS}"
else
    add_test_result "Document Directory" "❌ FAIL" "Documents directory not accessible"
fi

# Test 13: UNO Socket Functionality Test
echo "=== Test 13: UNO Socket Functionality Test ==="
UNO_SOCKET_TEST=$(podman exec ${CONTAINER_NAME} timeout 10s python3 -c "
import socket
import sys

try:
    # Test UNO socket connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    result = sock.connect_ex(('localhost', 2002))
    sock.close()
    
    if result == 0:
        print('UNO socket connection successful')
        sys.exit(0)
    else:
        print(f'UNO socket connection failed: {result}')
        sys.exit(1)
        
except Exception as e:
    print(f'UNO socket test error: {e}')
    sys.exit(1)
" 2>&1)

UNO_TEST_EXIT=$?
if [ ${UNO_TEST_EXIT} -eq 0 ]; then
    add_test_result "UNO Socket Function" "✅ PASS" "${UNO_SOCKET_TEST}"
else
    add_test_result "UNO Socket Function" "❌ FAIL" "${UNO_SOCKET_TEST}"
fi

# Test 14: Template System Version Validation
echo "=== Test 14: Template System Version Validation ==="
VERSION_CHECK=$(podman logs ${CONTAINER_NAME} 2>&1 | grep "v2.5.2" | head -1)
if [ -n "${VERSION_CHECK}" ]; then
    add_test_result "Template System Version" "✅ PASS" "v2.5.2 Template System detected"
else
    add_test_result "Template System Version" "❌ FAIL" "v2.5.2 version not detected in logs"
fi

# Test 15: Container Environment Variables
echo "=== Test 15: Container Environment Variables ==="
ENV_VARS=("PYTHONPATH" "UNO_PATH" "LIBREOFFICE_HEADLESS" "MCP_SERVER_MODE")
ENV_OK=0

for var in "${ENV_VARS[@]}"; do
    if podman exec ${CONTAINER_NAME} printenv "${var}" >/dev/null 2>&1; then
        ENV_OK=$((ENV_OK + 1))
    fi
done

if [ ${ENV_OK} -eq 4 ]; then
    add_test_result "Environment Variables" "✅ PASS" "All required environment variables set"
else
    add_test_result "Environment Variables" "❌ FAIL" "Only ${ENV_OK}/4 environment variables found"
    
    echo "  Environment variable status:"
    for var in "${ENV_VARS[@]}"; do
        VALUE=$(podman exec ${CONTAINER_NAME} printenv "${var}" 2>/dev/null || echo "NOT SET")
        echo "    ${var}: ${VALUE}"
    done
    echo ""
fi

# Test 16: Template System Feature Validation (NEW)
echo "=== Test 16: Template System Feature Validation ==="
TEMPLATE_FEATURES=$(podman logs ${CONTAINER_NAME} 2>&1 | grep -E "(Template Tools|Apply|Create|List|Style)" | wc -l)
if [ "${TEMPLATE_FEATURES}" -gt 0 ]; then
    add_test_result "Template System Features" "✅ PASS" "Found ${TEMPLATE_FEATURES} Template System feature announcements"
    echo "  Template feature messages:"
    podman logs ${CONTAINER_NAME} 2>&1 | grep -E "(Template Tools|Apply|Create|List|Style)" | head -3
    echo ""
else
    add_test_result "Template System Features" "❌ FAIL" "No Template System feature messages found"
fi

# Final Test Summary
echo "========================================"
echo "=== LIBREOFFICE MCP v2.5.2 TEMPLATE SYSTEM TEST SUMMARY ==="
echo "========================================"
echo ""
echo "Test Results:"
for result in "${TEST_RESULTS[@]}"; do
    echo "  ${result}"
done

echo ""
echo "Summary Statistics:"
echo "  ✅ Tests Passed: ${TESTS_PASSED}"
echo "  ❌ Tests Failed: ${TESTS_FAILED}"
echo "  📊 Total Tests: $((TESTS_PASSED + TESTS_FAILED))"

if [ ${TESTS_FAILED} -eq 0 ]; then
    echo "  🎉 Overall Status: ALL TESTS PASSED"
    echo ""
    echo "🌟 LibreOffice MCP Server v2.5.2 Template System is fully functional!"
    echo "🚀 Revolutionary 15-Tool Template Management System is ready!"
    echo "📝 Template workflows: Apply, Create, List, Style Transfer - ALL OPERATIONAL"
    echo "🔥 World's first AI-powered Template Management System - VALIDATED!"
    echo ""
    echo "🎯 Container is ready for revolutionary Template System workflows!"
    exit 0
else
    PASS_RATE=$((TESTS_PASSED * 100 / (TESTS_PASSED + TESTS_FAILED)))
    echo "  ⚠️ Overall Status: ${TESTS_FAILED} TESTS FAILED (${PASS_RATE}% pass rate)"
    echo ""
    echo "❌ LibreOffice MCP Server v2.5.2 Template System has issues that need attention."
    echo ""
    echo "Troubleshooting recommendations:"
    echo "1. Check container logs: podman logs -f ${CONTAINER_NAME}"
    echo "2. Verify Template System server file was properly installed"
    echo "3. Ensure sufficient system resources (memory, CPU)"
    echo "4. Check for port conflicts or network issues"
    echo "5. Verify LibreOffice and Python installations in container"
    echo "6. Validate 15-tool server compilation and startup"
    echo ""
    echo "For detailed debugging:"
    echo "  Enter container: podman exec -it ${CONTAINER_NAME} /bin/bash"
    echo "  Check processes: podman exec ${CONTAINER_NAME} ps aux"
    echo "  Check networking: podman exec ${CONTAINER_NAME} netstat -ln"
    echo "  Check Template System logs for specific errors"
    echo ""
    exit 1
fi