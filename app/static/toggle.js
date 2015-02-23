$( document ).ready(function() {
   $(".dropdown").hover(function() {
        $(this).toggleClass("open");
        if (this.className == "dropdown open") {
            $("#themes").attr("aria-expanded", "true");
        } else {
            $("#themes").attr("aria-expanded", "false");
        }
   });
   $(".navbar-toggle").click(function() {
       var element = $(".navbar-mobile")[0];
       $(element).toggleClass("show");
   });
});