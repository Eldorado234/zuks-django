$(function () {
    $('.nav-tabs a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
    });

    $('.navbar-nav a').click(function (e) {
        if(!$(this).parent('li').hasClass('active')) {
            $(this).parent('li').addClass('active');
        }

        $(this).parent('li').siblings('.active').removeClass('active');
    });

    $('.header .navbar-nav a').smoothScroll();

    $('#jump2top').css('bottom', '-100px');
    $(window).scroll(function () {
        var btn = $('#jump2top');
        if ($(this).scrollTop() > 100) {
            btn.stop().animate({ 'bottom': '0' }, 200);
        } else {
            btn.stop().animate({ 'bottom': '-100px' }, 200);
        }
    });

    $('#jump2top').smoothScroll();

    $('#contactform').ajaxForm(function(returnVal) {
        $('#contactform').html($(returnVal).html());
    });

    $('#newsletterform').ajaxForm(function(returnVal) {
        $('#newsletterform').html($(returnVal).html());
    });
});
