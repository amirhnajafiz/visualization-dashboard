function createWordCloud(data) {
    // console.log(data);

    // Clear existing wordcloud
    document.getElementById("wordcloud").innerHTML = "";

    const outerWidth = 390;
    const outerHeight = 500;
    const margin = { top: 10, right: 10, bottom: 10, left: 10 };
    const innerWidth = outerWidth - margin.left - margin.right;
    const innerHeight = outerHeight - margin.top - margin.bottom;
    

    const color = d3.scaleOrdinal(d3.schemeSet2);

    const wordScale = d3.scaleLinear()
        .domain(d3.extent(data, d => +d.count))
        .range([15, 70]);

    const svg = d3.select("#wordcloud")
        .append("svg")
        .attr("width", outerWidth)
        .attr("height", outerHeight)
        .attr("viewBox", `0 0 ${outerWidth} ${outerHeight}`)
        .attr("preserveAspectRatio", "xMidYMid meet")
        .append("g")
        .attr("transform", `translate(${outerWidth / 2}, ${outerHeight / 2})`);

    const layout = d3.layout.cloud()
        .size([innerWidth, innerHeight])
        .words(data.map(d => ({ text: d.genre, size: wordScale(+d.count) })))
        .padding(4)
        .rotate(() => 0)
        .font("Segoe UI")
        .fontSize(d => d.size)
        .on("end", draw);

    layout.start();

    function draw(words) {
        svg.selectAll("text")
            .data(words)
            .enter().append("text")
            .style("font-size", d => `${d.size}px`)
            .style("font-family", "Segoe UI, sans-serif")
            .style("font-weight", "600")
            .style("fill", (d, i) => color(i))
            .attr("text-anchor", "middle")
            .attr("transform", d => `translate(${d.x},${d.y})rotate(${d.rotate})`)
            .text(d => d.text);
    }
}
