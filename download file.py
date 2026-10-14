import requests
import re

def download_playlist():
    output_filename = "plsemarasli.m3u"
    
    # Target URL alternatif yang memuat data asli berdasarkan struktur auth semar
    target_urls = [
        "https://auth.semar.my.id/playlist.m3u",
        "https://auth.semar.my.id/list.m3u",
        "https://plsemar.pages.dev/playlist.m3u",
        "https://plsemar.pages.dev"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://plsemar.pages.dev/"
    }

    best_content = None

    for url in target_urls:
        print(f"Mencoba mengakses: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=20)
            if response.status_code == 200:
                content = response.text
                # Cek apakah isinya benar-benar playlist M3U (memiliki tag channel)
                if "#EXTM3U" in content and ("group-title" in content or "tvg-id" in content or len(content.splitlines()) > 10):
                    best_content = content
                    print(f"[SUKSES] Berhasil mendapatkan playlist valid dari {url}")
                    break
        except Exception as e:
            print(f"Gagal pada {url}: {e}")

    # Jika melalui direct URL belum ketemu, coba ekstrak dari file auth.js jika ada
    if not best_content:
        try:
            print("Mencoba mengambil data dari skrip auth...")
            js_resp = requests.get("https://auth.semar.my.id/auth.js", headers=headers, timeout=20)
            if js_resp.status_code == 200:
                # Cari link m3u di dalam file javascript
                found_links = re.findall(r'https?://[^\s<>"\']+\.m3u8?[^\s<>"\']*', js_resp.text)
                for link in found_links:
                    print(f"Mendownload dari link di auth.js: {link}")
                    r = requests.get(link, headers=headers, timeout=20)
                    if r.status_code == 200 and "#EXTM3U" in r.text:
                        best_content = r.text
                        break
        except Exception as e:
            print(f"Error pada auth.js: {e}")

    # Simpan hasil akhir
    if best_content:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(best_content)
        print(f"[SELESAI] File playlist berhasil disimpan ke {output_filename}")
    else:
        print("[GAGAL] Belum berhasil menemukan playlist channel. Menyimpan halaman utama...")
        # Fallback terakhir ambil dari pages.dev
        r = requests.get("https://plsemar.pages.dev", headers=headers)
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(r.text)

if __name__ == "__main__":
    download_playlist()
