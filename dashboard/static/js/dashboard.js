function resetDashboard() {
    selected_countries = []
    maxPCPCountry = 0;
    worldmap_country = "world"
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
            console.log("Error:", err);
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

    // Cluster Summary
    // $.ajax({
    //     type: "POST",
    //     url: "/api/cluster",
    //     contentType: "application/json",
    //     data: JSON.stringify({}),
    //     success: function (response) {
    //         plotStats(response);
    //     },
    //     error: function (err) {
    //         console.log(err);
    //     }
    // });

    //Correlogram
    $.ajax({
        type: "POST",
        url: "/api/correlation",
        contentType: "application/json",
        data: JSON.stringify({}),
        success: function (response) {
            createCorrelogram(response);
        },
        error: function (err) {
            console.log(err);
        }
    });

    //Stacked Barchart
    $.ajax({
        type: "POST",
        url: "/api/stackedbar",
        contentType: "application/json",
        data: JSON.stringify({
            mental_health_metric: "anxiety",
            countries: []
        }),
        dataType: "json",
        success: function(response) {
            createStackedBar(response);
        },
        error: function(err) {
            console.log("Error loading stacked bar chart:", err);
        }
    });
    
}

$(document).ready(function () {

    $('#resetAll').click(resetDashboard);

    $('#musicattr').on('change', function () {
        const selected_metric = $(this).val();
        selected_attr = selected_metric
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

    $("#mentalFeatureSelector").on("change", function() {
        const selectedFeature = $(this).val();
        $.ajax({
            type: "POST",
            url: "/api/stackedbar",
            contentType: "application/json",
            data: JSON.stringify({
                mental_health_metric: selectedFeature,
                countries: selected_countries
            }),
            dataType: "json",
            success: function(response) {
                createStackedBar(response);
            },
            error: function(err) {
                console.log("Error updating stacked bar:", err);
            }
        });
    });

    resetDashboard();
});