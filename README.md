
# TikTok Automated
![An example of the videos](https://i.imgur.com/MPNTg4y.png)

You have probably seen these types of videos tons of times. Gameplay at the bottom, Some random video clip at the top. It's so lazily made. So I decided to be even lazier and automate it. 

This project is a combination of two projects. Mine (Which grabs clips, creates the videos and what not) and ```xXChezyXx```'s [TikTok AutoUpload project](https://github.com/xXChezyXx/TikTok-AutoUpload)

I am kinda new to Github so if there is anything "off" or something I should add tell me. There will be updates to this project but not in a looooooooong time. Enjoy the project :>
## Features

- Scheduling TikTok Uploads (In its own way)
- TikTok Uploads
- Count number of clips available
- Prepare the YT Clips straight from the channel of your choice
- Prepare the Gameplay clips




## Setup
1. Install Python3.7+: Ensure you have Python 3.7+ installed on your system. If not, you can download and install it from https://www.python.org/downloads/.

2. Install NodeJS 19.3+: Ensure you have NodeJS 19.3+ installed on your system. If not, you can download and install it from https://nodejs.org/en/download/.

3. Install the requirements with pip
```
python -m pip install -r requirements.txt
```

Now you will need a few things. 
- SessionID (View ```xXChezyXx```'s [TikTok AutoUpload project](https://github.com/xXChezyXx/TikTok-AutoUpload) on how to obtain)
- Channel ID (You can use a website like [this](https://commentpicker.com/youtube-channel-id.php))
- Github Repo (Can be private. We need this because when the program grabs a YouTube Video it will store the link here so it knows not to go get it again)
- GitHub Token (Which can edit and view private repos)
- Google API ([This](https://developers.google.com/docs/api/quickstart/python) documentation should help)

All you need is something like this below. Refer to it as this is what the GitHub file structure in the code will be based off.

![Simple Github Repo](https://i.imgur.com/y5GDdQ9.png)

## Configuring the Script
Go to the main.py file then add the following:

- Line 62, 88 - An example could be ```"Holding-Space/TikTok-Automation-Files"```
- Line 63, 89 - An example could be ```"Mr Beast/UploadedVideos.txt"```
- Line 64, 87 - Add your Github Token which can view and private repos here
- Line 85 - Your Google API Token
- Line 86 - Channel ID
- Line 208 - The URL of your gameplay (Subway Surfers for now)
- Line 333 - Your SessionID
## Screenshots

![Main Menu](https://i.imgur.com/kbLldLZ.png)

![Clips Counted Screen](https://i.imgur.com/6EpjAHl.png)

![Gameplay Clips being made](https://i.imgur.com/glOYBIM.png)
## Disclaimer

This was made for educational purposes. Please use this reponsibly and I am not liable for any damages that could happen

