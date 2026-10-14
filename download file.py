import requests
import re

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
        if response.status_code == 200:
            html_content = response.text
            
            # Cari apakah ada URL file .m3u atau link API tersembunyi di dalam skrip JS HTML
            # Contohnya mencocokkan pola URL di dalam file javascript
            found_urls = re.findall(r'https?://[^\s<>"\']+\.m3u[^\s<>"\']*', html_content)
            
            if found_urls:
                target_m3u = found_urls[0]
                print(f"Menemukan link sumber M3U: {target_m3u}")
                res_m3u = requests.get(target_m3u, headers=headers, timeout=30)
                if res_m3u.status_code == 200:
                    with open(output_filename, "w", encoding="utf-8") as f:
                        f.write(res_m3u.text)
                    print("[SUKSES] Playlist M3U asli berhasil didownload!")
                    return

            # Jika tidak ada link langsung, coba cari script auth.js atau file pendukung lainnya
            script_urls = re.findall(r'src=["\']([^"\']+\.js[^"\']*)["\']', html_content)
            for js_url in script_urls:
                if not js_url.startswith('http'):
                    js_url = base_url.rstrip('/') + '/' + js_url.lstrip('/')
                
                print(f"Memeriksa file skrip: {js_url}")
                js_resp = requests.get(js_url, headers=headers, timeout=15)
                if js_resp.status_code == 200:
                    # Cari apakah ada link m3u di dalam file Javascript tersebut
                    js_m3u = re.findall(r'https?://[^\s<>"\']+\.m3u[^\s<>"\']*', js_resp.text)
                    if js_m3u:
                        real_url = js_m3u[0]
                        print(f"Menemukan link di dalam JS: {real_url}")
                        final_res = requests.get(real_url, headers=headers, timeout=30)
                        if final_res.status_code == 200:
                            with open(output_filename, "w", encoding="utf-8") as f:
                                f.write(final_res.text)
                            print("[SUKSES] Playlist berhasil diambil melalui skrip JS!")
                            return

            # Fallback terakhir: jika #EXTM3U terselip di suatu tempat
            if "#EXTM3U" in html_content:
                start_idx = html_content.find("#EXTM3U")
                with open(output_filename, "w", encoding="utf-8") as f:
                    f.write(html_content[start_idx:])
                print("[SUKSES] Berhasil memotong dan menyimpan M3U.")
                return

        print("[GAGAL] Tidak dapat menemukan sumber link playlist di halaman ini.")
        
    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan: {e}")

if __name__ == "__main__":
    download_playlist()
