import requests
from bs4 import BeautifulSoup
import urllib.parse

def download_playlist():
    base_url = "https://plsemar.pages.dev"
    output_filename = "plsemarasli.m3u"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://plsemar.pages.dev/"
    }

    print(f"Mengakses {base_url}...")
    try:
        response = requests.get(base_url, headers=headers, timeout=30)
        if response.status_code != 200:
            print(f"Gagal mengakses halaman, status: {response.status_code}")
            return

        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Kumpulkan semua link yang berakhiran atau mengandung .m3u / .m3u8
        potential_links = []
        
        # 1. Cari dari tag <a> atau tag sumber lain
        for tag in soup.find_all(['a', 'source', 'iframe'], href=True):
            href = tag.get('href') or tag.get('src')
            if href and ('.m3u' in href or '.m3u8' in href):
                full_url = urllib.parse.urljoin(base_url, href)
                potential_links.append(full_url)

        # 2. Cari juga menggunakan teks/skrip di dalam halaman
        import re
        text_urls = re.findall(r'https?://[^\s<>"\']+\.m3u8?[^\s<>"\']*', html_content)
        for u in text_urls:
            if u not in potential_links:
                potential_links.append(u)

        print(f"Ditemukan {len(potential_links)} kandidat link playlist.")

        # Cek dan download link yang merupakan master playlist (bukan segmen kecil .ts)
        best_content = None
        for link in potential_links:
            print(f"Memeriksa link: {link}")
            try:
                res = requests.get(link, headers=headers, timeout=15)
                if res.status_code == 200:
                    content = res.text
                    # Pastikan ini playlist channel (biasanya ada banyak baris #EXTINF atau group-title)
                    if "#EXTM3U" in content and ("group-title" in content or len(content.splitlines()) > 20):
                        best_content = content
                        print(f"[ketemu] Master playlist valid ditemukan dari: {link}")
                        break
            except:
                continue

        # Jika ketemu master playlist, simpan
        if best_content:
            with open(output_filename, "w", encoding="utf-8") as f:
                f.write(best_content)
            print(f"[SUKSES] Berhasil menyimpan master playlist ke '{output_filename}'")
        else:
            print("[PERINGATAN] Tidak ditemukan master playlist multi-channel. Menyimpan halaman utama...")
            with open(output_filename, "w", encoding="utf-8") as f:
                f.write(html_content)

    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan: {e}")

if __name__ == "__main__":
    download_playlist()
