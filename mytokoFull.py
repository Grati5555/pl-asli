import os
import urllib.request

def generate_playlist():
    source_file = "mytoko2.txt"
    playlist_file = "PLmytoko2.m3u"
    
    if not os.path.exists(source_file):
        print("File mytoko2.txt tidak ditemukan.")
        return

    # Membaca link sumber dari mytoko2.txt
    with open(source_file, "r", encoding="utf-8") as f:
        links = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    if not links:
        print("Tidak ada link di dalam mytoko2.txt.")
        return

    # Mengambil link pertama dari mytoko2.txt
    target_url = links[0]

    try:
        print(f"Mengambil data dari: {target_url}")
        
        # Mengatur User-Agent agar terbaca seperti browser/downloader
        req = urllib.request.Request(
            target_url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        
        # Mendownload isi file playlist asli dari link sumber
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')

        # Menyimpan isi aslinya ke PLmytoko2.m3u
        with open(playlist_file, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Berhasil memperbarui {playlist_file} dengan isi file playlist asli!")

    except Exception as e:
        print(f"Terjadi kesalahan saat mendownload: {e}")

if __name__ == "__main__":
    generate_playlist()
