import urllib.request
import urllib.error

SOURCE_URL = "https://bestpl.my.id/rijal4921"
OUTPUT_FILE = "PLmytoko2.m3u"

def update_playlist():
    print(f"Mengambil data dari: {SOURCE_URL}")
    try:
        # Header lengkap agar terbaca sebagai browser desktop
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        
        req = urllib.request.Request(SOURCE_URL, headers=headers)
        
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            
        # Validasi apakah hasil unduhan benar-benar playlist M3U
        if "#EXTM3U" not in content:
            print("Error: Konten yang didapat bukan format M3U yang valid!")
            exit(1)
            
        # Simpan ke file M3U
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Berhasil memperbarui {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        exit(1)

if __name__ == "__main__":
    update_playlist()
