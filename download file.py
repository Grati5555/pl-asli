import requests
import sys

def download_playlist():
    url = "https://plsemar.pages.dev"
    output_filename = "plsemarasli.m3u"
    
    # Headers lengkap agar dikenali sebagai browser asli
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://plsemar.pages.dev/"
    }

    print(f"Mencoba mengambil data dari {url}...")
    
    try:
        # Menggunakan session dan timeout untuk menghindari blokir
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=30)
        
        print(f"Status Kode Server: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # Simpan ke file
            with open(output_filename, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"[SUKSES] Playlist berhasil disimpan sebagai '{output_filename}'")
        else:
            print(f"[GAGAL] Server menolak dengan kode: {response.status_code}")
            sys.exit(1)
            
    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan koneksi: {e}")
        sys.exit(1)

if __name__ == "__main__":
    download_playlist()
