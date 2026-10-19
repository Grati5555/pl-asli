import urllib.request

# URL sumber playlist
SOURCE_URL = "https://bestpl.my.id/rijal4921"
OUTPUT_FILE = "PLmytoko2.m3u"

def update_playlist():
    print(f"Mengambil data dari: {SOURCE_URL}")
    try:
        # Mengunduh konten dari sumber dengan User-Agent agar tidak diblokir
        req = urllib.request.Request(
            SOURCE_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            
        # Menyimpan ke file output
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Berhasil memperbarui {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"Terjadi kesalahan saat memperbarui playlist: {e}")
        exit(1)

if __name__ == "__main__":
    update_playlist()
