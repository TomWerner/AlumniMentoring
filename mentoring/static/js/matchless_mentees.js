"use strict";

$(document).ready(function () {
    var mentee_id = $('#mentee_id').val();

    $.get('/honorsAdmin/mentee/' + mentee_id + '/getallmatcheslist').success(function (e) {
        $("#mentor_list").html(e);
    });
});
