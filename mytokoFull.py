import urllib.request
import urllib.error

SOURCE_URL = "https://bestpl.my.id/rijal4921"
OUTPUT_FILE = "PLmytoko2.m3u"

def update_playlist():
    print(f"Mengambil data dari: {SOURCE_URL}")
    try:
        # Menyamar sebagai browser desktop agar tidak diblokir oleh server sumber
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
        
        req = urllib.request.Request(SOURCE_URL, headers=headers)
        
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            
        # Periksa apakah konten yang diambil berisi format M3U
        if "#EXTM3U" not in content:
            print("Peringatan: Konten yang diunduh tidak memiliki format #EXTM3U.")
        
        # Menyimpan hasil ke file PLmytoko2.m3u
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Berhasil memperbarui {OUTPUT_FILE} dengan sempurna!")
        
    except urllib.error.HTTPError as e:
        print(f"Gagal HTTP: {e.code} - {e.reason}")
        exit(1)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        exit(1)

if __name__ == "__main__":
    update_playlist()
