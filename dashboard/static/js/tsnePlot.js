function createTSNEPlot(data, target) {
    d3.select(target).html("");

    const width = 500;
    const height = 340;

    const svg = d3.select(target).append("svg")
        .attr("width", width)
        .attr("height", height);

    const margin = { top: 20, right: 20, bottom: 30, left: 40 },
          innerWidth = width - margin.left - margin.right,
          innerHeight = height - margin.top - margin.bottom;

    const x = d3.scaleLinear()
        .domain(d3.extent(data, d => d.tsne_x)).nice()
        .range([0, innerWidth]);

    const y = d3.scaleLinear()
        .domain(d3.extent(data, d => d.tsne_y)).nice()
        .range([innerHeight, 0]);

    const color = d3.scaleOrdinal(d3.schemeCategory10);

    const g = svg.append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    const tooltip = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("position", "absolute")
        .style("background", "#333")
        .style("color", "white")
        .style("padding", "5px")
        .style("border-radius", "5px")
        .style("pointer-events", "none")
        .style("display", "none");

    g.selectAll("circle")
        .data(data)
        .enter().append("circle")
        .attr("cx", d => x(d.tsne_x))
        .attr("cy", d => y(d.tsne_y))
        .attr("r", 4)
        .attr("opacity", 0.5)
        .attr("fill", d => color(d.genre))
        .on("mouseover", (event, d) => {
            tooltip.style("display", "block")
                .html(`<strong>Genre:</strong> ${d.genre}<br><strong>Country:</strong> ${d.country}`);
        })
        .on("mousemove", (event) => {
            tooltip.style("top", (event.pageY + 10) + "px")
                   .style("left", (event.pageX + 10) + "px");
        })
        .on("mouseout", () => {
            tooltip.style("display", "none");
        });

    g.append("g")
        .attr("transform", `translate(0,${innerHeight})`)
        .call(d3.axisBottom(x));

    g.append("g")
        .call(d3.axisLeft(y));
}
