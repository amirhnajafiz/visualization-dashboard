function createCorrelogram(correlationData) {
  document.getElementById("correlogram").innerHTML = "";

  var margin = { top: 25, right: 80, bottom: 25, left: 25 },
    width = 500 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

  var domain = d3.set(correlationData.map((d) => d.x)).values();
  var num = Math.sqrt(correlationData.length);

  var color = d3
    .scaleLinear()
    .domain([-1, 0, 1])
    .range(["#B22222", "#fff", "#000080"]);

  var x = d3.scalePoint().range([0, width]).domain(domain);

  var y = d3.scalePoint().range([0, height]).domain(domain);

  var xSpace = x.range()[1] - x.range()[0] + 40;
  var ySpace = y.range()[1] - y.range()[0] + 40;

  var svg = d3
    .select("#correlogram")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var cor = svg
    .selectAll(".cor")
    .data(correlationData)
    .enter()
    .append("g")
    .attr("class", "cor")
    .attr("transform", function (d) {
      return "translate(" + x(d.x) + "," + y(d.y) + ")";
    });

  cor
    .filter(function (d) {
      return d.x !== d.y;
    })
    .append("rect")
    .attr("width", xSpace / 10)
    .attr("height", ySpace / 10)
    .attr("x", -xSpace / 20)
    .attr("y", -ySpace / 20)
    .style("fill", "none")
    .style("stroke", "lightgray");

  cor
    .filter(function (d) {
      var ypos = domain.indexOf(d.y);
      var xpos = domain.indexOf(d.x);
      for (var i = ypos + 1; i < num; i++) {
        if (i === xpos) return false;
      }
      return true;
    })
    .append("text")
    .attr("x", function (d) {
      return d.x === d.y ? -20 : -15;
    })
    .attr("y", 5)
    .attr("font-size", "12px")
    .attr("font-weight", "bold")
    // .attr("transform", function(d) {
    //     if (d.x === d.y) {
    //         return "rotate(45)";
    //     } else {
    //         return null;
    //     }
    // })
    .text(function (d) {
      return d.x === d.y ? d.x : d.value.toFixed(2);
    })
    .style("fill", function (d) {
      if (d.value === 1) {
        return "#000";
      } else {
        return color(d.value);
      }
    });

  cor
    .filter(function (d) {
      var ypos = domain.indexOf(d.y);
      var xpos = domain.indexOf(d.x);
      for (var i = ypos + 1; i < num; i++) {
        if (i === xpos) return true;
      }
      return false;
    })
    .append("circle")
    .attr("r", function (d) {
      return (width / (num * 2)) * (Math.abs(d.value) + 0.1);
    })
    .style("fill", function (d) {
      if (d.value === 1) {
        return "#000";
      } else {
        return color(d.value);
      }
    });

  // Color legend (gradient bar)
  var aS = d3
    .scaleLinear()
    .range([-margin.top + 5, height + margin.bottom - 5])
    .domain([1, -1]);

  var yA = d3.axisRight().scale(aS).tickPadding(7);

  var aG = svg
    .append("g")
    .attr("class", "y axis")
    .attr("transform", "translate(" + (width + margin.right / 2) + ",0)")
    .call(yA);

  var iR = d3.range(-1, 1.01, 0.01);
  var h = height / iR.length + 3;

  iR.forEach(function (d) {
    aG.append("rect")
      .style("fill", color(d))
      .style("stroke-width", 0)
      .attr("height", h)
      .attr("width", 10)
      .attr("x", 0)
      .attr("y", aS(d));
  });
}
