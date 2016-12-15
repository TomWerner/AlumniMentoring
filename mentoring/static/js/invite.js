"use strict";

$(document).ready(function () {
    $('#preview_email').on('click', function (e) {
        e.preventDefault();
        var url = "/honorsAdmin/preview_invite?" + $('#invite_form').serialize();

        $.get(url).success(function (e) {
            $('#viewing-modal-title').text(e['title']);

            if (e['modal_footer']) {
                var footer = $('.modal-footer');
                footer.html(e['modal_footer']);
                footer.show()
            } else
                $('.modal-footer').hide();

            $('#modal-content').html(e['html']);
            $('#viewing-modal').modal('show');


            if (e['modal_width']) {
                $('.modal-dialog').width(e['modal_width']);
            } else {
                $('.modal-dialog').width(600);
            }
        });
    });
});
