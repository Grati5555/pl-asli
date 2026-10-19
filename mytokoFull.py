import urllib.request
import urllib.error

# URL sumber playlist
SOURCE_URL = "https://bestpl.my.id/rijal4921"
OUTPUT_FILE = "PLmytoko2.m3u"

def update_playlist():
    print(f"Mengambil data dari: {SOURCE_URL}")
    try:
        # Menggunakan headers yang menyerupai browser asli secara lengkap
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        
        req = urllib.request.Request(SOURCE_URL, headers=headers)
        
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            
        # Validasi sederhana: pastikan isinya adalah M3U, bukan halaman HTML
        if "<html" in content.lower() or "<doctype" in content.lower():
            print("Peringatan: Sumber mengembalikan halaman HTML, bukan playlist M3U.")
            print("Kemungkinan link sumber memerlukan token khusus atau diblokir.")
        
        # Menyimpan ke file output
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Berhasil memperbarui {OUTPUT_FILE}")
        
    except urllib.error.HTTPError as e:
        print(f"Gagal HTTP: {e.code} - {e.reason}")
        exit(1)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        exit(1)

if __name__ == "__main__":
    update_playlist()
