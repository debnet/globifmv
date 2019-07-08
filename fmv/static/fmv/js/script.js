
function onYouTubeIframeAPIReady() {
    let player = new YT.Player('player');
    player.addEventListener("onStateChange", function(event) {
        if (event.data === 0) {
            player.pauseVideo();
            player.seekTo(player.getDuration() - 0.1);
            $('#modal').modal({
                backdrop: 'static',
                keyboard: false,
            });
        }
    });
}
