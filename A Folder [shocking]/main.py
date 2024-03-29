# READ THE COMMENTS CAUSE DONT COMPLAIN WHEN SMTH DOESNT WORK

# READ THE ________ !!! (Fill in the blanks)
# A) Comments
# B) Comets
# C) Sozin's Comet
# D) Sung Drip Woo

### Imports
import random
import os
import random
import requests
import time
import threading
import customtkinter

from g4f.client import Client
from bs4 import BeautifulSoup
from plyer import notification
from tkinter import messagebox
from googleapiclient.discovery import build
from github import Github
from pytube import YouTube
from moviepy.editor import VideoFileClip, clips_array
from tiktok_autoupload import upload_video


### Global Variables
scheduling = False
countingdown = False
seconds = 0

### Functions
def send_notification(title, message): # Displays Windows Notifications based on whats happening
    notification.notify(
        title=title,
        message=message,
        timeout=10,  # Notification will disappear after 10 seconds
        app_icon="Resources\\TikTok Auto Icon.ico",
        app_name="TikTok Automation (Mr Beast)", # Change to whatever tbh
    )
    print(f"{message}")

def create_captions(): # Uses AI to create "compelling" captions so TikTok doesn't think I botted the video.
    def get_youtube_video_title(url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.find('meta', property='og:title')
                if title:
                    return title['content']
                else:
                    return "Title not found"
            else:
                return f"Failed to retrieve page content. Status code: {response.status_code}"
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def get_last_line_from_github_repo():
        repo_name = "" # Enter the Name of your GitHub Repo
        file_path = "" # Path to the .txt file
        github_token = "" # GitHub Token (Preferably one that can access private repos)


        github = Github(github_token)
        repo = github.get_repo(repo_name)
        file = repo.get_contents(file_path)
        existing_content = file.decoded_content.decode("utf-8")
        last_line = existing_content.strip().split('\n')[-1]
        return last_line
        
    client = Client() # We using AI in this joint :O
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"There is a YouTube Video titled '{get_youtube_video_title(get_last_line_from_github_repo())}'. I decided to create a clip from this video. Give me another captivating caption I could use for social media with no hastags."}],
    )

    return response.choices[0].message.content


