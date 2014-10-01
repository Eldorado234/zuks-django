$(function () {
    $(window).scroll(function () {
        if($(this).scrollTop() < 20) {
             $('.navbar-collapse .navbar-nav a').parent('li').siblings('.active').removeClass('active');
             $('.navbar-collapse .navbar-nav a').parent('li:eq(1)').addClass('active');

             $('.navbar-responsive-collapse .navbar-nav a').parent('li').siblings('.active').removeClass('active');
             $('.navbar-responsive-collapse .navbar-nav a').parent('li:eq(1)').addClass('active');
        } else if($(this).scrollTop() < $('#haftungsausschluss').offset().top + 200) {
             $('.navbar-collapse .navbar-nav a').parent('li').siblings('.active').removeClass('active');
             $('.navbar-collapse .navbar-nav a').parent('li:eq(2)').addClass('active');

             $('.navbar-responsive-collapse .navbar-nav a').parent('li').siblings('.active').removeClass('active');
             $('.navbar-responsive-collapse .navbar-nav a').parent('li:eq(2)').addClass('active');
        } else if($(this).scrollTop() < $('#datenschutz').offset().top + 200) {
             $('.navbar-collapse .navbar-nav a').parent('li').siblings('.active').removeClass('active');
             $('.navbar-collapse .navbar-nav a').parent('li:eq(3)').addClass('active');

             $('.navbar-responsive-collapse .navbar-nav a').parent('li').siblings('.active').removeClass('active');
             $('.navbar-responsive-collapse .navbar-nav a').parent('li:eq(3)').addClass('active');
        } 
    });
});