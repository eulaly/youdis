build and run the docker container
```
api_token = [discord bot token]
-v [downloads]:/downloads
-v [config]:/config
```
config contains data to persist across container updates, i.e., unraid appdata, 
such as users.json (authorized users) and yt-dlp's archive.txt
