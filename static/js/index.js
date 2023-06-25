$(document).ready(function() {

    $("#create-post").click(function(e) {
        e.preventDefault(); 
        $(".create-post-content").show();
    });

    setTimeout(function() {
        $(".message").fadeOut();
    }, 5000);
    
});