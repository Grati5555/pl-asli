import urllib.request
import urllib.error

# Gunakan URL tujuan akhir atau endpoint API jika ada, 
# atau tambahkan parameter/headers khusus agar server mengembalikan M3U
SOURCE_URL = "https://bestpl.my.id/rijal4921"
OUTPUT_FILE = "PLmytoko2.m3u"

def update_playlist():
    print(f"Mengambil data dari: {SOURCE_URL}")
    try:
        # Menyamar sebagai browser modern dengan header lengkap
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Accept': 'text/plain, */*; q=0.01',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': 'https://bestpl.my.id/',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        req = urllib.request.Request(SOURCE_URL, headers=headers)
        
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            
        # Jika ternyata masih terdeteksi HTML, coba cari tahu apakah ada link download langsung di dalamnya
        if "<html" in content.lower() or "<doctype" in content.lower():
            print("Peringatan: Situs masih merespons dengan HTML.")
            print("Kemungkinan besar halaman ini memerlukan eksekusi JavaScript.")
        
        # Menyimpan konten ke file PLmytoko2.m3u
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
