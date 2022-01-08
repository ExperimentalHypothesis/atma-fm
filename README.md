# Online Radio 
Online radio station built on top of the Icecast server using Ices as the streaming client. It is a server-centric website bridging backend streaming Icecast server with frontend GUI. It is written in Python Flask with a little bit of vanilla Javascript.

Online radio is broadcasting live 24/7, streaming mostly ambient/experimental/electronic music. All audio files are located on a VPS server, the code for the website is on the same server. It uses NGINX as reverse proxy and UWSGI as a web server.

URLs for main homepage:   
https://atma.fm  

URLs for direct streaming server links:  
https://atma.fm/channel1-128k  
https://atma.fm/channel2-128k


#### Public API endpoints
For fun I have created a couple of endpoints. All of them are GET endpoints that return JSON format and status code 200 for success. They can be used to get info about currently played song, playlist, artists or albums for each channel. 

- /api/song => returns details about currently played song on both channels
- /api/song/channel1 => returns details about currently played song on channel1
- /api/song/channel2 => returns details about currently played song on channel

- /api/playlist?channel=1&songs=10 => return 10 last played songs on channel 1
- /api/playlist?channel=2&songs=10 => return 10 last played songs on channel 1

- /api/