def YouTube_Prep1():
    def get_random_video_url():
        api_key = '' # Google API goes here
        channel_id = '' # Channel ID goes here. Did you know it doesn't have to be just Mr Beast 🤯
        github_token = '' # GitHub Token Blah Blah Blah
        repo_name = '' # Repo Name (Including User (User/RepoName) ) Bla blah blah
        file_path = '' # Path to the TXT file Blah blah blah

        youtube = build('youtube', 'v3', developerKey=api_key)

        # Get playlist items from the uploads playlist of the channel
        uploads_playlist = youtube.channels().list(
            id=channel_id,
            part='contentDetails'
        ).execute()['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        # Get all videos in the uploads playlist
        playlist_items = []
        next_page_token = None
        while True:
            playlist_request = youtube.playlistItems().list(
                playlistId=uploads_playlist,
                part='contentDetails',
                maxResults=50,
                pageToken=next_page_token
            )
            playlist_response = playlist_request.execute()
            playlist_items.extend(playlist_response['items'])
            next_page_token = playlist_response.get('nextPageToken')
            if not next_page_token:
                break

        # Iterate through the playlist items starting from the newest
        for video_item in playlist_items:
            video_id = video_item['contentDetails']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            # Check if the URL already exists in the GitHub repository
            github = Github(github_token)
            repo = github.get_repo(repo_name)
            file = repo.get_contents(file_path)
            existing_content = file.decoded_content.decode("utf-8")

            # If the URL already exists, continue to the next video
            if video_url in existing_content:
                continue

            # Append the new URL to the file
            new_content = existing_content + video_url + '\n'
            repo.update_file(file_path, "Add YouTube video URL", new_content, file.sha)
            return video_url

        # If all videos are already uploaded, return None
        return None

    def download_youtube_video(url, output_path=''):
        try:
            yt = YouTube(url)
            # Get the highest quality video stream
            video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            if not video:
                raise Exception("No video with progressive download available.")
            filename = os.path.join(output_path, 'full_youtube_video.mp4')
            video.download(output_path, filename=filename)
            return True
        except Exception as e:
            print(f"[-] An error occurred: {e}")
            return False

    def split_video_into_clips():
        video_path = 'full_youtube_video.mp4' # When it downloads the video it saves it as this
        output_folder = 'YouTube Clips' # Where the clips are being stored, it matters
        try:
            # Create the output folder if it doesn't exist
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            
            # Load the video
            video = VideoFileClip(video_path)
            
            # Calculate the total duration of the video
            total_duration = video.duration
            
            # Split the video into 30-second clips
            clip_duration = 30  # seconds
            clip_number = 0
            for i in range(0, int(total_duration), clip_duration):
                start_time = i
                clip_number += 1
                end_time = min(i + clip_duration, total_duration)
                clip = video.subclip(start_time, end_time)
                clip_filename = os.path.join(output_folder, f"clip_{clip_number}.mp4")
                clip.write_videofile(clip_filename, codec="libx264")
            
            video.close()

            os.remove(f"YouTube Clips\\clip_{clip_number}.mp4") # See it matters here 
            os.remove(f"{video_path}")
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    print("[-] Preparing YouTube Clips...")

    # Get YouTube Video URL
    print("[-] Grabbing Random YouTube URL...")
    random_video_url = get_random_video_url()

    # Download Video
    print("[-] Downloading Video...")
    download_youtube_video(random_video_url, output_path='')

    # Split Video into Clips
    print("[-] Splitting Video into Clips...")
    split_video_into_clips()

    enable_buttons()
def YouTube_Prep():
    disable_buttons()
    youtube_prep_button.configure(text="Working...")
    threading.Thread(target=YouTube_Prep1).start()

def Gameplay_Prep1():
    def download_youtube_video():
        url = "https://www.youtube.com/watch?v=4GZRICFNeT0" # The gameplay, its the same one everytime but you can change to whatever you want
        output_path=''

        try:
            yt = YouTube(url)
            # Get the highest quality video stream
            video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            if not video:
                raise Exception("No video with progressive download available.")
            filename = os.path.join(output_path, 'full_gameplay_video.mp4')
            video.download(output_path, filename=filename)
            return True
        except Exception as e:
            print(f"[-] An error occurred: {e}")
            return False
        
    def split_video_into_clips_no_audio():
        video_path = 'full_gameplay_video.mp4' # Downloaded as this, if you paid attention you'll know why it matters
        output_folder = 'Gameplay Clips' # Where the clips go

        try:
            # Create the output folder if it doesn't exist
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            
            # Load the video
            video = VideoFileClip(video_path)
            
            # Calculate the total duration of the video
            total_duration = video.duration
            
            # Split the video into 30-second clips
            clip_duration = 30  # seconds
            clip_number = 0
            for i in range(0, int(total_duration), clip_duration):
                clip_number += 1
                start_time = i
                end_time = min(i + clip_duration, total_duration)
                clip = video.subclip(start_time, end_time)
                clip_filename = os.path.join(output_folder, f"clip_{clip_number}.mp4")
                clip.write_videofile(clip_filename, codec="libx264", audio=False)
            
            video.close()

            os.remove(f"Gameplay Clips\\clip_{clip_number}.mp4") # ...
            os.remove(f"{video_path}")
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        
    print("[-] Preparing Gameplay Clips...")

    # Download Video
    print("[-] Downloading Video...")
    download_youtube_video()

    # Split Video into Clips
    print("[-] Splitting Video into Clips...")
    split_video_into_clips_no_audio()

    enable_buttons()
def Gameplay_Prep():
    disable_buttons()
    gameplay_prep_button.configure(text="Working...")
    threading.Thread(target=Gameplay_Prep1).start()

def TikTok_Prep1():
    def combine_clips():
        gameplay_folder = 'Gameplay Clips' # Where da clips go
        youtube_folder = 'YouTube Clips'
        output_folder = 'TikTok Clips' # Gets uploaded shortly after the finished video is put here so don't worry if you're not seeing anything

        try:
            # Create the output folder if it doesn't exist
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            
            # Get list of gameplay clips
            gameplay_clips = [clip for clip in os.listdir(gameplay_folder) if clip.endswith('.mp4')]
            # Get list of youtube clips
            youtube_clips = [clip for clip in os.listdir(youtube_folder) if clip.endswith('.mp4')]
            
            # Choose random clips from each folder
            gameplay_clip_name = random.choice(gameplay_clips)
            youtube_clip_name = random.choice(youtube_clips)
            
            # Load video clips
            gameplay_clip = VideoFileClip(os.path.join(gameplay_folder, gameplay_clip_name))
            youtube_clip = VideoFileClip(os.path.join(youtube_folder, youtube_clip_name))
            
            # Resize gameplay clip to half height and maintain aspect ratio
            gameplay_clip = gameplay_clip.resize(height=int(gameplay_clip.h / 2), width=int(gameplay_clip.w / 2))

            # Resize YouTube clip to half height and maintain aspect ratio
            youtube_clip = youtube_clip.resize(height=int(youtube_clip.h / 2), width=int(youtube_clip.w / 2))

            # Find the maximum width of the resized clips
            max_width = max(gameplay_clip.w, youtube_clip.w)

            # Resize clips to have the same width
            gameplay_clip = gameplay_clip.resize(width=max_width)
            youtube_clip = youtube_clip.resize(width=max_width)

            # Combine clips
            final_clip = clips_array([[youtube_clip], [gameplay_clip]])
            
            # Write final clip to file
            final_clip_path = os.path.join(output_folder, 'final_clip.mp4')
            final_clip.write_videofile(final_clip_path, codec="libx264")
            
            # Close clips
            gameplay_clip.close()
            youtube_clip.close()
            
            # Delete source clips
            os.remove(os.path.join(gameplay_folder, gameplay_clip_name))
            os.remove(os.path.join(youtube_folder, youtube_clip_name))
            
            return True
        except Exception as e:
            print(f"[-] An error occurred: {e}")
            return False

    # TikTok Upload Settings - where the magic happens
    sessionid = "" # Place your TikTok session ID here
    video = "TikTok Clips\\final_clip.mp4"
    title = f"{create_captions()} Tags: #mrbeast #mrbeastvideo #videoviral #foryou #mrbeastchallenge #viralvideotiktok #popular #views" # Change the Tags to whatever depending on what you're uploading
    print("[-] Combining clips")
    # Combine Clips
    combine_clips()

    # Upload Video to TikTok
    upload_video(sessionid, video, title) # Video is uploaded :o
    os.remove(f"{video}")

    enable_buttons()
def TikTok_Prep():
    disable_buttons()
    tiktok_prep_button.configure(text="Working...")
    threading.Thread(target=TikTok_Prep1).start()

def count_files_in_folders1():
    folder1 = 'Gameplay Clips' # I mean as im writing this some of this stuff is pretty obvious what it does idk if i should put more detail in these comments
    folder2 = 'YouTube Clips'

    try:
        # Get the list of files in the first folder
        files_folder1 = os.listdir(folder1)
        # Get the list of files in the second folder
        files_folder2 = os.listdir(folder2)
        
        # Count the number of files in each folder
        num_files_folder1 = len(files_folder1)
        num_files_folder2 = len(files_folder2)
        
        # Display message box with counts
        message = (
            f"[+] {folder1}: {num_files_folder1}\n"
            f"[+] {folder2}: {num_files_folder2}"
        )
        messagebox.showinfo("Number of Clips", message)

        count_files_button.configure(text="Count Clips", state="enabled")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
def count_files_in_folders():
    count_files_button.configure(text="Working...", state="disabled")
    threading.Thread(target=count_files_in_folders1).start()

def upload_schedule1():
    global scheduling
    global seconds
    minutes = minute.get()
    seconds = minutes * 60
    scheduling = True
    while scheduling:
        threading.Thread(target=TikTok_Prep).start()
        threading.Thread(target=show_countdown).start()
        time.sleep(seconds)
def upload_schedule():
    global scheduling

    scheduling = True
    threading.Thread(target=upload_schedule1).start()
    start_button.configure(state="disabled")

def cancel_upload_schedule():
    global scheduling
    # Cancel the timer if it's running
    if scheduling == True:
        scheduling = False
        message = "[+] All events cancelled"
        messagebox.showinfo("Schedule Upload", message)
        enable_buttons()
    elif scheduling == False:
        message = "[-] No events were found!"
        messagebox.showinfo("Number of Clips", message)
        enable_buttons()

def disable_buttons():
    start_button.configure(state="disabled")
    youtube_prep_button.configure(state="disabled")
    gameplay_prep_button.configure(state="disabled")
    tiktok_prep_button.configure(state="disabled")
def enable_buttons():
    global scheduling
    if scheduling == False:
        start_button.configure(text = "Start", state="enabled")
    youtube_prep_button.configure(text = "Prepare YT Video", state="enabled")
    gameplay_prep_button.configure(text = "Prepare Gameplay", state="enabled")
    tiktok_prep_button.configure(text = "Upload TikTok", state="enabled")

def show_countdown():
    global seconds
    for i in range(seconds, 0, -1):
        if tiktok_prep_button.cget("text") == "Upload TikTok" and gameplay_prep_button.cget("text") == "Prepare Gameplay" and youtube_prep_button.cget("text") == "Prepare YT Video" and start_button.cget("state") == "disabled":
            print(f"[+] Seconds remaining: {i}")
        elif start_button.cget("state") == "enabled":
            print("[+] Timer Cancelled")
            break
        time.sleep(1)


### Tkinter Stuff - I am not explaining a single thing here 
# 😭(you)
        
## Main Configs
app = customtkinter.CTk() 
app.title("Mr Beast TikTok Automation")
app.resizable(False, False)
app.attributes("-topmost", True)
app.iconbitmap("Resources\\TikTok Auto Icon.ico")

## Frame Stuff
# Structured as Frame... 
ClipsPrep_frame = customtkinter.CTkFrame(app)
ClipsPrep_frame.grid(row=0, column=0, padx=(5,0), pady=(5, 5), sticky="nsw")
# ... and Frame Label
ClipsPrep_label = customtkinter.CTkLabel(ClipsPrep_frame, text="Clip Preparation", fg_color="gray30", corner_radius=6)
ClipsPrep_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")


Others_frame = customtkinter.CTkFrame(app)
Others_frame.grid(row=0, column=1, padx=5, pady=(5, 5), sticky="nsw")
Others_label = customtkinter.CTkLabel(Others_frame, text="Other", fg_color="gray30", corner_radius=6)
Others_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

Scheduling_frame = customtkinter.CTkFrame(app)
Scheduling_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky="nsw")
Scheduling_label = customtkinter.CTkLabel(Scheduling_frame, text="Scheduling TikTok Upload", fg_color="gray30", corner_radius=6)
Scheduling_label.grid(row=0, column=0, columnspan=2, padx=5, pady=(10, 5), sticky="ew")

