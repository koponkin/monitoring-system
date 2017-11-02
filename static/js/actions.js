function renderPingdomTable(results) {

    var tableHeader = "<table>" +
        "<tr>" +
        "<th>date</th>" +
        "<th>responsetime</th>" +
        "<th>status</th>" +
        "<th>statusdesc</th>" +
        "</tr>";
    var tableContent = "";

    for (i = 0; i < results.length; i++) {
        var rowData = results[i];
        tableContent = tableContent + "<tr>" +
            "<td>" + rowData.date + "</td>" +
            "<td>" + rowData.responsetime + "</td>" +
            "<td>" + rowData.status + "</td>" +
            "<td>" + rowData.statusdesc + "</td>" +
            "</tr>";
    }
    var tableFooter = "</table>";


    var tableHtml = tableHeader + tableContent + tableFooter;
    if(tableHtml == ""){
        tableHtml = "<p>Empty result!</p>"
    }
    $("#pingdom_table").html(tableHtml);
}

function onTimeChange(curentValue) {
    $.get('/pingdom/monitor', {period: curentValue}, function (data) {
        $("#pingdom_service_name").html(data.service_name);
        renderPingdomTable(data.results);
    });
}