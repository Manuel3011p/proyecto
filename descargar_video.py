import yt_dlp
import os

def download_video_audio():
    url = input("Introduce la URL del video: ")
    path = os.getcwd()  # Ruta predeterminada a la carpeta donde se ejecuta el script
    
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
        'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }]
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Descarga completada")
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")

if __name__ == "__main__":
    download_video_audio()