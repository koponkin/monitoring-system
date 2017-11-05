function renderPostgres(period) {
    $.get('/db/monitor', {period: period}, function (data) {
        var tableContent = "";
        data.forEach(function(item, i, arr) {
            tableContent += makePostgresTable(item);
        });

        var tableHtml = "";
        if(tableContent === "") {
            tableHtml = "<p>Empty result!</p>"
        }else {
            tableHtml = "<table cellspacing=2 border=1 cellpadding=5>" +
                makePostgresHeader() +
                tableContent +
                "</table>"
        }

        $("#postgres_block").html(
            makePostgresBlockLabel() +
            tableHtml)
    });
}

function makePostgresBlockLabel() {
        return "<div>" +
            "<label>DB service : </label>" +
            "<label>Postgres</label>" +
            "</div>";
}

function makePostgresHeader() {
    return "<tr>" +
        "<th>date</th>" +
        "<th>connection_count</th>" +
        "<th>cpu</th>" +
        "<th>ram</th>" +
        "<th>status</th>" +
        "<th>error_text</th>" +
        "</tr>";
}

function makePostgresTable(rowData) {
    return "<tr>" +
            "<td>" + rowData.date + "</td>" +
            "<td>" + rowData.connection_count + "</td>" +
            "<td>" + rowData.cpu + "</td>" +
            "<td>" + rowData.ram + "</td>" +
            "<td>" + rowData.status + "</td>" +
            "<td>" + rowData.error_text + "</td>" +
            "</tr>";
}