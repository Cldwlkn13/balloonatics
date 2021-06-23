$(document).ready(function() {
    var currIndex = -1;
    var initial = true;
    manageSlides();

    function manageSlides() {
      $('.slideshow-container').each(function(e){
        showSlides($(this), e);
      });
      setTimeout(manageSlides, 10000); 
      initial = false;
    }

    function showSlides(container, e) {
      var slides = $(container).find(".slides");
      var visibleSlides = $(container).find('.slides:visible');
      if(visibleSlides.length > 0) {
        slide = $(visibleSlides)[0];
        currIndex = $(slide).attr('id').split('-')[2];
      }
      if(currIndex >= 0) {
        var id = `#slide-${e}-${currIndex}`
        $(id).fadeOut(500);
      }
      currIndex++;
      if (currIndex > (slides.length - 1)) {
        currIndex = 0;
      }
      var id = `#slide-${e}-0`
      if(!initial){
        id = `#slide-${e}-${currIndex}`
      }
      $(id).fadeIn(2000);
    }
})