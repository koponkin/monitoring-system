function renderPingdom(period) {
    $.get('/pingdom/monitor', {period: period}, function (data) {
        var pingdomHtml = "";
        data.forEach(function(item, i, arr) {
            pingdomHtml += makePingdomServiceBlock(item);
        });
        $("#pingdom_block").html(pingdomHtml)
    });
}


function makePingdomServiceBlock(data) {
    return "<div class='floatLeft'>" +
    makePingdomBlockLabel(data.service_name) +
    makePingdomTable(data.results) +
    "</div>";
}

function makePingdomBlockLabel(service_name) {
        return "<div>" +
            "<label>Pingdom service : </label>" +
            "<label>" + service_name + "</label>" +
            "</div>";
}

function makePingdomTable(results) {

    var tableHeader = "<table cellspacing=2 border=1 cellpadding=5>" +
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
    if(tableHtml === ""){
        tableHtml = "<p>Empty result!</p>"
    }
    return tableHtml;
}