$(document).ready(function() {
    draw_current_kernel_extensions();

    // Click handlers
    $('#kernel-menu-item').click(function() {
        draw_current_kernel_extensions();
    });
});

function draw_current_kernel_extensions() {
    $('#loading').show();

    $.post(API_BASE + 'getkernerext', function(data) {
        $('#loading').hide();
        $('#kernel-title').show();

        for(var i = 0; i < data.length; i++) {
            if(data[i]['dirpath']) {
                draw_data(data[i]);
            }
        }
    });
}

function draw_data(data) {
    var string = '<tr><td style="width: 200px">' +
                    '<span>Directory Path</span>' +
                 '</td><td>' +
                    data['dirpath'] +
                 '</td></tr>' +
                 '<tr><td>' +
                    '<span>File Path</span>' +
                 '</td><td>' +
                    data['filepath'] +
                 '</td></tr>' +
                 '<tr><td>' +
                    '<span>Last Path Modification</span>' +
                 '</td><td>' +
                    data['lastpathmod'] +
                 '</td></tr>' +
                 '<tr><td>' +
                    '<span>Last Metadata Modification</span>' +
                 '</td><td>' +
                    data['lastmetamod'] +
                 '</td></tr>' +
                 '<tr><td style="height: 20px;background-color:white"></td></tr>';

    $('#kernel-data-table').append(string);
}