$( document ).ready(function() {
   $(".rsvp").click(function(e) {
        e.preventDefault();
        var url = $(this).attr('href');
        var that = $(this);
        $.ajax({
            url: url,
            method: "POST",
            success: function( data ) {
                $('.empty').html('');
                if ( data.volunteering === "yes") {
                    $(that).html("<img src='/static/bold_checkmark_edited.png' style='max-height: 25px'/>");
                    $(that).parent().parent().find('.volunteer_qty').html(data.volunteers_needed);
                } else {
                    $(that).html("RSVP");
                    if ( data.event_full === true) {
                        $('.empty').html('<h4>Sorry, no more volunteers are needed for this event.</h4>')
                        $('.empty').css('text-align', 'center')
                    }
                    $(that).parent().parent().find('.volunteer_qty').html(data.volunteers_needed);
                }
            },
            error: function (xhr, status) {
                alert("Sorry, there was a problem!");
            }
        });
   });
})