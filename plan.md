# Plan: MCP Server dengan FastMCP + GitHub Actions Deployment

## Overview
Membuat MCP (Model Context Protocol) server sederhana menggunakan FastMCP dengan Python, yang akan di-deploy otomatis ke SSH server melalui GitHub Actions.

## Target Server
- **IP Address**: 103.164.191.212
- **Port SSH**: 22193
- **Private Key**: devops01.ppk (akan disimpan sebagai GitHub Secret)

## Struktur Project

```
TestMCP/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions workflow
├── src/
│   └── server.py               # FastMCP server utama
├── requirements.txt            # Dependencies Python
├── README.md                   # Dokumentasi
├── .gitignore                  # Ignore files
└── plan.md                     # File ini
```

## Tahapan Implementasi

### 1. Setup FastMCP Server (`src/server.py`)
- Membuat MCP server sederhana dengan beberapa tools dasar
- Tools yang akan dibuat:
  - `hello` - Tool untuk greeting
  - `calculate` - Tool untuk kalkulasi sederhana
  - `get_time` - Tool untuk mendapatkan waktu server

### 2. Dependencies (`requirements.txt`)
- fastmcp
- python-dateutil

### 3. GitHub Actions Workflow (`.github/workflows/deploy.yml`)
- Trigger: push ke branch `main` atau pull request ke `main`
- Steps:
  1. Checkout code
  2. Setup SSH key dari GitHub Secrets
  3. Deploy ke server via rsync/scp
  4. Restart service di server (jika ada)

### 4. Konfigurasi GitHub Secrets (Manual)
Secrets yang perlu ditambahkan di GitHub repository:
- `SSH_PRIVATE_KEY` - Isi dari private key (convert dari .ppk ke OpenSSH format)
- `SSH_HOST` - 103.164.191.212
- `SSH_PORT` - 22193
- `SSH_USER` - Username SSH server

## Catatan Keamanan
⚠️ **PENTING**: 
- Private key (`devops01.ppk`) TIDAK boleh di-commit ke repository
- Tambahkan ke `.gitignore`
- Simpan sebagai GitHub Secret

## Langkah Deploy Manual (Testing Local)
1. Convert .ppk ke OpenSSH format (jika belum)
2. Test koneksi SSH: `ssh -i devops01.pem -p 22193 user@103.164.191.212`
3. Copy files ke server

## Next Steps
1. ✅ Buat plan.md (file ini)
2. ✅ Buat .gitignore
3. ✅ Buat requirements.txt
4. ✅ Buat src/server.py (FastMCP server)
5. ✅ Buat .github/workflows/deploy.yml
6. ✅ Buat README.md

## ✅ COMPLETED!

### Files Created:
- `plan.md` - Planning dokumen
- `.gitignore` - Ignore private keys dan file Python
- `requirements.txt` - fastmcp, python-dateutil
- `src/server.py` - MCP server dengan 4 tools (hello, calculate, get_time, server_info)
- `.github/workflows/deploy.yml` - Auto deploy ke SSH server
- `README.md` - Dokumentasi lengkap

### Manual Steps Required:
1. Buat repository GitHub baru
2. Tambahkan GitHub Secrets:
   - `SSH_PRIVATE_KEY` - Convert dari devops01.ppk ke OpenSSH format
   - `SSH_HOST` - 103.164.191.212
   - `SSH_PORT` - 22193
   - `SSH_USER` - Username SSH Anda
   - `DEPLOY_PATH` - Path di server (contoh: /home/user/mcp-server)
3. Push code ke GitHub
