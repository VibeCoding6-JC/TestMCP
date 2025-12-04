"""
Simple MCP Client untuk mengakses MCP Server yang sudah dideploy
"""

import asyncio
import json
from mcp import ClientSession
from mcp.client.sse import sse_client

# Konfigurasi Server
MCP_SERVER_URL = "http://103.164.191.212:6969/sse"


async def main():
    print(f"🔗 Connecting to MCP Server: {MCP_SERVER_URL}")
    print("=" * 50)
    
    async with sse_client(MCP_SERVER_URL) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize session
            await session.initialize()
            print("✅ Connected to MCP Server!\n")
            
            # 1. List available tools
            print("📦 Available Tools:")
            print("-" * 30)
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"  • {tool.name}: {tool.description}")
            print()
            
            # 2. Test 'hello' tool
            print("🧪 Testing 'hello' tool...")
            result = await session.call_tool("hello", {"name": "World"})
            print(f"   Result: {result.content[0].text}")
            print()
            
            # 3. Test 'calculate' tool
            print("🧪 Testing 'calculate' tool...")
            operations = [
                {"operation": "add", "a": 10, "b": 5},
                {"operation": "subtract", "a": 10, "b": 5},
                {"operation": "multiply", "a": 10, "b": 5},
                {"operation": "divide", "a": 10, "b": 5},
            ]
            for op in operations:
                result = await session.call_tool("calculate", op)
                print(f"   {op['a']} {op['operation']} {op['b']} = {result.content[0].text}")
            print()
            
            # 4. Test 'get_time' tool
            print("🧪 Testing 'get_time' tool...")
            result = await session.call_tool("get_time", {"timezone": "Asia/Jakarta"})
            print(f"   Result: {result.content[0].text}")
            print()
            
            # 5. Test 'server_info' tool
            print("🧪 Testing 'server_info' tool...")
            result = await session.call_tool("server_info", {})
            print(f"   Result: {result.content[0].text}")
            print()
            
            print("=" * 50)
            print("✅ All tests completed!")


if __name__ == "__main__":
    asyncio.run(main())
