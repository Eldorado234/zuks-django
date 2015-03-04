$(function () {
    $('.header .navbar-nav a').smoothScroll();

    function activate(navbarItem) {
      navbarItem.addClass('active').siblings('li').removeClass('active');
    }

    $('.navbar-nav a').click(function() {
      var navbarItem = $(this).parent();
      activate(navbarItem);
    });

    $('#contactform').ajaxForm(function(returnVal) {
        $('#contactform').html($(returnVal).html());
    });

    $('#newsletterform').ajaxForm(function(returnVal) {
        $('#newsletterform').html($(returnVal).html());
    });

    $('ul.navbar-nav').onePageNav({
        currentClass: 'active',
        changeHash: false,
        scrollSpeed: 750,
        scrollThreshold: 0.5,
        filter: '',
        easing: 'swing'
    });
});
