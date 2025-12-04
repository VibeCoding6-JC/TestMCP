"""
Simple HTTP Client untuk mengakses MCP Server (tanpa library MCP)
Menggunakan httpx untuk SSE connection
"""

import httpx
import json
import uuid

# Konfigurasi Server
MCP_SERVER_URL = "http://103.164.191.212:6969"


def call_tool(session_id: str, tool_name: str, arguments: dict) -> dict:
    """Call a tool on the MCP server"""
    
    message = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    
    url = f"{MCP_SERVER_URL}/messages/?session_id={session_id}"
    
    response = httpx.post(
        url,
        json=message,
        headers={"Content-Type": "application/json"},
        timeout=30.0
    )
    
    return response.json()


def get_session_id() -> str:
    """Get session ID from SSE endpoint"""
    
    with httpx.stream("GET", f"{MCP_SERVER_URL}/sse", timeout=10.0) as response:
        for line in response.iter_lines():
            if line.startswith("data:"):
                data = line[5:].strip()
                # Parse session_id dari URL
                if "session_id=" in data:
                    return data.split("session_id=")[1]
    return None


def initialize_session(session_id: str) -> dict:
    """Initialize MCP session"""
    
    message = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "simple-mcp-client",
                "version": "1.0.0"
            }
        }
    }
    
    url = f"{MCP_SERVER_URL}/messages/?session_id={session_id}"
    
    response = httpx.post(
        url,
        json=message,
        headers={"Content-Type": "application/json"},
        timeout=30.0
    )
    
    return response.json()


def list_tools(session_id: str) -> dict:
    """List available tools"""
    
    message = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": "tools/list",
        "params": {}
    }
    
    url = f"{MCP_SERVER_URL}/messages/?session_id={session_id}"
    
    response = httpx.post(
        url,
        json=message,
        headers={"Content-Type": "application/json"},
        timeout=30.0
    )
    
    return response.json()


def main():
    print(f"🔗 Connecting to MCP Server: {MCP_SERVER_URL}")
    print("=" * 50)
    
    # 1. Get session ID
    print("📡 Getting session ID...")
    session_id = get_session_id()
    if not session_id:
        print("❌ Failed to get session ID")
        return
    print(f"   Session ID: {session_id[:20]}...")
    print()
    
    # 2. Initialize session
    print("🔧 Initializing session...")
    init_result = initialize_session(session_id)
    print(f"   Server: {init_result.get('result', {}).get('serverInfo', {}).get('name', 'Unknown')}")
    print()
    
    # 3. List tools
    print("📦 Available Tools:")
    print("-" * 30)
    tools_result = list_tools(session_id)
    tools = tools_result.get("result", {}).get("tools", [])
    for tool in tools:
        print(f"  • {tool['name']}: {tool.get('description', '')}")
    print()
    
    # 4. Test 'hello' tool
    print("🧪 Testing 'hello' tool...")
    result = call_tool(session_id, "hello", {"name": "World"})
    content = result.get("result", {}).get("content", [{}])[0].get("text", "No result")
    print(f"   Result: {content}")
    print()
    
    # 5. Test 'calculate' tool
    print("🧪 Testing 'calculate' tool...")
    operations = [
        {"operation": "add", "a": 10, "b": 5},
        {"operation": "multiply", "a": 7, "b": 8},
    ]
    for op in operations:
        result = call_tool(session_id, "calculate", op)
        content = result.get("result", {}).get("content", [{}])[0].get("text", "No result")
        print(f"   {op['a']} {op['operation']} {op['b']} = {content}")
    print()
    
    # 6. Test 'get_time' tool
    print("🧪 Testing 'get_time' tool...")
    result = call_tool(session_id, "get_time", {"timezone": "Asia/Jakarta"})
    content = result.get("result", {}).get("content", [{}])[0].get("text", "No result")
    print(f"   Result: {content}")
    print()
    
    # 7. Test 'server_info' tool
    print("🧪 Testing 'server_info' tool...")
    result = call_tool(session_id, "server_info", {})
    content = result.get("result", {}).get("content", [{}])[0].get("text", "No result")
    print(f"   Result: {content}")
    print()
    
    print("=" * 50)
    print("✅ All tests completed!")


if __name__ == "__main__":
    main()
