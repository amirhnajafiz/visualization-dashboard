import { useEffect, useRef } from 'react';
import * as d3 from 'd3';

function BarChart({ data }) {
  const ref = useRef();

  useEffect(() => {
    // preprocess data to calculate the count of each genre
    const genreCounts = d3.rollups(
      data,
      (v) => v.length,
      (d) => d.genre
    ).map(([genre, count]) => ({ genre, count }));

    const svg = d3.select(ref.current);
    svg.selectAll("*").remove(); // clear previous chart

    const width = 400;
    const height = 150;
    const margin = { top: 0, right: 0, bottom: 30, left: 30 };

    svg.attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom);

    const chart = svg.append("g")
      .attr("transform", `translate(${margin.left}, ${margin.top})`);

    const x = d3.scaleBand()
      .domain(genreCounts.map((d) => d.genre))
      .range([0, width])
      .padding(0.1);

    const y = d3.scaleLinear()
      .domain([0, d3.max(genreCounts, (d) => d.count)])
      .range([height, 0]);

    // add axes
    const xAxis = d3.axisBottom(x);
    const yAxis = d3.axisLeft(y);

    chart.append("g")
      .attr("transform", `translate(0, ${height})`)
      .call(xAxis)
      .selectAll("text")
      .style("fill", "white"); // Set x-axis text color to white

    chart.append("g")
      .call(yAxis)
      .selectAll("text")
      .style("fill", "white"); // Set y-axis text color to white

    chart.selectAll(".domain, .tick line")
      .style("stroke", "white"); // Set axis path and tick color to white

    // Draw bars
    chart.selectAll("rect")
      .data(genreCounts)
      .enter()
      .append("rect")
      .attr("x", (d) => x(d.genre))
      .attr("y", (d) => y(d.count))
      .attr("width", x.bandwidth())
      .attr("height", (d) => height - y(d.count))
      .attr("fill", "steelblue");
  }, [data]);

  return <svg ref={ref}></svg>;
}

export default BarChart;
