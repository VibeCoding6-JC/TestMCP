# Simple MCP Server dengan FastMCP

MCP (Model Context Protocol) server sederhana menggunakan FastMCP dengan auto-deployment via GitHub Actions.

## 🚀 Features

- **hello** - Tool untuk greeting/salam
- **calculate** - Tool untuk kalkulasi matematika (add, subtract, multiply, divide)
- **get_time** - Tool untuk mendapatkan waktu server
- **server_info** - Tool untuk info server

## 📁 Struktur Project

```
TestMCP/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions workflow
├── src/
│   └── server.py               # FastMCP server utama
├── Dockerfile                  # Docker image
├── docker-compose.yml          # Docker compose config
├── requirements.txt            # Dependencies Python
├── README.md                   # Dokumentasi ini
├── .gitignore                  # Ignore files
└── plan.md                     # Planning dokumen
```

## 🛠️ Setup Local Development

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd TestMCP
```

### 2. Buat Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Jalankan Server (Local)
```bash
python src/server.py
```

### 5. Jalankan dengan Docker (Recommended)
```bash
docker-compose up -d --build
```

Server akan berjalan di `http://0.0.0.0:6969`

- **SSE Endpoint**: `http://localhost:6969/sse`
- **Messages Endpoint**: `http://localhost:6969/messages/`

## ⚙️ Setup GitHub Actions Deployment

### 1. Tambahkan GitHub Secrets

Pergi ke **Settings > Secrets and variables > Actions** di repository GitHub, lalu tambahkan:

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `SSH_PRIVATE_KEY` | (isi private key OpenSSH) | Private key untuk SSH |
| `SSH_HOST` | `103.164.191.212` | IP address server |
| `SSH_PORT` | `22193` | Port SSH |
| `SSH_USER` | `your-username` | Username SSH |
| `DEPLOY_PATH` | `/home/user/mcp-server` | Path deploy di server |

### 2. Convert PPK ke OpenSSH (jika menggunakan PuTTY key)

```bash
# Install puttygen (Linux)
sudo apt install putty-tools

# Convert
puttygen devops01.ppk -O private-openssh -o devops01.pem
```

### 3. Push ke Main Branch

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

GitHub Actions akan otomatis men-deploy ke server saat ada push atau PR ke branch `main`.

## 🌐 Akses dari IP Public

Setelah deploy, MCP server bisa diakses via:
- **SSE Endpoint**: `http://103.164.191.212:6969/sse`
- **Messages**: `http://103.164.191.212:6969/messages/`

> ⚠️ Pastikan port 6969 dibuka di firewall server!

## 📖 Penggunaan Tools

### Hello Tool
```json
{
  "tool": "hello",
  "arguments": {
    "name": "John"
  }
}
```

### Calculate Tool
```json
{
  "tool": "calculate",
  "arguments": {
    "operation": "add",
    "a": 10,
    "b": 5
  }
}
```

### Get Time Tool
```json
{
  "tool": "get_time",
  "arguments": {
    "timezone": "UTC"
  }
}
```

### Server Info Tool
```json
{
  "tool": "server_info",
  "arguments": {}
}
```

## 🔒 Keamanan

⚠️ **PENTING:**
- Jangan pernah commit private key ke repository
- Gunakan GitHub Secrets untuk menyimpan credentials
- File `.gitignore` sudah dikonfigurasi untuk mengabaikan file sensitif

## 📝 License

MIT License
