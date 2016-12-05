
$(document).ready(function () {
    setup_popups = function() {
        $(".popup").on('click', function (e) {
            e.preventDefault();
            var url = $(this).attr('href');

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
    };
    setup_popups();
});
