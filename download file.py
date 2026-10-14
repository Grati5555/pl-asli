import requests

def download_playlist():
    url = "https://plsemar.pages.dev"
    output_filename = "plsemarasli.m3u"
    
    # Header penyamaran agar lolos dari proteksi Cloudflare Pages
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    print(f"Mengambil data dari {url}...")
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            content = response.text
            
            # Simpan langsung ke file output
            with open(output_filename, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"[SUKSES] Playlist berhasil disimpan sebagai '{output_filename}'")
        else:
            print(f"[GAGAL] Server merespon dengan kode error: {response.status_code}")
            
    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan: {e}")

if __name__ == "__main__":
    download_playlist()
