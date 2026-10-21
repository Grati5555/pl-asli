import urllib.request
import urllib.error

SOURCE_URL = "https://bestpl.my.id/rijal4921"
OUTPUT_FILE = "PLmytoko2.m3u"

def update_playlist():
    print(f"Mengambil data dari: {SOURCE_URL}")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        
        req = urllib.request.Request(SOURCE_URL, headers=headers)
        
        with urllib.request.urlopen(req) as response:
            raw_content = response.read().decode('utf-8', errors='ignore')
            
        # Proses pembersihan: Hanya ambil baris yang benar-benar bagian dari M3U
        cleaned_lines = []
        capture = False
        
        for line in raw_content.splitlines():
            stripped = line.strip()
            
            # Mulai merekam ketika menemukan tag awal m3u atau tag info channel
            if stripped.startswith("#EXTM3U") or stripped.startswith("#EXTINF") or stripped.startswith("#EXTVLCOPT") or stripped.startswith("#KODIPROP"):
                capture = True
                
            if capture:
                cleaned_lines.append(line)
                
        # Jika file sama sekali tidak terdeteksi tag m3u, ambil semua teks mentahnya sebagai fallback
        if not cleaned_lines:
            cleaned_lines = raw_content.splitlines()

        # Gabungkan kembali baris yang sudah bersih
        final_content = "\n".joi(cleaned_lines) if 'joi' not in locals() else "\n".join(cleaned_lines)
        
        # Simpan ke file output
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(final_content)
            
        print(f"Berhasil membersihkan dan memperbarui {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        exit(1)

if __name__ == "__main__":
    update_playlist()
