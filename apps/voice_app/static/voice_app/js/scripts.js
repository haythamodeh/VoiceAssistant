$(document).ready(function() {
    var playback = document.getElementById("playback");
    // var last_thing_said = document.getElementById("last_thing_said")
    // console.log("sam this was the last thing said")
    // console.log(last_thing_said.innerHTML)
    playback.play()
})

$(document).ready(function () {
    if (navigator.appVersion.indexOf("Win") !=-1){
        $("#loading-content").css("margin", "-85px 0 0 -85px"); //for windows
    }
    else{
        $("#loading-content").css("margin", "-85px 0 0 -119px"); //for mac/linux88
    }
    $('#micbtn_web').click(function(){
        console.log('web mic on')
        $("#loading-wrapper").css("display", "block");
        $("#blur").css("filter", "blur(8px)");
        $("#loading-wrapper").css("z-index", "10");
        window.SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
        let finalTranscript = '';
        let recognition = new window.SpeechRecognition();
        recognition.interimResults = true;
        recognition.maxAlternatives = 10;
        recognition.continuous = true;
        recognition.onresult = (event) => {
            let interimTranscript = '';
            for (let i = event.resultIndex, len = event.results.length; i < len; i++) {
            let transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript;
            } else {
                interimTranscript += transcript;
            }
            }
            console.log(finalTranscript)
            // document.querySelector('#phrase').innerHTML = finalTranscript + interimTranscript;

            const url = '/voice' 
            const web_voice_data = {
                web_voice_phrase: finalTranscript,
            }

            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            var csrftoken = getCookie('csrftoken');
            function csrfSafeMethod(method) {
                // these HTTP methods do not require CSRF protection
                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            }
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });

            $.post(url,web_voice_data,function(data, status){
                console.log(`${status}`)
                console.log("final trasn text")
                console.log(finalTranscript)
                console.log("final trans leng")
                console.log(finalTranscript.length)        
                if (finalTranscript.length > 0){
                    location.reload()
                }
            })

        }
        recognition.start();
    });
});

$(document).ready(function (e) {

    $('body').keyup(function (e) {
        if (e.keyCode == 32) {
            $("#micbtn").click();
        }
    });

});

$(document).ready(function () {
    $("#about_wrapper").css("display", "none");
    
    $("#micbtn").click(function () {
        $("#loading-wrapper").css("display", "block");
        $("#blur").css("filter", "blur(8px)");
        $("#loading-wrapper").css("z-index", "10");

    });
    var display = false;
    $(".skills").click(function(){
        display = !display
        if (display)
            if($("#commands_wrapper").hasClass("bounceOutRight")){
                $("#commands_wrapper").removeClass("bounceOutRight");
            }
            else{
                $("#commands_wrapper").css("display" , "inline");
            }
        else
            $("#commands_wrapper").addClass("bounceOutRight");
    });

    $(".close").click(function()
    {   
        if ( $("#about_wrapper").hasClass("fadeIn") ){
            $("#about_wrapper").removeClass("fadeIn");
        }
        $("#about_wrapper").addClass("fadeOut");
        $("#blur").css("filter", "blur(0px)");
    });

    $(".about").click(function()
    {
        if ( $("#about_wrapper").hasClass("fadeOut") ){
            $("#about_wrapper").removeClass("fadeOut");
        }
        $("#about_wrapper").addClass("fadeIn");
        $("#about_wrapper").css("display", "block");
        $("#about_wrapper").css("z-index", "20");
        $("#blur").css("filter", "blur(8px)");
    });

});

$(document).ready(function () {
    var chart_data = document.getElementById("data_for_viz_radar").innerHTML.split(",")
    // console.log("Sam")
    // console.log(chart_data)
    // console.log(chart_labels)
    var ctx = document.getElementById("chartjs-2").getContext('2d');
    Chart.defaults.scale.gridLines.color = "rgba(255,255,255,0.5)";
    Chart.defaults.scale.gridLines.zeroLineColor = "rgba(255,255,255,0.5)";
    Chart.defaults.scale.angleLines= { color: "rgba(255,255,255,0.5)" };
    var myChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: [
                'Housing',
                'Cost of Living',
                'Healthcare',
                'Education',
                'Environmental Quality',
                'Economy',
                'Outdoors',
                'Commute',
            ],
            datasets: [
                {
                    label: "Score out of 10",
                    fill: true,
                    backgroundColor: "rgba(255,205,86,0.2)",
                    borderColor: "rgba(255,205,86,1)",
                    pointBorderColor: "#fff",
                    pointBackgroundColor: "rgba(179,181,198,1)",
                    data: chart_data,
                    pointBorderColor: 'turquoise',
                    pointBackgroundColor: 'turquoise',
                    pointRadius: 5,
                }
            ]
        },
        options: {
            title: {
                display: false,
                text: 'Scores are out of 10'
            },
            scale: {
                pointLabels: {
                    fontColor: '#fff',
                    fontSize: 18,
                }
            }
        }
    });
});

$(document).ready(function () {
    var chart_data = document.getElementById("data_for_viz").innerHTML.split(",")
    var chart_labels = document.getElementById("label_for_viz").innerHTML.split(",")
    // console.log("Sam")
    // console.log(chart_data)
    // console.log(chart_labels)
    var ctx = document.getElementById("chartjs-1").getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: chart_labels,
            datasets: [{
                label: 'AQI Score',
                data: chart_data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(205,175,149, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)'
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(205,175,149,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        fontColor: 'white',
                        beginAtZero:false
                    }
                }],
                xAxes: [{
                    ticks: {
                        fontColor: 'white',
                        fontSize: 12
                    }
                }]
            }
        }
    });
});