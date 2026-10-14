import requests
from bs4 import BeautifulSoup
import urllib.parse

def download_playlist():
    base_url = "https://plsemar.pages.dev"
    output_filename = "plsemarasli.m3u"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    print(f"Mengakses {base_url}...")
    try:
        # Coba akses halaman utama
        response = requests.get(base_url, headers=headers, timeout=30)
        if response.status_code == 200:
            content = response.text
            
            # Jika halaman utama ternyata isinya adalah M3U
            if "#EXTM3U" in content:
                with open(output_filename, "w", encoding="utf-8") as f:
                    f.write(content)
                print("[SUKSES] File M3U ditemukan langsung di halaman utama.")
                return

            # Cari tombol atau link download di HTML
            soup = BeautifulSoup(content, 'html.parser')
            for a in soup.find_all('a', href=True):
                href = a['href']
                if 'm3u' in href.lower() or 'download' in href.lower():
                    target_url = urllib.parse.urljoin(base_url, href)
                    print(f"Mencoba mendownload dari link terkait: {target_url}")
                    res_target = requests.get(target_url, headers=headers, timeout=30)
                    if res_target.status_code == 200 and "#EXTM3U" in res_target.text:
                        with open(output_filename, "w", encoding="utf-8") as f:
                            f.write(res_target.text)
                        print("[SUKSES] Playlist berhasil didownload melalui link target.")
                        return

        print("[INFO] Mencoba jalur langsung alternatif...")
        # Coba beberapa nama file umum jika di-hosting di pages.dev
        alternatives = [
            f"{base_url}/playlist.m3u",
            f"{base_url}/list.m3u",
            f"{base_url}/index.m3u"
        ]
        
        for alt_url in alternatives:
            res_alt = requests.get(alt_url, headers=headers, timeout=15)
            if res_alt.status_code == 200 and "#EXTM3U" in res_alt.text:
                with open(output_filename, "w", encoding="utf-8") as f:
                    f.write(res_alt.text)
                print(f"[SUKSES] Berhasil mendownload dari: {alt_url}")
                return

        print("[GAGAL] Tidak dapat menemukan format M3U yang valid.")
        
    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan: {e}")

if __name__ == "__main__":
    download_playlist()
