REQUIREMENTS:
  - install pygame module: pip install pygame
  - intall requests module for api: pip install requests
  - install yt_dlp module: python3 -m pip install -U yt-dlp
  - install mutagen module: pip install mutagen

Music player with help of Youtube API. currently plays music by retriving youtube search results, downlaoding and converting the selected file to mp3 and playing it.
Has a few minor bugs such as stop not reseting the time to 00:00:00 and resizing but playing audio works fine.
files alraeady played dont get re downloaded.
Close program deletes all previously downloaded files of the session. 
