import requests
import flet as ft
import asyncio
import threading
import os
import fnmatch
import time
import schedule

api_url = "https://wshr.hasaki.vn/api/hr/music/songs/current-video-file?category_id=2"

def get_current_video():
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        file_path = data.get("data", {}).get("current", {}).get("file")
        duration = data.get("data", {}).get("current", {}).get("duration", 0)
        if file_path:
            base_url_music = f"{file_path}"
            name_of_video = base_url_music.split('/')[-1]
            video_filename = str(duration) +"_" + name_of_video 
            return base_url_music, video_filename, duration
        
def download_video(current_video, video_filename):
    if not os.path.exists("./video"):
        os.makedirs("./video")
    response = requests.get(current_video)
    if response.status_code == 200:
        with open(f"./video/{video_filename}", 'wb') as f:
            f.write(response.content)

async def play(page: ft.Page):
    try:
        while True:
            current_video,video_filename,duration = get_current_video()
      
            threading.Thread(target=download_video, args=(current_video,video_filename)).start()
            if current_video:
                media = [
                    ft.VideoMedia(
                        f"{current_video}"),
                ]
                page.controls.clear()
                page.add(
                    video := ft.Video(
                        expand=True,
                        playlist=media,
                        playlist_mode=ft.PlaylistMode.LOOP,
                        aspect_ratio=9/16,
                        volume=100,
                        autoplay=True,
                        muted=False,
                        
                    ),
                )

                await asyncio.sleep(duration)
            else:
                await asyncio.sleep(1)
    except Exception as e:
        folder_path = os.path.expanduser("./video")
        
        video_files = [file_name for file_name in os.listdir(folder_path) if fnmatch.fnmatch(file_name, '*.mp4')]
        if video_files:
            media_local = []

            for file_name in video_files:
                media_local.append(ft.VideoMedia(f"./video/{file_name}"))
            page.controls.clear()
            page.add(
                video := ft.Video(

                    expand=True,
                    playlist=media_local,
                    playlist_mode=ft.PlaylistMode.LOOP,
                    aspect_ratio=9/16,
                    volume=100,
                    autoplay=True,
                    muted=False,
                    
                ),
            )
            duration_local = int(file_name.split("_")[0])
            await asyncio.sleep(duration_local)


        else:
            print("Không có video để phát!")
            await asyncio.sleep(1)

def clear_videos():
    folder_path = os.path.expanduser("./video")
    video_files = [file_name for file_name in os.listdir(folder_path) if fnmatch.fnmatch(file_name, '*.mp4')]
    for file_name in video_files:
        os.remove(os.path.join(folder_path, file_name))
    print("All video files have been cleared.")

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.title = "HASAKI VIDEO"
    page.window_always_on_top = True
    page.spacing = 5
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    schedule.every().monday.at("08:00").do(clear_videos)
    threading.Thread(target=run_scheduler, daemon=True).start()

    asyncio.run(play(page))

if __name__ == '__main__':
    ft.app(target=main)