// tsnePlotAnimated.js
// Requires tsne-js via: <script src="static/lib/tsne.umd.js"></script>

function createTSNEAnimatedPlot(data, target, features, perplexity = 15, clusterCount = 4) {
    d3.select(target).html("");

    const width = 505;
    const height = 330;
    const margin = { top: 20, right: 20, bottom: 30, left: 40 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;
    const clusterLabels = ["Calm", "Energetic", "Melancholic", "Upbeat", "Aggressive", "Dreamy", "Lively", "Serene"];

    const mentalColor = d3.scaleOrdinal()
    .domain(["Low Anxiety", "Moderate Anxiety", "High Anxiety"])
    .range(["#1f77b4", "#ff7f0e", "#d62728"]);
    
    const svg = d3.select(target).append("svg")
        .attr("width", width)
        .attr("height", height);

    const g = svg.append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    const tip = d3.tip()
    .attr("class", "d3-tip")
    .offset([-10, 0])
    .html(function (d) {
        return `<strong>Anxiety Group:</strong> <span class='details'>${d.anxiety_group}</span><br>` +
               `<strong>Genre:</strong> <span class='details'>${d.genre}</span><br>` +
               `<strong>Country:</strong> <span class='details'>${d.country}</span>`;
    });

    svg.call(tip);

    const vectors = data.map(d => features.map(f => +d[`norm_${f}`]));

    const tsne = new tsnejs.tSNE({ dim: 2, perplexity: perplexity, epsilon: 10 });
    tsne.initDataRaw(vectors);

    const positions = new Array(data.length).fill().map(() => ({ x: 0, y: 0 }));

    const clusterColor = d3.scaleOrdinal(d3.schemeCategory10);

    let labelGroup = g.append("g");

    function assignClusters(Y, k = clusterCount) {
        // Basic k-means clustering
        let centroids = Y.slice(0, k);
        let clusters = new Array(Y.length);
        let changed = true;

        for (let iter = 0; iter < 10 && changed; iter++) {
            changed = false;

            // Assign points to nearest centroid
            for (let i = 0; i < Y.length; i++) {
                let minDist = Infinity, minIndex = 0;
                for (let j = 0; j < k; j++) {
                    const dx = Y[i][0] - centroids[j][0];
                    const dy = Y[i][1] - centroids[j][1];
                    const dist = dx * dx + dy * dy;
                    if (dist < minDist) {
                        minDist = dist;
                        minIndex = j;
                    }
                }
                if (clusters[i] !== minIndex) changed = true;
                clusters[i] = minIndex;
            }

            // Recalculate centroids
            const newCentroids = new Array(k).fill().map(() => [0, 0]);
            const counts = new Array(k).fill(0);
            for (let i = 0; i < Y.length; i++) {
                newCentroids[clusters[i]][0] += Y[i][0];
                newCentroids[clusters[i]][1] += Y[i][1];
                counts[clusters[i]]++;
            }
            for (let j = 0; j < k; j++) {
                if (counts[j] > 0) {
                    newCentroids[j][0] /= counts[j];
                    newCentroids[j][1] /= counts[j];
                }
            }
            centroids = newCentroids;
        }

        return { clusters, centroids };
    }

    let nodes = g.selectAll("circle")
    .data(data)
    .enter()
    .append("circle")
    .attr("r", 5)
    .attr("opacity", 0.8)
    .attr("fill", d => mentalColor(d.anxiety_group))
    .on("mouseover", function (event, d) {
        tip.show.call(this, event, d);
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

    function updatePlot() {
        tsne.step();
        const Y = tsne.getSolution();

        const xExtent = d3.extent(Y, d => d[0]);
        const yExtent = d3.extent(Y, d => d[1]);

        const x = d3.scaleLinear().domain(xExtent).range([0, innerWidth]);
        const y = d3.scaleLinear().domain(yExtent).range([innerHeight, 0]);

        // Assign clusters and centroids
        const { clusters, centroids } = assignClusters(Y, clusterCount);
        clusters.forEach((cluster, i) => {
            data[i].cluster = cluster;
        });

        Y.forEach((coord, i) => {
            positions[i].x += 0.2 * (x(coord[0]) - positions[i].x);
            positions[i].y += 0.2 * (y(coord[1]) - positions[i].y);
        });

        nodes
            .attr("transform", (d, i) => `translate(${positions[i].x},${positions[i].y})`)
            .attr("fill", (d, i) => clusterColor(d.cluster));

        // Draw cluster labels
        labelGroup.raise().selectAll("text").remove();
        centroids.forEach((centroid, i) => {
            labelGroup.append("text")
                .attr("x", x(centroid[0]))
                .attr("y", y(centroid[1]))
                .attr("text-anchor", "middle")
                .attr("dy", "-0.6em")
                .attr("fill", "white")
                .attr("font-size", "12px")
                .attr("font-weight", "bold")
                .text(clusterLabels[i % clusterLabels.length]);
        });

        requestAnimationFrame(updatePlot);
    }

    updatePlot();
}

function attachPerplexitySlider(sliderId, data, target, features, colorBy = "genre") {
    const slider = document.getElementById(sliderId);
    const label = document.getElementById("perplexityValue");
    slider.addEventListener("input", () => {
        const perplexity = parseInt(slider.value);
        label.textContent = perplexity;
        createTSNEAnimatedPlot(data, target, features, colorBy, perplexity);
    });
}