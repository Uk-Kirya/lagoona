$(".phone__mask").mask("+7 (999) 999 - 99 - 99");

(function () {
    'use strict'
    var forms = document.querySelectorAll('.needs-validation')

    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }

                form.classList.add('was-validated')
            }, false)
        })
})()


$(document).ready(function () {
    var owl = $('.photos');
    owl.owlCarousel({
        margin: 0,
        nav: false,
        dots: true,
        autoHeight: true,
        loop: true,
        items: 1
    });
})


$(document).ready(function () {
    var owl = $('.slider');
    owl.owlCarousel({
        margin: 0,
        nav: true,
        dots: false,
        autoHeight: true,
        loop: true,
        items: 1
    });
})


$(document).ready(function () {
    var owl = $('.popular');
    owl.owlCarousel({
        margin: 24,
        nav: true,
        dots: false,
        autoHeight: true,
        loop: true,
        responsive: {
            0: {
              items: 2
            },
            576: {
              items: 2
            },
            768: {
              items: 3
            },
            1200: {
              items: 4
            }
          }
    });
})


$(document).ready(function () {
    $("a.topLink").click(function () {
        $("html, body").animate({
            scrollTop: $($(this).attr("href")).offset().top + "px"
        }, {
            duration: 0,
            easing: "swing"
        });
        return false;
    });
});


$(function () {
    $(window).scroll(function () {
        var top = $(document).scrollTop();
        if (top > 40) $('.head').addClass('head_fixed');
        else $('.head').removeClass('head_fixed');
    });
});


$(document).ready(function() {
    var img1 = $('.img1'),
        img2 = $('.img2'),
        img3 = $('.img3'),
        img4 = $('.img4'),
        lastPosition = 0
    $(window).scroll(function() {
        var position = $(window).scrollTop()
        var top = -position / 3,
            top2 = -position / 7,
            top3 = -position / 5,
            itop = top,
            itop2 = top2
        itop3 = top3
        if (position > lastPosition) {
            TweenLite.to(img1, 1, { y: top / 2 })
            TweenLite.to(img2, 1, { y: top2 / 2 })
            TweenLite.to(img3, 1, { y: top / 1 })
            TweenLite.to(img4, 1, { y: top3 })
        } else {
            TweenLite.to(img1, 1, { y: itop / 2 })
            TweenLite.to(img2, 1, { y: itop2 / 2 })
            TweenLite.to(img3, 1, { y: itop3 / 2 })
            TweenLite.to(img4, 1, { y: itop3 })
        }
        lastPosition = position
    })
})


AOS.init({
    duration: 1500,
    offset: 0,
    once: false
});