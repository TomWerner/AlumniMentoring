"use strict";

$(document).ready(function () {
    var box = document.querySelector('.carouselbox');
    var next = $('#next');
    var prev = $('#prev');
    var items = box.querySelectorAll('.content li');
    var counter = 0;
    var amount = items.length;
    var current = items[0];
    box.classList.add('active');
    function navigate(direction) {
        current.classList.remove('current');
        counter = counter + direction;
        if (direction === -1 &&
            counter < 0) {
            counter = amount - 1;
        }
        if (direction === 1 && !items[counter]) {
            counter = 0;
        }
        current = items[counter];
        current.classList.add('current');
        if (counter == 0)
            prev.attr('disabled', 'disabled');
        else
            prev.removeAttr('disabled');
        if (counter == amount - 1)
            next.attr('disabled', 'disabled');
        else
            next.removeAttr('disabled');

        var mentee_id = $('li.current >> .mentee_id').val();
        $.get('/honorsAdmin/mentee/' + mentee_id + '/getallmatcheslist').success(function (e) {
            $("#mentor_list").html(e);
            setup_popups();
        });
    }

    next.on('click', function (ev) {
        navigate(1);
    });
    prev.on('click', function (ev) {
        navigate(-1);
    });
    navigate(0);
    console.log()
    if ($(window).height() < $('.affix').find('li').height() + 300) {
        var card = $('.affix').find('li').find('.card');
        card.height($(window).height() - 222);
        card.css('overflow-y', 'auto');
        // $('.affix').find('li').height($(window).height() - 300);
    }
});
