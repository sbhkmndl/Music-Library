//status bar
var status_bar=document.getElementById('play-control-bar');
var music_current_status = document.getElementById("play-status-bar");
var music_handler = document.getElementById("paly-handeler");

//Volume status bar
var volume_status_bar = document.getElementById("volume-control-status");
var volume_current_status = document.getElementById("volume-control-status-current");
var volume_handler = document.getElementById("volume-control-handler");

//Songs source and album image

//select buttons

//play control
var prev_button = document.getElementById("button-prev");
var next_button = document.getElementById("button-next");
var play_button = document.getElementById("button-play");
//volume control
var volume_up_button = document.getElementById("volume-up");
var volume_down_button = document.getElementById("volume-down");
var volume_mute_button = document.getElementById("volume-mute");
//song details music-artist   music-album
var musicTitle = document.querySelector("#music-name a");
var musicArtist = document.querySelector("#music-artist a");
var musicAlbum = document.querySelector("#music-album a");

//select time change elment
var play_musis_status =  document.getElementById("play-time");
var total_music_status = document.getElementById("total-time");
//create song object
var music = new Audio();
var currentMusic = 0; 

//Play music
window.onload = playMusic;

function playMusic(){
    if(musics[currentMusic]) {
        music.src = musics[currentMusic];
    }
    if(Titles[currentMusic]) {
        musicTitle.textContent = Titles[currentMusic];
        $("#music-name a").attr("href", Music_play_link[currentMusic]);
    }
    if(Artists[currentMusic]) {
        musicArtist.textContent = Artists[currentMusic];
        $("#music-artist a").attr("href", Music_play_artist[currentMusic]);
    }
    if(Albums[currentMusic]) {
        musicAlbum.textContent = Albums[currentMusic];
        $("#music-album a").attr("href", music_play_album[currentMusic]);
    }
    if(posters[currentMusic]) {
        $("#music-img img").attr("src", posters[currentMusic]);
    }

    //playlist add link
    $(".link-add-playlist").each(function() {
   var $this = $(this);
   var _href = $this.attr("href").match("^(.*[\\\/])")[1];
   $this.attr("href", _href + music_id[currentMusic]);
    });

    music.play();
    $("#button-play img").attr("src",pause_button_img);
    vol_position_update();
}

//play and pause music
play_button.addEventListener("click",PlayPause);
function PlayPause(){
    if(music.paused){
        music.play();
        $("#button-play img").attr("src",pause_button_img);
    }
    else{
        music.pause();
        $("#button-play img").attr("src",play_button_img);
    }
}

//display status
music.addEventListener('timeupdate',function(){
   var position = music.currentTime / music.duration;
    music_current_status.style.width = position * 100 + '%';
    music_handler.style.left = position * 100 + '%';
    showCurrentStatus(Math.round(music.currentTime));
    if(isNaN(music.duration)){
        total_music_status.textContent = "00:00"
    }
    else{
        showTotalTime(Math.round(music.duration));
    }
    if(music.ended){
        if(currentMusic<musics.length-1){
            next();
        }  
    }
});

//Time Update
function showCurrentStatus(seconds){
    var minute = Math.floor(seconds/60);
    var sec = seconds%60;
    
    minute = (minute<10)? "0" + minute : minute;
    sec = (sec<10)? "0" + sec : sec;
    play_musis_status.textContent = minute + ":" + sec;
}
function showTotalTime(seconds){
    var minute = Math.floor(seconds/60);
    var sec = seconds%60;
    
    minute = (minute<10)? "0"+minute : minute;
    sec = (sec<10)? "0"+sec : sec;
    total_music_status.textContent = minute + ":" + sec;
}
//music change
next_button.addEventListener("click",next);
function next(){
    currentMusic++;
    if(currentMusic > musics.length-1){
        currentMusic = 0;
    }
    playMusic();
    $("#button-play img").attr("src",pause_button_img);
    // $("#music-img img").attr("src",posters[currentMusic]);
}

prev_button.addEventListener("click",prev);
function prev(){
    currentMusic--;
    if(currentMusic < 0){
        currentMusic =  musics.length-1;
    }
    playMusic();
    $("#button-play img").attr("src",pause_button_img);
    // $("#music-img img").attr("src",posters[currentMusic]);
}

//progress bar click change
$("#play-control-bar").bind("change", function() {
            music.currentTime = $(this).val();
        });
status_bar.addEventListener("click",seek);
 function seek(e) {
    var percent = e.offsetX / this.offsetWidth;
    console.log(e.offsetX)
     console.log(this.offsetWidth)
     console.log(music.duration)
     music.currentTime = percent * music.duration;
}


//volume change
volume_up_button.addEventListener("click",volumeIncrease);
function volumeIncrease(){
    if(music.volume<1){
        if(music.volume>0.90){
            music.volume = 1;
        }
        else{
            music.volume += 0.10;
        }
        vol_position_update();
    }
    
}
volume_down_button.addEventListener("click",volumeDecrease);
function volumeDecrease(){
    if(music.volume>0){
        if(music.volume < 0.10){
            music.volume = 0;
        }
        else{
            music.volume -= 0.10;
        }
        vol_position_update();
        
    }
}
volume_mute_button.addEventListener("click",volumeMute);
var stor_volume=0.00;
function volumeMute(){
    if(music.volume != 0.00){
        stor_volume = music.volume;
        music.volume = 0.00;
        $("#volume-mute img").attr("src",mute_button_img);
        vol_position_update();
    }
    else{
        music.volume = stor_volume;
        $("#volume-mute img").attr("src",volume_button_img);
        vol_position_update();
    }
    
}

//Volume Handle
volume_status_bar.addEventListener("click",volumeControl);
 function volumeControl(e) {
    var vol_position = e.offsetX / this.offsetWidth;
    music.volume = vol_position;
    vol_position_update();
}
function vol_position_update()
{
    volume_current_status.style.width = music.volume * 100 + '%';
    volume_handler.style.left = music.volume * 100 + '%';
}
