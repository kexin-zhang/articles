var data = [];
for (var prop in all_articles) {
	var d = new Date(prop);
	d.setTime( d.getTime() + d.getTimezoneOffset()*60*1000 );
	data.push({'date': d, 'value': all_articles[prop] != null ? all_articles[prop].length : 0 });
}

MG.data_graphic({
    data: data,
    full_width: true,
    height: 500,
    width: 900,
    target: '#chart',
    top: 15,
    x_accessor: 'date',
    y_accessor: 'value',
    color: '#82b1ff',
    mouseover: function(d, i) {
    // custom format the rollover text, show days
    d3.select('#custom-rollover svg .mg-active-datapoint')
        .text(d.date + ': ' + d.value);

    var dateToShow = format(d.date, 'yyyy-MM-dd');
    //console.log(dateToShow);
    //console.log(all_articles[dateToShow]);
    displayArticles(all_articles[dateToShow], String(d.date).substring(4, 15));
	}
});

var keyword_data = [];
for (var prop in keywords) {
	keyword_data.push({'name': prop, 'size': keywords[prop]});
}

keyword_data.sort(function(a, b) { 
    return b.size - a.size;
})

keyword_data = keyword_data.slice(0, 29);

var diameter = 875;
var color = ["#81c784", "#7986cb", "#b39ddb", "#29b6f6", "#26c6da", "#26a69a", "#78909c"];

var svg = d3.select('#bubble-chart')
                .append('div')
                .classed("svg-container", true)
                .append('svg')
                .attr("preserveAspectRatio", "xMinYMin meet")
                //NEED TO CHANGE VIEWBOX HERE IF YOU CHANGE DIMENSIONS
                .attr("viewBox", "0 0 875 875")
                .classed("svg-content-responsive", true);

var bubble = d3.layout.pack()
            .size([diameter, diameter])
            .value(function(d) {return d.size;})
     // .sort(function(a, b) {
            //  return -(a.value - b.value)
            // }) 
            .padding(3);

  // generate data with calculated layout values
  var nodes = bubble.nodes({children: keyword_data})
                        .filter(function(d) { return !d.children; }); // filter out the outer bubble
 
  var vis = svg.append("g")
  				.selectAll('circle')
                .data(nodes);
  
  vis.enter().append('circle')
  			.style("fill", function(d, i) { return color[i % color.length]; })
            .attr('transform', function(d) { return 'translate(' + d.x + ',' + d.y + ')'; })
            .attr('r', function(d) { return d.r; })
            .on("mouseenter", keywordMouseover)
            .on("mouseleave", function(d) {
            		d3.select(this).style("opacity", 1); 
            		d3.select(this).attr("r", d.r-5); 
            	})
           	.on("click", function(d) {
           		location.href = "/results/" + d.name;
           	})
        .append("text")
      .attr("dy", ".3em")
      .style("text-anchor", "middle");

 
 vis.enter().append('text')
 	.attr("x", function(d){ return d.x; })
    .attr("y", function(d){ return d.y + 5; })
    .attr("text-anchor", "middle")
    .attr("pointer-events", "none")
 	.style("color", "white")
    .text(function(d) { return d.name });

	function keywordMouseover(d, i) {
		//d3.select(this).select("text").style("font-weight", "bold");
		d3.select(this).style("opacity", 0.5);
		d3.select(this).attr("r", d.r + 5);
		var word = d.name;
		var keywordArticles = [];
		for (prop in all_articles) {
			var articlesfordate = all_articles[prop];
			if (articlesfordate != null) {
 			for (var i=0; i<articlesfordate.length; i ++) {
 				var currArticle = articlesfordate[i]
	 			if (currArticle.keywords.indexOf(word) > -1) {
	 				keywordArticles.push(currArticle);
	 			}
 			}
			}
		}
		//console.log(keywordArticles);
		var title = '"' + query + '" + ' + '"' + word + '"';
		displayArticles(keywordArticles, title);
	} 

function displayArticles(arts, date) {
    $('#display-arts').html('');
	var htmlStr = '';
	if (arts != null) {
		$('#article-header').html('<h5>Articles published on <span style="color:#5c6bc0;">' + date + '</span></h5>');
    	for (var i=0; i < arts.length; i ++) {
    		var thisArt = arts[i];
    		htmlStr += '<div class="section">';
    		htmlStr += '<h6><a class="article-link" target="_blank" href="' + thisArt.url + '">' + thisArt.title + '</a></h6>';
    		if (thisArt.keywords != null) {
    			htmlStr += '<span>Keywords</span>: ';
	    		for (var j=0; j < thisArt.keywords.length; j++) {
	    			htmlStr += '<div class="chip"><a href="/results/' + thisArt.keywords[j] + '">' + thisArt.keywords[j] + '</a></div>';
	    		}
    		}
    		htmlStr += '</div>';
    		htmlStr += '<div class="divider"></div>';
    	}
    	$('#display-arts').html(htmlStr);
    }
}

format = function date2str(x, y) {
    var z = {
        M: x.getMonth() + 1,
        d: x.getDate(),
        h: x.getHours(),
        m: x.getMinutes(),
        s: x.getSeconds()
    };
    y = y.replace(/(M+|d+|h+|m+|s+)/g, function(v) {
        return ((v.length > 1 ? "0" : "") + eval('z.' + v.slice(-1))).slice(-2)
    });

    return y.replace(/(y+)/g, function(v) {
        return x.getFullYear().toString().slice(-v.length)
    });
}

$(document).ready(function() {
    $('#articles-card').pushpin({ top: $('#articles-card').offset().top });
}) 