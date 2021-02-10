function main() {
    $('.movies__item').hover(function() {
        $(this).find('.movies__item-image').css({"filter": "brightness(20%)"});
        $(this).find('.movies__item-star').toggleClass('hide');
        $(this).find('.movies__item-rating').toggleClass('hide');
        $(this).find('.movies__item-expander').toggleClass('hide');
        $(this).find('.movies__item-title').toggleClass('hide');
    }, function() {
        $(this).find('.movies__item-image').css({"filter": "brightness(100%)"});
        $(this).find('.movies__item-star').toggleClass('hide');
        $(this).find('.movies__item-rating').toggleClass('hide');
        $(this).find('.movies__item-expander').toggleClass('hide');
        $(this).find('.movies__item-title').toggleClass('hide');
    });
}

$(document).ready(main());

//$("p").hover(function(){
//  $(this).css("background-color", "yellow");
//  }, function(){
//  $(this).css("background-color", "pink");
//});