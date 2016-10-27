$(document).ready(function() {
	$.getJSON('/counts', function(sets) {

		// draw venn diagram
		var div = d3.select("#venn");
				
		// d3.select("#venn").append('div')
  //               .classed("svg-container", true)
  //               .append('svg')
  //               .attr("preserveAspectRatio", "xMinYMin meet")
  //               //NEED TO CHANGE VIEWBOX HERE IF YOU CHANGE DIMENSIONS
  //               .attr("viewBox", "0 0 1000 ")
  //               .classed("svg-content-responsive", true);

		div.datum(sets).call(venn.VennDiagram());

		//no captions
		d3.selectAll("#venn text").text('');

		// add a tooltip
		var tooltip = d3.select("body").append("div")
		    .attr("class", "venntooltip");

		// add listeners to all the groups to display tooltip on mouseover
		div.selectAll("g")
		    .on("mouseover", function(d, i) {
		        // sort all the areas relative to the current item
		        venn.sortAreas(div, d);

		        // Display a tooltip with the current size
		        tooltip.transition().duration(400).style("opacity", .9);
		        tooltip.text(d.sets + ': ' + d.size );

		        // highlight the current path
		        var selection = d3.select(this).transition("tooltip").duration(400);
		        selection.select("path")
		            .style("stroke-width", 3)
		            .style("fill-opacity", d.sets.length == 1 ? .4 : .1)
		            .style("stroke-opacity", 1);
		    })

		    .on("mousemove", function() {
		        tooltip.style("left", (d3.event.pageX) + "px")
		               .style("top", (d3.event.pageY - 28) + "px");
		    })

		    .on("mouseout", function(d, i) {
		        tooltip.transition().duration(400).style("opacity", 0);
		        var selection = d3.select(this).transition("tooltip").duration(400);
		        selection.select("path")
		            .style("stroke-width", 0)
		            .style("fill-opacity", d.sets.length == 1 ? .25 : .0)
		            .style("stroke-opacity", 0);
		    });
	})
})

