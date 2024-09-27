
import whisper
from get_links import sections_list
import yt_dlp
import os




def get_videos():
    videos = []
    for session in sections_list:
        for video in session[0]:
            videos.append(video)
    return videos

def download_audios(videos):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s', 
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',     
            'preferredquality': '192',    
        }],}

    output_folder = 'audios_will_be_then_deleted'
    os.makedirs(output_folder, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'), 
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',     
            'preferredquality': '192',    
        }],}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for video in videos:
            ydl.download([video])
    return output_folder

def get_transcriptions(output_folder):
    model = whisper.load_model("base")  
    transcriptions = []
    audio_files = [f for f in os.listdir(output_folder) if f.endswith('.mp3')]

    for audio_file in audio_files:
        audio_path = os.path.join(output_folder, audio_file)
        print(f"Transcribing {audio_file}...")
        result = model.transcribe(audio_path)
        transcriptions.append(result["text"])
    return transcriptions

def delete_folder(output_folder):
    for root, dirs, files in os.walk(output_folder, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(output_folder)



if __name__== "__main__":
    videos = get_videos()
    output_folder = download_audios(videos)
    transcriptions = get_transcriptions(output_folder)
    delete_folder(output_folder)




