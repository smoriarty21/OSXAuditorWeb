$(document).ready(function() {
    draw_installed_apps();
});

function draw_installed_apps() {
    $('#loading-string').show();

    get_installed_apps(fill_table);
}

function get_installed_apps(callback) {
    $.post(API_BASE + 'getapplications', function(data) {
        if(data) {
            callback(data);
        }
    });
}

function fill_table(data) {
    $('#installed-apps-table').html('');

    for(var i = 0; i < data.length; i++) {
        if(data[i]['dirpath']) {
            var table_data = '<tr><td>' +
                                'Application Path:' +
                             '</td><td>' +
                                data[i]['dirpath'] +
                             '</td></tr>' +
                             '<tr><td>' +
                                'File Path:' +
                             '</td><td>' +
                                data[i]['filepath'] +
                             '</td></tr>' +
                             '<tr><td>' +
                                'Hash:' +
                             '</td><td>' +
                                data[i]['hash'] +
                             '</td></tr>' +
                             '<tr><td>' +
                                'Last Metadata Modification:' +
                             '</td><td>' +
                                data[i]['lastmetamod'] +
                             '</td></tr>' +
                             '<tr><td>' +
                                'Last Path Modification' +
                             '</td><td>' +
                                data[i]['lastpathmod'] +
                             '</td></tr>' +
                             '<tr><td style="height: 20px;background-color:white"></td></tr>';

            $('#installed-apps-table').append(table_data);

            $('#installed-apps-table').show(table_data);
            $('#loading-string').hide();
        }
    }
}