$(document).ready(function (e) {
    console.log("hello");

    $('body').keyup(function (e) {
        if (e.keyCode == 32) {
            $("#micbtn").click();
        }
    });

});

$(document).ready(function () {
    
    
    $("#micbtn").click(function () {
        $("#loading-wrapper").css("display", "block");
        $("#blur").css("filter", "blur(8px)");
        $("#loading-wrapper").css("z-index", "10");
        
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
                        beginAtZero:false
                    }
                }]
            }
        }
    });
});