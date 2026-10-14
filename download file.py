import requests
from bs4 import BeautifulSoup
import re

def download_playlist():
    base_url = "https://plsemar.pages.dev"
    output_filename = "plsemarasli.m3u"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    print(f"Membuka halaman utama: {base_url}")
    try:
        response = requests.get(base_url, headers=headers, timeout=30)
        if response.status_code != 200:
            print(f"Gagal mengakses halaman utama, status: {response.status_code}")
            return

        html_content = response.text

        # 1. Cek apakah halaman utama ini ternyata sudah berisi teks M3U di suatu bagian
        if "#EXTM3U" in html_content:
            with open(output_filename, "w", encoding="utf-8") as f:
                f.write(html_content)
            print("[SUKSES] Berhasil menyimpan isi playlist langsung dari halaman.")
            return

        # 2. Jika berupa HTML, cari semua link (.m3u atau link download) di dalam halaman
        soup = BeautifulSoup(html_content, 'html.parser')
        target_link = None

        # Cari tag <a> yang mengarah ke file m3u atau teks tombol download
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if '.m3u' in href or 'download' in href.lower():
                target_link = href
                break

        # Jika tidak ketemu di tag <a>, coba cari menggunakan Regex di seluruh teks HTML
        if not target_link:
            urls = re.findall(r'https?://[^\s<>"]+?\.m3u[^\s<>"]*', html_content)
            if urls:
                target_link = urls[0]

        # Jika link ditemukan, download isi dari link tersebut
        if target_link:
            if not target_link.startswith('http'):
                # Jika link relatif, gabungkan dengan base_url
                if target_link.startswith('/'):
                    target_link = base_url.rstrip('/') + target_link
                else:
                    target_link = base_url.rstrip('/') + '/' + target_link

            print(f"Menemukan link playlist target: {target_link}")
            playlist_resp = requests.get(target_link, headers=headers, timeout=30)
            
            if playlist_resp.status_code == 200:
                with open(output_filename, "w", encoding="utf-8") as f:
                    f.write(playlist_resp.text)
                print(f"[SUKSES] Playlist asli berhasil disimpan sebagai '{output_filename}'")
            else:
                print(f"Gagal mendownload dari link target, status: {playlist_resp.status_code}")
        else:
            print("[GAGAL] Tidak dapat menemukan link .m3u di dalam halaman tersebut.")
            # Simpan HTML apa adanya untuk cadangan pengecekan
            with open(output_filename, "w", encoding="utf-8") as f:
                f.write(html_content)

    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan: {e}")

if __name__ == "__main__":
    download_playlist()
