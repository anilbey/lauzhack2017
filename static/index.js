var width = 960,
  height = 500;

var svg = d3.select("svg")

// tip
var tip = d3.tip()
  .attr('class', 'd3-tip')
  .offset([-10, 0])
  .html(function (d) {
    return `<span>${d.amount} ${d.currency}</span></br></br> <em>on ${d.date} at ${d.time}</em>`;
  });

// colors
var colors = ["black", "red", "orange", "yellow", "green"]

var force = d3.layout.force()
  .size([width, height]);

// init tip
svg.call(tip);

/**
 * 
 * @param {target, source, group} links 
 */
function initGraph(links) {

  var nodesByName = {};

  // process links and create nodes
  links.forEach(function (link) {
    link.currency = link.currency === 'None' ? 'CHF' : link.currency;
    link.source = nodeByName(link.source);
    link.target = nodeByName(link.target);
  });

  // Extract the array of nodes from the map by name.
  var nodes = d3.values(nodesByName);

  // Create the link lines.
  var linkEls = svg.selectAll(".link")
    .data(links)
    .enter().append("line")
    .attr("class", "link")
    .attr("stroke", function (d) { return colors[d.group] })
    .on('mouseover', tip.show)
    .on('mouseout', tip.hide);

  // Create the node circles.
  var nodeEls = svg.selectAll(".node")
    .data(nodes)
    .enter().append("circle")
    .attr("class", "node")
    .attr("r", 4.5)
    .call(force.drag);

  // Start the force layout.
  force
    .nodes(nodes)
    .links(links)
    .on("tick", tick)
    .start();

  function tick() {
    linkEls.attr("x1", function (d) { return d.source.x; })
      .attr("y1", function (d) { return d.source.y; })
      .attr("x2", function (d) { return d.target.x; })
      .attr("y2", function (d) { return d.target.y; });

    nodeEls.attr("cx", function (d) { return d.x; })
      .attr("cy", function (d) { return d.y; });
  }

  function nodeByName(name, ) {
    return nodesByName[name] || (nodesByName[name] = { name: name });
  }
}

function onSearch() {
  var firstClient = document.getElementById('first-client-input').value;
  var secondClient = document.getElementById('second-client-input').value;
  var transactionCount = document.getElementById('transaction-count-input').value;
  fetch(`./search?first_client=${firstClient}&second_client=${secondClient}&transaction_count=${transactionCount}`)
    .then(res => res.json())
    .then(body => initGraph(body));
}
