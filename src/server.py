"""
MCP Server untuk ChatGPT Integration
Mengimplementasikan tools 'search' dan 'fetch' sesuai spesifikasi OpenAI
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any

from fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inisialisasi MCP Server
mcp = FastMCP(
    name="Simple MCP Server",
    instructions="""
    This MCP server provides search and document retrieval capabilities
    for ChatGPT connectors and deep research. Use the search tool to find 
    relevant information, then use the fetch tool to retrieve complete content.
    """
)

# Konfigurasi Server
HOST = "0.0.0.0"
PORT = 6969

# ============================================================================
# Sample Data Store (simulasi database/knowledge base)
# Ganti dengan data source Anda sendiri (database, API, vector store, dll)
# ============================================================================

DOCUMENTS = {
    "doc-1": {
        "id": "doc-1",
        "title": "Panduan MCP Server",
        "text": """
        Model Context Protocol (MCP) adalah protokol terbuka yang menjadi standar industri 
        untuk memperluas kemampuan AI dengan tools dan knowledge tambahan.
        
        MCP Server dapat digunakan untuk:
        1. Menghubungkan AI ke data sources pribadi
        2. Menyediakan tools khusus untuk AI
        3. Integrasi dengan sistem eksternal
        
        Untuk membuat MCP server yang kompatibel dengan ChatGPT, Anda perlu mengimplementasikan
        dua tools utama: 'search' untuk mencari dokumen dan 'fetch' untuk mengambil konten lengkap.
        """,
        "url": "https://modelcontextprotocol.io/introduction",
        "metadata": {"category": "documentation", "language": "id"}
    },
    "doc-2": {
        "id": "doc-2",
        "title": "Cara Menggunakan Calculator",
        "text": """
        Calculator MCP Tool mendukung operasi matematika dasar:
        
        1. Addition (add): Menjumlahkan dua angka
           Contoh: 10 + 5 = 15
        
        2. Subtraction (subtract): Mengurangkan dua angka
           Contoh: 10 - 5 = 5
        
        3. Multiplication (multiply): Mengalikan dua angka
           Contoh: 10 × 5 = 50
        
        4. Division (divide): Membagi dua angka
           Contoh: 10 ÷ 5 = 2
        
        Gunakan tool 'calculate' dengan parameter operation, a, dan b.
        """,
        "url": "https://example.com/calculator-guide",
        "metadata": {"category": "tutorial", "language": "id"}
    },
    "doc-3": {
        "id": "doc-3",
        "title": "Server Information",
        "text": """
        Simple MCP Server v1.0.0
        
        Server ini menyediakan beberapa tools:
        - hello: Greeting/salam
        - calculate: Kalkulator matematika
        - get_time: Mendapatkan waktu server
        - server_info: Informasi server
        - search: Mencari dokumen (untuk ChatGPT)
        - fetch: Mengambil konten dokumen (untuk ChatGPT)
        
        Server berjalan di port 6969 dengan SSE transport.
        Endpoint: http://your-server:6969/sse
        """,
        "url": "https://example.com/server-info",
        "metadata": {"category": "info", "version": "1.0.0"}
    },
    "doc-4": {
        "id": "doc-4",
        "title": "Integrasi dengan ChatGPT",
        "text": """
        Untuk mengintegrasikan MCP Server dengan ChatGPT:
        
        1. Deploy MCP server ke server publik
        2. Pastikan endpoint /sse dapat diakses dari internet
        3. Di ChatGPT Settings → Connectors → tambahkan MCP server URL
        4. URL harus diakhiri dengan /sse/
        
        Contoh URL: https://your-server.com:6969/sse/
        
        ChatGPT akan menggunakan tools 'search' dan 'fetch' untuk
        mengakses data dari MCP server Anda.
        
        Untuk API integration, gunakan Responses API dengan tool type "mcp".
        """,
        "url": "https://platform.openai.com/docs/mcp",
        "metadata": {"category": "integration", "platform": "chatgpt"}
    }
}


# ============================================================================
# ChatGPT Required Tools: search dan fetch
# ============================================================================

@mcp.tool()
async def search(query: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Search for documents based on a query string.
    
    This tool searches through the knowledge base to find semantically relevant matches.
    Returns a list of search results with basic information. Use the fetch tool to get
    complete document content.
    
    Args:
        query: Search query string. Natural language queries work best.
        
    Returns:
        Dictionary with 'results' key containing list of matching documents.
        Each result includes id, title, text snippet, and URL.
    """
    if not query or not query.strip():
        return {"results": []}
    
    query_lower = query.lower()
    results = []
    
    for doc_id, doc in DOCUMENTS.items():
        # Simple keyword matching (ganti dengan vector search untuk production)
        title_match = query_lower in doc["title"].lower()
        text_match = query_lower in doc["text"].lower()
        
        # Juga cek kata-kata individual
        query_words = query_lower.split()
        word_matches = sum(
            1 for word in query_words 
            if word in doc["title"].lower() or word in doc["text"].lower()
        )
        
        if title_match or text_match or word_matches > 0:
            # Buat snippet dari text
            text_snippet = doc["text"][:200].strip() + "..." if len(doc["text"]) > 200 else doc["text"].strip()
            
            results.append({
                "id": doc["id"],
                "title": doc["title"],
                "text": text_snippet,
                "url": doc["url"]
            })
    
    logger.info(f"Search query: '{query}' - Found {len(results)} results")
    return {"results": results}


@mcp.tool()
async def fetch(id: str) -> Dict[str, Any]:
    """
    Retrieve complete document content by ID for detailed analysis and citation.
    
    Use this after finding relevant documents with the search tool to get complete
    information for analysis and proper citation.
    
    Args:
        id: Document ID from search results
        
    Returns:
        Complete document with id, title, full text content, URL, and metadata
        
    Raises:
        ValueError: If the specified ID is not found
    """
    if not id:
        raise ValueError("Document ID is required")
    
    if id not in DOCUMENTS:
        raise ValueError(f"Document with ID '{id}' not found")
    
    doc = DOCUMENTS[id]
    
    result = {
        "id": doc["id"],
        "title": doc["title"],
        "text": doc["text"].strip(),
        "url": doc["url"],
        "metadata": doc.get("metadata")
    }
    
    logger.info(f"Fetched document: {id}")
    return result


# ============================================================================
# Additional Tools (bonus tools untuk fungsi lain)
# ============================================================================

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
        Informasi tentang server dan tools yang tersedia
    """
    info = {
        "name": "Simple MCP Server",
        "version": "1.0.0",
        "description": "MCP Server dengan integrasi ChatGPT",
        "tools": ["search", "fetch", "hello", "calculate", "get_time", "server_info"],
        "chatgpt_compatible": True,
        "endpoint": f"http://{HOST}:{PORT}/sse"
    }
    return json.dumps(info, indent=2)


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    print(f"🚀 Starting MCP Server on http://{HOST}:{PORT}")
    print(f"📡 SSE endpoint: http://{HOST}:{PORT}/sse")
    print(f"📨 Messages endpoint: http://{HOST}:{PORT}/messages/")
    print()
    print("🔧 Available Tools:")
    print("   - search: Search documents (ChatGPT compatible)")
    print("   - fetch: Fetch document content (ChatGPT compatible)")
    print("   - hello: Greeting tool")
    print("   - calculate: Calculator")
    print("   - get_time: Get server time")
    print("   - server_info: Server information")
    print()
    
    # Jalankan server dengan SSE transport
    mcp.run(transport="sse", host=HOST, port=PORT)
