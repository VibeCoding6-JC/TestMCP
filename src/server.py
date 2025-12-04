"""
MCP Server sederhana menggunakan FastMCP dengan HTTP transport
"""

from datetime import datetime
from fastmcp import FastMCP

# Inisialisasi MCP Server
mcp = FastMCP("Simple MCP Server")

# Konfigurasi Server
HOST = "0.0.0.0"  # Listen di semua interface
PORT = 6969       # Port HTTP server


@mcp.tool()
def hello(name: str) -> str:
    """
    Tool untuk memberikan greeting/salam.
    
    Args:
        name: Nama orang yang ingin disapa
        
    Returns:
        Pesan greeting
    """
    return f"Halo, {name}! Selamat datang di MCP Server! 👋"


@mcp.tool()
def calculate(operation: str, a: float, b: float) -> str:
    """
    Tool untuk melakukan kalkulasi matematika sederhana.
    
    Args:
        operation: Operasi matematika (add, subtract, multiply, divide)
        a: Angka pertama
        b: Angka kedua
        
    Returns:
        Hasil kalkulasi
    """
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else "Error: Division by zero"
    }
    
    if operation not in operations:
        return f"Error: Operasi '{operation}' tidak valid. Gunakan: add, subtract, multiply, divide"
    
    result = operations[operation](a, b)
    
    symbols = {"add": "+", "subtract": "-", "multiply": "×", "divide": "÷"}
    symbol = symbols.get(operation, "?")
    
    return f"{a} {symbol} {b} = {result}"


@mcp.tool()
def get_time(timezone: str = "UTC") -> str:
    """
    Tool untuk mendapatkan waktu server saat ini.
    
    Args:
        timezone: Timezone (default: UTC)
        
    Returns:
        Waktu server saat ini
    """
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return f"Waktu server saat ini ({timezone}): {formatted_time}"


@mcp.tool()
def server_info() -> str:
    """
    Tool untuk mendapatkan informasi tentang server MCP ini.
    
    Returns:
        Informasi server
    """
    info = {
        "name": "Simple MCP Server",
        "version": "1.0.0",
        "description": "MCP Server sederhana dengan FastMCP",
        "tools": ["hello", "calculate", "get_time", "server_info"]
    }
    
    return f"""
📦 Server Information
━━━━━━━━━━━━━━━━━━━━━
Name: {info['name']}
Version: {info['version']}
Description: {info['description']}
Available Tools: {', '.join(info['tools'])}
"""


if __name__ == "__main__":
    # Jalankan MCP server dengan HTTP transport
    print(f"🚀 Starting MCP Server on http://{HOST}:{PORT}")
    print(f"📡 SSE endpoint: http://{HOST}:{PORT}/sse")
    print(f"📨 Messages endpoint: http://{HOST}:{PORT}/messages/")
    mcp.run(transport="sse", host=HOST, port=PORT)