## Buttons
youtube_prep_button = customtkinter.CTkButton(ClipsPrep_frame, text="Prepare YT Video", command=YouTube_Prep)
youtube_prep_button.grid(row=1, column=0, padx=5, pady=5)

gameplay_prep_button = customtkinter.CTkButton(ClipsPrep_frame, text="Prepare Gameplay", command=Gameplay_Prep)
gameplay_prep_button.grid(row=2, column=0, padx=5, pady=(0, 5))

tiktok_prep_button = customtkinter.CTkButton(Others_frame, text="Upload TikTok", command=TikTok_Prep)
tiktok_prep_button.grid(row=1, column=0, padx=5, pady=5)

count_files_button = customtkinter.CTkButton(Others_frame, text="Count Clips", command=count_files_in_folders)
count_files_button.grid(row=2, column=0, padx=5, pady=(0, 5))

## Auto Upload Stuff
# Entry for inputting minutes
trigger_minutes_label = customtkinter.CTkLabel(Scheduling_frame, text="Every Minute:")
trigger_minutes_label.grid(row=1, column=0, padx=5, pady=5)

minute = customtkinter.IntVar(value = 10)  # Default trigger minute is 5
trigger_minutes_entry = customtkinter.CTkEntry(Scheduling_frame, textvariable=minute)
trigger_minutes_entry.grid(row=1, column=1, padx=5, pady=5)

# Button to start schedule
start_button = customtkinter.CTkButton(Scheduling_frame, text="Start", command=upload_schedule)
start_button.grid(row=2, column=0, padx=5, pady=5)

# Button to cancel schedule
cancel_button = customtkinter.CTkButton(Scheduling_frame, text="Cancel", command=cancel_upload_schedule)
cancel_button.grid(row=2, column=1, padx=5, pady=5)

# Start Tkinter loop
os.system("cls")
app.mainloop()







### Notes and Stuff - Incase I wanted to use it later idk 🤷‍♂️
# pady = (2, 0) # Pads the top not bottom
