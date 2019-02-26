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
    });
});