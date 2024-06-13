import requests
import flet as ft
import asyncio
import threading
import os
import fnmatch
import time
import schedule


def online():
    url= 'https://raw.githubusercontent.com/Johnny-Hao-Le//hasaki-led-tm/main/main.py'
    token='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'
    headers = {'Authorization': f'token {token}'}
    r = requests.get(url, headers=headers)
    code = r.text
    return code

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
async def play_local(page: ft.Page):
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
                filter_quality=ft.FilterQuality.HIGH,
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

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.title = "HASAKI VIDEO"
    page.window_always_on_top = True
    page.spacing = 5
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    schedule.every().monday.at("08:00").do(clear_videos)
    threading.Thread(target=run_scheduler, daemon=True).start()

    asyncio.run(play_local(page))


if __name__ == "__main__":
    try:
        code = online()
        print(code)
        exec(code)
    except:
        ft.app(target=main)

