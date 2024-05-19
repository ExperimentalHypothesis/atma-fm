# Online Radio 
Online radio station built on top of the Icecast server using Ices as the streaming client. It is a server-centric website bridging backend streaming Icecast server with frontend GUI. It is written in Python Flask with a little bit of vanilla Javascript.

Online radio is broadcasting live 24/7, streaming mostly ambient/experimental/electronic music. All audio files are located on a VPS server, the code for the website is on the same server. It uses NGINX as reverse proxy and UWSGI as a web server.

URLs for main homepage:   
https://atma.fm  

URLs for direct streaming server links:  
https://atma.fm/channel1-128k  
https://atma.fm/channel2-128k

#### Run locally with docker
```sh
    docker build -t atma-fm .
    docker run -p 5555:5555 atma-fm
    # app accessible in http://localhost:5555/
```
#### Run locally with docker-compose
```sh
    docker docker-compose up
    # app accessible in http://localhost:5555/
    # grafana accessible in http://localhost:3000/
```
------
#### API endpoints
For fun I have created a couple of endpoints. All of them use GET method and all return JSON format and status code 200 for success. They can be used to query info about currently played song, playlists, artists or albums for each channel. 

 GET endpoint for current song:
```
api/song => return song details from cue file for both channels  
api/song/channel1 => return song details from cue file from channel1  
api/song/channel2 => return song details from cue file from channel2  
```

GET endpoint for playlist:
```
api/playlist => returns last 10 songs played on both channels  
api/playlist/channel1 => returns last 10 songs played on channel1   
api/playlist/channel2 => returns last 10 songs played on channel2   
api/playlist/channel1?songs=N => returns last N songs played on channel1 (N must be integer)  
api/playlist/channel2?songs=N => returns last N songs played on channel1 (N must be integer)
``` 

GET endpoints for artists:
```
api/artists => return all artists for both channels  
api/artists/channel1 => return all artists played on channel1  
api/artists/channel2 => return all artists played on channel2
``` 

GET endpoint for albums:  
```    
api/albums/<artist_name> => return all albums of particular artist with channel where they are played on  
```