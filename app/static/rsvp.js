$( document ).ready(function() {
   $(".rsvp").click(function(e) {
        e.preventDefault();
        var url = $(this).attr('href');
        var that = $(this);
        console.log(url);
        $.ajax({
            url: url,
            method: "POST",
            success: function( data ) {
                if ( data.volunteering === 1) {
                    $(that).html("<img src='/static/bold_checkmark_edited.png' style='max-height: 25px'/>");
                } else {
                    $(that).html("RSVP");
                }
            },
            error: function (xhr, status) {
                alert("Sorry, there was a problem!");
            }
        });
   });
})