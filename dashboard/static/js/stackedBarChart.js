function createStackedBar(data) {
    d3.select("#stackedbar").html(""); // Clear previous content

    var svg = d3.select("#stackedbar").append("svg")
        .attr("width", 450)
        .attr("height", 300),
        margin = { top: 20, right: 20, bottom: 30, left: 50 },
        width = +svg.attr("width") - margin.left - margin.right - 50,
        height = +svg.attr("height") - margin.top - margin.bottom,
        g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var x = d3.scaleBand()
        .rangeRound([0, 250])
        .paddingInner(0.05)
        .align(0.1);

    var y = d3.scaleLinear()
        .rangeRound([height, 0]);

    // Color palette
    var colorRange = [
        "#40E0D0",
        "#FFD700",
        "#FF6347",
        "#6A5ACD",
        "#3CB371",
        "#FF69B4",
        "#9370DB",
        "#FF4500",
        "#FF8C00",
        "#BA55D3",
        "#32CD32",
        "#00FA9A",
        "#DC143C",
        "#DA70D6"
    ];
    var z = d3.scaleOrdinal(colorRange);

    // Extract genre keys, excluding 'health_bucket'
    var keys = Object.keys(data[0]).filter(function (d) { return d !== "health_bucket"; });

    // Compute total counts for each row
    data.forEach(function (d) {
        let t = 0;
        keys.forEach(function (k) { t += d[k] = +d[k]; });
        d.total = t;
    });

    // Calculate total counts per genre key
    var genreTotals = keys.map(function (key) {
        return {
            key: key,
            total: d3.sum(data, function (d) { return d[key]; })
        };
    });

    // Sort genres by total counts ascending
    genreTotals.sort(function (a, b) { return a.total - b.total; });

    // Update keys to be sorted according to genreTotals
    keys = genreTotals.map(function (d) { return d.key; });

    x.domain(data.map(function (d) { return d.health_bucket; }));
    y.domain([0, d3.max(data, function (d) { return d.total; })]).nice();
    z.domain(keys);

    var stackGroup = g.append("g")
        .selectAll("g")
        .data(d3.stack().keys(keys)(data))
        .enter().append("g")
        .attr("fill", function (d) { return z(d.key); });

    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function (event, d) {
            var genre = d3.select(this.parentNode).datum().key;
            var originalData = d3.select(this).datum().data;
            var count = originalData ? originalData[genre] : 0;

            return "<strong>Genre:</strong> <span class='details'>" + genre +
                "<br></span><strong>Count:</strong> <span class='details'>" +
                count + "</span>";
        });

    svg.call(tip);

    stackGroup.selectAll("rect")
        .data(function (d) { return d; })
        .enter().append("rect")
        .attr("x", function (d) { return x(d.data.health_bucket); })
        .attr("y", function (d) { return y(d[1]); })
        .attr("height", function (d) { return y(d[0]) - y(d[1]); })
        .attr("width", x.bandwidth())
        .on("mouseover", function (event, d) {
            tip.show.call(this, event, d); // important: .call(this, event, d)
            d3.select(this)
                .attr("stroke", "white")
                .attr("stroke-width", 2);
        })
        .on("mouseout", function (event, d) {
            tip.hide.call(this, event, d);
            d3.select(this)
                .attr("stroke", null)
                .attr("stroke-width", null);
        });

    // Add x-axis at the bottom
    g.append("g")
        .attr("class", "axis")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    // Add y-axis with labels
    g.append("g")
        .attr("class", "axis")
        .call(d3.axisLeft(y).ticks(null, "s"))
        .append("text")
        .attr("x", -32)
        .attr("y", y(y.ticks().pop()) - 14)
        .attr("dy", "0.32em")
        .attr("fill", "#000")
        .attr("font-weight", "bold")
        .attr("text-anchor", "start")
        .text("Count");

    var legend = g.append("g")
        .attr("font-family", "sans-serif")
        .attr("font-size", 10)
        .attr("text-anchor", "end")
        .selectAll("g")
        .data(keys.slice().reverse())
        .enter().append("g")
        .attr("transform", function (d, i) { return "translate(0," + i * 20 + ")"; });

    legend.append("rect")
        .attr("x", width + 20)
        .attr("y", 15)
        .attr("width", 19)
        .attr("height", 19)
        .attr("fill", z);

    legend.append("text")
        .attr("x", width + 16)
        .attr("y", 9.5 + 15)
        .attr("dy", "0.32em")
        .attr("font-weight", "bold")
        .attr("fill", "white")
        .text(function (d) { return d; });
}

// // Interaction triggers:
// worldMapTrigger.registerListener(function(countryID) {
//     currentCountries = countryID === "world" ? [] : [countryID];
//     fetchStackedBarChart(currentMetric, currentCountries);
// });

// pcpTrigger.registerListener(function(selectedCountryIDs) {
//     currentCountries = selectedCountryIDs;
//     fetchStackedBarChart(currentMetric, currentCountries);
// });

// // Dropdown change (you should create a dropdown manually)
// $("#stackedBarDropdown").on("change", function() {
//     currentMetric = $(this).val();
//     fetchStackedBarChart(currentMetric, currentCountries);
// });

// // Initial fetch
// fetchStackedBarChart(currentMetric, currentCountries);
