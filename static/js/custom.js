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

    $('#button-send').submit(function() {
        return false;
    });

    //setup email here
    $('#button-send').click(function(event) {
        $('#button-send').html('Sending E-Mail...');
        event.preventDefault();

        $.ajax({
            type: 'POST',
            url: 'send_form_email.php',
            data: $('#contactform').serialize(),
            contentType: 'application/x-www-form-urlencoded',
            success: function (html) {
                $('#contactform .success').hide();
                $('#contactform .error').hide();
                if (html.success == '1') {
                    $('#contactform #button-send').html('Nachricht senden');
                    $('#contactform .success').show();
                }
                else {
                    $('#contactform #button-send').html('Nachricht senden');
                    $('#contactform .error').show();
                }
            },
            error: function () {
                $('#contactform #button-send').html('Nachricht senden');
                $('#contactform .error').show();
            }
        });
    });

    var defaultError = 'Die Anfrage konnte leider nicht bearbeitet werden. Versuchen Sie es sp&auml;ter erneut.';

    // newsletter feedback
    $('.submit-newsletter').on('click', function(e) {
        e.preventDefault();
        
        $.ajax({
            type: 'POST',
            url: 'newsletter.php?subscribe=1',
            data: $('#newsletterform').serialize(),
            contentType: 'application/x-www-form-urlencoded',
            success: function(e) {
                $('#newsletterform .success').hide();
                $('#newsletterform .error').hide();
                if(e.status == true) {
                    $('#newsletterform .success').html(e.msg);
                    $('#newsletterform .success').show();
                } else {
                    $('#newsletterform .error').html(e.msg);
                    $('#newsletterform .error').show();
                }
            }, 
            error: function() {
                alert("error");
                $('#newsletterform .success').hide();
                $('#newsletterform .error').html(defaultError);
                $('#newsletterform .error').show();
            }
        });
    });
});

function scrollTo(elem) {
   /* $('body,html').animate({
        scrollTop: elem.offset().top
    }, 500);*/
}

function valemail(email) {
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}