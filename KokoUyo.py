import os

def generate_playlist():
    source_file = "Koko.txt"
    playlist_file = "Plkoko.m3u"
    
    if not os.path.exists(source_file):
        print("File Koko.txt tidak ditemukan.")
        return

    with open(source_file, "r", encoding="utf-8") as f:
        links = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    # Menulis ulang file M3U
    with open(playlist_file, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        
        for index, link in enumerate(links, start=1):
            channel_name = f"Stream Video {index}"
            f.write(f'#EXTINF:-1 tvg-id="" tvg-name="{channel_name}" group-title="Google Drive VOD",{channel_name}\n')
            f.write(f"{link}\n")

    print(f"Playlist berhasil diperbarui ke {playlist_file} dengan {len(links)} tautan.")

if __name__ == "__main__":
    generate_playlist()
