(function() {

    //Handling login
    $('#loginForm').on('submit', function(event) {
    	event.preventDefault();
    	$.post("/imgup/login/", $(this).serialize())
        .done(function() {
        	location.reload();
        })
        .fail(function() {
        	$("#logError").show();
        })
    });

    //Handling logout
    $('#logOutButton').on('click', function() {
        $.get("/imgup/logout/").done(function() {
            location.replace("/imgup/");
        })
    });

    //Toggling login form on low resolutions
    $('#toggleLogin').on('click', function() {
        $("#loginForm").toggle();
        $("#toggleLoginShow").toggle();
        $("#toggleLoginHide").toggle();
    });

}) ()