let is_playing = false;
const audio = document.getElementById("player");
const listen_now_txt = document.getElementById("bt-txt")
const listen_now_icon = document.getElementById("bt-icon")

function toggle_play() {
  if (!is_playing) {
    audio.play();
    listen_now_txt.innerHTML = "stop now";
    listen_now_icon.className = "fas fa-volume-mute player-button-icon";
  } else {
    audio.pause();
    listen_now_txt.innerHTML = "listen now";
    listen_now_icon.className = "fa fa-volume-up player-button-icon";
    audio.currentTime = 0;
  }
};

audio.onplaying = function () {
  is_playing = true;
};

audio.onpause = function () {
  is_playing = false;
};
