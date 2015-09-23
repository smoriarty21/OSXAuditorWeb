$(document).ready(function() {
    show_header_info();

    // Click handlers
    $('#header-menu-item').click(function() {
        show_header_info();
    });
});

function show_header_info() {
    //Show loading text
    $('#loading').show();

    // Reset table data
    $('#header-data-table').html('');

    // Pull fresh header info
    get_header_data();
}

function get_header_data() {
    $.post(API_BASE + 'getheader', function(data) {
        // Hide loading
        $('#loading').hide();
        
        // Show title
        $('#header-title').show();

        if(data) {
            create_header_table(data);
        }
    });
}

function create_header_table(data) {
    draw_data(data['description']);
    draw_data(data['system_version']);
    draw_data(data['audit_path']);
    draw_data(data['timezone']);

}

function draw_data(data) {
    $('#header-data-table').append('<tr><td><span class="glyphicon glyphicon-wrench" aria-hidden="true"></span></td><td>' + data + '</td></tr>');
}