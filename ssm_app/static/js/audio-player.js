var player = $('.player'),
    audio = player.find('audio'),
    duration = $('.duration'),
    currentTime = $('.current-time'),
    progressBar = $('.progress span'),
    mouseDown = false,
    rewind, showCurrentTime;

function secsToMins(time) {
    var int = Math.floor(time),
        mins = Math.floor(int / 60),
        secs = int % 60,
        newTime = mins + ':' + ('0' + secs).slice(-2);

    return newTime;
}

function getCurrentTime() {
    var currentTimeFormatted = secsToMins(audio[0].currentTime),
        currentTimePercentage = audio[0].currentTime / audio[0].duration * 100;

    currentTime.text(currentTimeFormatted);
    progressBar.css('width', currentTimePercentage + '%');

    if (player.hasClass('playing')) {
        showCurrentTime = requestAnimationFrame(getCurrentTime);
    } else {
        cancelAnimationFrame(showCurrentTime);
    }
}

audio.on('loadedmetadata', function () {
    var durationFormatted = secsToMins(audio[0].duration);
    duration.text(durationFormatted);
}).on('ended', function () {
    if ($('.repeat').hasClass('active')) {
        audio[0].currentTime = 0;
        audio[0].play();
    } else {
        player.removeClass('playing').addClass('paused');
        audio[0].currentTime = 0;
    }
});

var songPlaying = null;

function fastForward() {
    let nextId = (parseInt(songPlaying) + 1);
    play(nextId.toString());
}

function previous() {
    let nextId = (parseInt(songPlaying) - 1);
    if (nextId >= 0)
        play(nextId.toString());
}

function play(idAudioTag) {
    let audioTag = document.getElementById(idAudioTag);
    if (audioTag !== null) {
        songPlaying = idAudioTag;
        let self = $('#play_button');
        let mainAudioTag = document.getElementById('main_audio_tag');
        mainAudioTag.pause();
        // console.log(mainAudioTag);
        // console.log(audioTag);
        // console.log(mainAudioTag.src);
        // console.log(audioTag.src);
        mainAudioTag.src = audioTag.src;
        mainAudioTag.play();
        if (self.hasClass('play-pause') && player.hasClass('paused')) {
            player.removeClass('paused').addClass('playing');
            getCurrentTime();
        }
    }
}


function pause(idPlayButton, idAudioTag) {

    let self = $(idPlayButton);
    let audioTag = $(idAudioTag);
    if (self.hasClass('play-pause') && player.hasClass('playing')) {
        player.removeClass('playing').addClass('paused');
        audioTag.pause();
    }
}

function playPause() {
    console.log('playPause...');
    var self = $(this);
    let playButton = $('#play_button');
    let audioTag = document.getElementById('main_audio_tag');
    //todo: add src
    if (self.hasClass('play-pause') && player.hasClass('paused')) {
        player.removeClass('paused').addClass('playing');
        // playButton.play();
        audioTag.play();

        getCurrentTime();
    } else if (self.hasClass('play-pause') && player.hasClass('playing')) {
        player.removeClass('playing').addClass('paused');
        // playButton.pause();
        audioTag.pause();
    }

    if (self.hasClass('shuffle') || self.hasClass('repeat')) {
        self.toggleClass('active');
    }
}

$('button').on('click', playPause).on('mousedown', function () {
    var self = $(this);

    if (self.hasClass('ff')) {
        player.addClass('ffing');
        audio[0].playbackRate = 2;
    }

    if (self.hasClass('rw')) {
        player.addClass('rwing');
        rewind = setInterval(function () {
            audio[0].currentTime -= .3;
        }, 100);
    }
}).on('mouseup', function () {
    var self = $(this);

    if (self.hasClass('ff')) {
        player.removeClass('ffing');
        audio[0].playbackRate = 1;
    }

    if (self.hasClass('rw')) {
        player.removeClass('rwing');
        clearInterval(rewind);
    }
});

player.on('mousedown mouseup', function () {
    mouseDown = !mouseDown;
});

progressBar.parent().on('click mousemove', function (e) {
    var self = $(this),
        totalWidth = self.width(),
        offsetX = e.offsetX,
        offsetPercentage = offsetX / totalWidth;

    if (mouseDown || e.type === 'click') {
        audio[0].currentTime = audio[0].duration * offsetPercentage;
        if (player.hasClass('paused')) {
            progressBar.css('width', offsetPercentage * 100 + '%');
        }
    }
});
