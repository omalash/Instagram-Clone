$(document).ready(function() {

    $("#create-post").click(function(e) {
        e.preventDefault(); 
        $(".create-post-content").show();
    });

    setTimeout(function() {
        $(".message").fadeOut();
    }, 5000);

    $(".search").click(function(e) {
        e.preventDefault();
        $(".search-bar").show();
    });
    
    $("#search-input").keypress(function(event) {
        if (event.which === 13) {
            event.preventDefault();
            $(".search-bar form").submit();
        }
    });

});