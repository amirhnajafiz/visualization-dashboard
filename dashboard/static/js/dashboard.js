function resetDashboard() {
    selected_countries = []
    maxPCPCountry = 0;
    worldmap_country = "world"
    const selected_metric = "anxiety";
    $("#mapMentalFeatureSelector").val(selected_metric);
    $("#mentalFeatureSelector").val(selected_metric);

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

    // Correlogram
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

    // Stacked Barchart
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

    // t-SNE
    $.ajax({
        url: "/api/tsne",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            features: ["valence", "energy", "danceability", "tempo"],
            countries: []
        }),
        success: function(response) {
            createTSNEAnimatedPlot(response, "#tsnePlot", ["valence", "energy", "danceability", "tempo"]);
        },
        error: function(xhr, status, error) {
            console.error("Error fetching t-SNE data:", error);
        }
    });
    
}

$(document).ready(function () {

    $('#resetAll').click(resetDashboard);

    $("#mapMentalFeatureSelector").on("change", function() {
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
                countries: selected_countries.length === 0 ? clicked_countries : selected_countries
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

    $("#perplexitySlider").on("input", function () {
        const perplexity = +this.value;
        $("#perplexityValue").text(perplexity);
    
        // Re-fetch data or re-run t-SNE locally
        $.ajax({
            url: "/api/tsne",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                features: ["valence", "energy", "danceability", "tempo"],
            }),
            success: function (response) {
                d3.select("#tsnePlot").html(""); // Clear old plot
                createTSNEAnimatedPlot(response, "#tsnePlot", ["valence", "energy", "danceability", "tempo"], perplexity);
            }
        });
    });

    resetDashboard();
});