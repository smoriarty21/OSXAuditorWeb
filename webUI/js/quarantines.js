$(document).ready(function() {
    $('#loading-string').show();
    get_quarantines();
});

function get_quarantines() {
    $.post(API_BASE + 'getquarantines', function(data) {
        $('#quarantines-table').html('');

        for(var i = 0; i < data.length; i++) {
            $('#quarantines-table').append('<tr><td>' + data[i] + '</td></tr>');
        }

        $('#loading-string').hide();
        $('#quarantines-title').show();
    });
}