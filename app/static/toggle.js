$( document ).ready(function() {
   $(".dropdown").click(function() {
        $(this).toggleClass("open");
        if (this.className == "dropdown open") {
            $("#themes").attr("aria-expanded", "true");
        } else {
            $("#themes").attr("aria-expanded", "false");
        };
   });
});