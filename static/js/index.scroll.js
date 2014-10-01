$(function () {
    $(window).scroll(function () {
        if($(this).scrollTop() < 250) {
             $('.navbar-collapse .navbar-nav a').parent('li').siblings('.active').removeClass('active');
             $('.navbar-collapse .navbar-nav a').parent('li:eq(0)').addClass('active');

             $('.navbar-responsive-collapse .navbar-nav a').parent('li').siblings('.active').removeClass('active');
             $('.navbar-responsive-collapse .navbar-nav a').parent('li:eq(0)').addClass('active');
        } else if($(this).scrollTop() < $('#idee').offset().top + 250) {
             $('.navbar-collapse .navbar-nav a').parent('li').siblings('.active').removeClass('active');
             $('.navbar-collapse .navbar-nav a').parent('li:eq(1)').addClass('active');

             $('.navbar-responsive-collapse .navbar-nav a').parent('li').siblings('.active').removeClass('active');
             $('.navbar-responsive-collapse .navbar-nav a').parent('li:eq(1)').addClass('active');
        } else if($(this).scrollTop() < $('#team').offset().top + 250) {
             $('.navbar-collapse .navbar-nav a').parent('li').siblings('.active').removeClass('active');
             $('.navbar-collapse .navbar-nav a').parent('li:eq(2)').addClass('active');

             $('.navbar-responsive-collapse .navbar-nav a').parent('li').siblings('.active').removeClass('active');
             $('.navbar-responsive-collapse .navbar-nav a').parent('li:eq(2)').addClass('active');
        } else if($(this).scrollTop() < $('#motivation').offset().top) {
             $('.navbar-collapse .navbar-nav a').parent('li').siblings('.active').removeClass('active');
             $('.navbar-collapse .navbar-nav a').parent('li:eq(3)').addClass('active');

             $('.navbar-responsive-collapse .navbar-nav a').parent('li').siblings('.active').removeClass('active');
             $('.navbar-responsive-collapse .navbar-nav a').parent('li:eq(3)').addClass('active');
        } else if($(this).scrollTop() < $('#kontakt').offset().top) {
             $('.navbar-collapse .navbar-nav a').parent('li').siblings('.active').removeClass('active');
             $('.navbar-collapse .navbar-nav a').parent('li:eq(4)').addClass('active');

             $('.navbar-responsive-collapse .navbar-nav a').parent('li').siblings('.active').removeClass('active');
             $('.navbar-responsive-collapse .navbar-nav a').parent('li:eq(4)').addClass('active');
        }
    });
});