"use strict";

$(document).ready(function () {
    $("td > .popup").on('click', function(e) {
        e.preventDefault();
        var url = $(this).attr('href');

        $.get(url).success(function (e) {
            $('#viewing-modal-title').text(e['title']);
            $('#modal-content').html(e['html']);
            $('#viewing-modal').modal('show');
        });
    });
});
