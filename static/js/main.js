const socket = new Socket(`${window.location.protocol}//${window.location.hostname}:${window.location.port}`);
var isLoading = false;

$(document).ready(function () {
    const interBubble = $(".interactive")
    const inputBox = $("#input-prompt")
    var audio_data = null;

    let curX = 0
    let curY = 0
    let tgX = 0
    let tgY = 0

    function move() {
        curX += (tgX - curX) / 20
        curY += (tgY - curY) / 20
        interBubble.css("transform", `translate(${Math.round(curX)}px, ${Math.round(curY)}px)`)
        requestAnimationFrame(move)
    }

    $(document).click(function() {
        $(".settings-panel").hide();
    });
    
    $(".settings-panel").click(function(event) {
        event.stopPropagation();
    })

    $(".settings-btn").click(function(event) {
        event.stopPropagation();
        $(".settings-panel").show();
    });    

    $("#audio-file").change(function() {
        var audioFile = this.files[0];
        getData(audioFile, function(data) {
            audio_data = data;
            console.log(data);
        });
    });

    $(document).keypress(function (e) {
        if (e.which == 13) {
            var value = inputBox.val();
            if (value.replace(/\s/g, '')) {
                if (!isLoading) {
                    isLoading = true;
                    $(".audio-result").animate({ height: 0 }, 1000).css({ display: "none" });
                    $('.result').children().not('span').remove();
                    $("#prograss-rate").show();
                    $("#modelName").val()

                    socket.send({
                        "op": "generateMusic",
                        "prompt": [value],
                        "model":  audio_data === null ? $("#modelName").val() : "melody",
                        "top_k": $("#top_k").val(),
                        "top_p": $("#top_p").val(),
                        "duration": $("#duration").val(),
                        "audioData": audio_data
                    });

                    socket.addMessageListener("message", (msg) => handleMessage(msg));
                    socket.addMessageListener("audio_data", (data) => updateAudioSource(data));
                    $(".audio-result").css({ display: "flex" }).animate({ height: 200 }, 1000);
                }
            } else {
                $(".text-input").addClass("shake");
                setTimeout(function () { $(".text-input").removeClass("shake"); }, 1000);
            }
        }
    });

    $(window).on("mousemove", function (event) {
        tgX = event.clientX + 530
        tgY = event.clientY + 200
    });

    move()
});

function getData(audioFile, callback) {
    var reader = new FileReader();
    reader.onload = function(event) {
        var data = event.target.result;
        var base64Data = data.split(",")[1];
        callback(base64Data);        
    };
    reader.readAsDataURL(audioFile);
}

function updateAudioSource(data) {
    var audioPlayer = document.getElementById('audioPlayer');
    var base64 = 'data:audio/mp3;base64,' + data.audio_data;
    audioPlayer.src = base64

    const wavesurfer = WaveSurfer.create({
        container: ".result",
        waveColor: 'violet',
        progressColor: 'purple',
        height: "100%",
        width: "1000px",
        media: audioPlayer
    });

    $("#prograss-rate").hide();
    wavesurfer.load(base64);
    socket.disconnect();
    isLoading = false;
}

function handleMessage(msg) {
    console.log(msg);
    $("#prograss-rate").text(msg.generated)
}