function resetDashboard() {
    const selected_metric = "anxiety";
    $("#musicattr").val(selected_metric);

    // World map data
    $.ajax({
        type: "POST",
        url: "/api/country",
        contentType: "application/json",
        data: JSON.stringify({ metric: selected_metric }),
        success: function (response) {
            createChoropleth(response, selected_metric);
        },
        error: function (err) {
            console.log(err);
        }
    });

    // Parallel Coordinates
    $.ajax({
        type: "POST",
        url: "/api/pcp",
        contentType: "application/json",
        data: JSON.stringify({}),
        success: function (response) {
            plot_pcp(response);
        },
        error: function (err) {
            console.log(err);
        }
    });

    // Word Cloud
    $.ajax({
        type: "POST",
        url: "/api/wordcloud",
        contentType: "application/json",
        data: JSON.stringify({}),
        success: function (response) {
            createWordCloud(response);
        },
        error: function (err) {
            console.log(err);
        }
    });

    // MCA Plot
    $.ajax({
        type: "POST",
        url: "/api/mca",
        contentType: "application/json",
        data: JSON.stringify({}),
        success: function (response) {
            plotMCA(response);
        },
        error: function (err) {
            console.log(err);
        }
    });

    // Cluster Summary
    $.ajax({
        type: "POST",
        url: "/api/cluster",
        contentType: "application/json",
        data: JSON.stringify({}),
        success: function (response) {
            plotStats(response);
        },
        error: function (err) {
            console.log(err);
        }
    });
}

$(document).ready(function () {

    $('#resetAll').click(resetDashboard);

    $('#musicattr').on('change', function () {
        const selected_metric = $(this).val();

        $.ajax({
            type: "POST",
            url: "/api/country",
            contentType: "application/json",
            data: JSON.stringify({ metric: selected_metric }),
            dataType: "json",
            success: function (response) {
                createChoropleth(response, selected_metric);
            },
            error: function (err) {
                console.log(err);
            }
        });
    });

    resetDashboard();
});