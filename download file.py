import requests
from bs4 import BeautifulSoup

def download_playlist():
    url = "https://plsemar.pages.dev"
    output_filename = "plsemarasli.m3u"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://plsemar.pages.dev/"
    }

    print(f"Mengambil data dari {url}...")
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            html_content = response.text
            
            # Gunakan BeautifulSoup untuk mengambil teks bersih di dalam body atau seluruh dokumen
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Cari apakah teks #EXTM3U ada di dalam dokumen
            raw_text = soup.get_text()
            
            # Jika teks M3U ditemukan di dalamnya, potong dan ambil mulai dari #EXTM3U
            if "#EXTM3U" in raw_text:
                start_idx = raw_text.find("#EXTM3U")
                playlist_content = raw_text[start_idx:]
                
                # Simpan murni sebagai format M3U
                with open(output_filename, "w", encoding="utf-8") as f:
                    f.write(playlist_content)
                print("[SUKSES] Berhasil mengekstrak dan membersihkan file M3U!")
            else:
                # Fallback jika struktur berbeda, simpan apa adanya
                with open(output_filename, "w", encoding="utf-8") as f:
                    f.write(html_content)
                print("[INFO] Menyimpan konten mentah.")
        else:
            print(f"Gagal mengakses server, status: {response.status_code}")
            
    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan: {e}")

if __name__ == "__main__":
    download_playlist()
