import whisper
from pydub import AudioSegment
from moviepy import AudioFileClip, VideoFileClip
from deep_translator import GoogleTranslator
from gtts import gTTS
import os

def traduce_audio():
    archivo = input("Ingrese el archivo de audio o video: ")
    if not archivo:
        print("No se seleccionó ningún archivo")
    # Obtener la duración del video
    video = VideoFileClip(archivo)
    duracion_video = video.duration
    modelo = "medium"
    max_chars = 4950
    print("Duración del video: ", duracion_video)
    
    """
    Transcribe el audio o video usando Whisper y traduce el texto transcrito.

    Args:
        archivo (str): Ruta al archivo de audio o video.
        modelo (str): Modelo de Whisper a usar (por defecto, "medium").
        idioma (str): Idioma del audio (por defecto, "en").
        idioma_destino (str): Idioma al que se traducirá el texto (por defecto, "es").

    Returns:
        str: Texto traducido.
    """
    # Instanciar el traductor
    traductor = GoogleTranslator(source='en', target='es')

    # Transcribir audio
    print("Transcripción del archivo...")

    modelo_whisper = whisper.load_model(modelo)
    resultado = modelo_whisper.transcribe(archivo)

    texto_transcrito = resultado['text']

    print("Traduciendo texto...")

    partes = [texto_transcrito[i:i+max_chars] for i in range(0, len(texto_transcrito), max_chars)]
    partes_traducidas = [traductor.translate(part) for part in partes]

    texto_traducido = " ".join(partes_traducidas)
    print(f"Texto traducido: \n{texto_traducido}")

    return texto_traducido, duracion_video, video

def combinar_archivos(traduccion_del_texto,duracion_video,video):
    try:
        idioma = "es"
        print("Convirtiendo a voz, espere...")

        audio_generado = "audio_generado.mp3"

        voz = gTTS(text=traduccion_del_texto, lang=idioma, slow=False)
        voz.save(audio_generado)
        
        audio = AudioSegment.from_file(audio_generado)
        
        factor_de_velocidad = audio.duration_seconds / duracion_video
        recortar_factor = round(factor_de_velocidad, 5)
        
        # Acelerar el audio
        audio_acelerado = audio.speedup(playback_speed=recortar_factor)

        # Guardar el audio acelerado
        audio_acelerado.export("audio_acelerado.mp3", format="mp3")
        
        os.remove(audio_generado)
        
        audio_en_español = AudioFileClip("audio_acelerado.mp3")
        
        video_con_audio_al_español = video.with_audio(audio_en_español)

        video_con_audio_al_español.write_videofile("video_traducido_al_español.mp4", codec="libx264", audio_codec="aac")
        
        os.remove("audio_acelerado.mp3")

    except Exception as e:
        print(f"Error con la conversión del audio: {e}")

if __name__ == "__main__":
    try:
        traduccion_del_texto, duracion_video, video = traduce_audio()
        combinar_archivos(traduccion_del_texto, duracion_video, video)
    except Exception as e:
        print(f"Error durante la ejecución: {e}")
    except Exception as e:
        print(f"Error durante la traducción o combinación de archivos: {e}")
        
        
        
        
        
        
        