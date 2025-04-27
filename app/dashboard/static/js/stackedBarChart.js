function createStackedBar(data, target) {
    d3.select("#stackedbar").html("");  // clear before redraw

    const margin = { top: 30, right: 100, bottom: 50, left: 60 },
          width = 700 - margin.left - margin.right,
          height = 400 - margin.top - margin.bottom;

    const svg = d3.select("#stackedbar")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    // Parse data
    const genres = data.map(d => d.genre);
    const scores = data.map(d => d.score);

    const x = d3.scaleBand()
        .domain(genres)
        .range([0, width])
        .padding(0.2);

    const y = d3.scaleLinear()
        .domain([0, d3.max(scores)])
        .nice()
        .range([height, 0]);

    const color = d3.scaleOrdinal()
        .domain(genres)
        .range(d3.schemeSet3);

    // Bars
    svg.append("g")
        .selectAll("rect")
        .data(data)
        .enter()
        .append("rect")
        .attr("x", d => x(d.genre))
        .attr("y", d => y(d.score))
        .attr("width", x.bandwidth())
        .attr("height", d => height - y(d.score))
        .attr("fill", d => color(d.genre));

    // X Axis
    svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x))
        .selectAll("text")
        .attr("transform", "rotate(-45)")
        .style("text-anchor", "end")
        .style("font-size", "11px");

    // Y Axis
    svg.append("g")
        .call(d3.axisLeft(y).ticks(6))
        .append("text")
        .attr("fill", "#000")
        .attr("x", -40)
        .attr("y", -10)
        .attr("text-anchor", "start")
        .text(target.charAt(0).toUpperCase() + target.slice(1));

    // Legend
    const legend = svg.append("g")
        .attr("font-family", "sans-serif")
        .attr("font-size", 10)
        .attr("text-anchor", "end")
        .selectAll("g")
        .data(genres)
        .enter().append("g")
        .attr("transform", (d, i) => `translate(0,${i * 20})`);

    legend.append("rect")
        .attr("x", width + 40)
        .attr("width", 19)
        .attr("height", 19)
        .attr("fill", d => color(d));

    legend.append("text")
        .attr("x", width + 35)
        .attr("y", 9.5)
        .attr("dy", "0.32em")
        .text(d => d);
}
