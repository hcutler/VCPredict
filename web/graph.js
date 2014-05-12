var tah = $('#squery').typeahead();
var highlighted = "";
var node;

function hlight(item) {
  highlighted = item;
  node.style("stroke", function(d) { return (d.name==highlighted ? "#FFA500" : "#FFFFFF")})
            .style("stroke-width", function(d) { return (d.name==highlighted ? 20 : 0); });
}

function writeTypeAheads() {
  d3.text("verts.csv", function(error, wdata) {
    wdata = d3.csv.parseRows(wdata);
    sources = [];
    for (var i=0; i<wdata.length; i++)
      sources.push(wdata[i][0]);
    tah.data('typeahead').updater = function(item) {
      hlight(item);
      return item;
    };
    tah.data('typeahead').source = sources;
  });
}

function sortNumber(a,b){
   return a - b;
}

function makeGradientColor(color1, color2, percent) {
    var newColor = {};

    function makeChannel(a, b) {
        return(a + Math.round((b-a)*(percent/100)));
    }

    function makeColorPiece(num) {
        num = Math.min(num, 255);   // not more than 255
        num = Math.max(num, 0);     // not less than 0
        var str = num.toString(16);
        if (str.length < 2) {
            str = "0" + str;
        }
        return(str);
    }

    newColor.r = makeChannel(color1.r, color2.r);
    newColor.g = makeChannel(color1.g, color2.g);
    newColor.b = makeChannel(color1.b, color2.b);
    newColor.cssColor = "#" + 
                        makeColorPiece(newColor.r) + 
                        makeColorPiece(newColor.g) + 
                        makeColorPiece(newColor.b);
    return(newColor);
}

var yellow = {r:255, g:255, b:0};
var red = {r:255, g:0, b:0};
var black = {r:0, g:0, b:0};
var white = {r:255, g:255, b:255};
var green = {r:0, g:255, b:0};
var gray = {r:240, g:240, b:240};
var dgray = {r:144, g:144, b:144};


function drawGraph() {

  var cthresh = parseFloat(document.getElementById("cor-thresh").value);

  d3.text("verts.csv", function(error, wdata) {
    wdata = d3.csv.parseRows(wdata);

    var V = new Object(), graph = {nodes: [], links: []}, sec = {};
    for (var i=0; i<wdata.length; i++) {
      V[wdata[i][0].replace("\"", "")] = i;
      graph.nodes.push({"name": wdata[i][0], "ind": i, "category": wdata[i][2]});
      if (sec[wdata[i][2]]==null)
        sec[wdata[i][2]] = Object.keys(sec).length;      
    }

    var width = 900,
        height = 600;

    var color = d3.scale.category20();
    //var color = ["#FFFF66", "#FFCC00", "#FF9900", "#CC3300"];

    var force = d3.layout.force()
        .charge(-120)
        .linkDistance(30)
        .size([width, height]);

    document.getElementById("graph").style.width = width + "px";
    document.getElementById("graph").style.height = (height) + "px";

    var div = d3.select("body").append("div")   
      .attr("class", "tooltip")               
      .style("opacity", 0);

    document.getElementById("graph").innerHTML = "";

    var svg = d3.select("#graph").append("svg")
        .attr("width", width)
        .attr("height", height);

    var box = svg.append("rect")
         .attr("x", 0)
         .attr("y", 0)
         .attr("width", width)
         .attr("height", height)
         .style("fill", "#F8F8F8")
         .style("stroke-width", 2)
         .style("stroke", "#F5F5F5");

    d3.text("adj.csv", function(error, rawData) {

      var data = d3.csv.parseRows(rawData);
      var carr = [[]], csrt = [], cquart = [[]];
      var cor = [], sum;
      for (var i=0; i<data.length; i++) {
        cor.push([]); carr.push([]);
        sum = 0;
        for (var j=1; j<data[i].length; j++)
          sum += parseFloat(data[i][j].split("||")[1]);
        for (var j=1; j<data[i].length; j++) {
          cor[i].push(parseFloat(data[i][j].split("||")[1]) / sum);
          carr[i].push(parseFloat(data[i][j].split("||")[1]) / sum);
          csrt.push(parseFloat(data[i][j].split("||")[1]) / sum);
          if (parseFloat(data[i][j].split("||")[1]) / sum > cthresh) {
            if (!(data[i][0] in V && data[i][j].split("||")[0] in V)) break;
            graph.links.push({"source": V[data[i][0]], "target": V[data[i][j].split("||")[0]], "value": parseFloat(data[i][j].split("||")[1]) / sum});
          
          }
        }
      }

      csrt.sort(sortNumber);
      for (var i=0; i<data.length; i++) {
        cquart.push([]);
        for (var j=0; j<data.length; j++)
          cquart[i].push(0);
      }

      for (var i=0; i<carr.length; i++) {
        for (var j=0; j<carr[i].length; j++) {
          if (carr[i][j] <= csrt[Math.floor(parseFloat(csrt.length) / parseFloat(4))]) cquart[i][j] = 0;
          else if (carr[i][j] <= csrt[Math.floor(parseFloat(csrt.length) / parseFloat(4) * 2)]) cquart[i][j] = 1;
          else if (carr[i][j] <= csrt[Math.floor(parseFloat(csrt.length) / parseFloat(4) * 3)]) cquart[i][j] = 2;
          else cquart[i][j] = 3;
          //cquart[j][i] = cquart[i][j];
          //carr[j][i] = carr[i][j];
        }
      }

      force
          .nodes(graph.nodes)
          .links(graph.links)
          .start();

      var link = svg.selectAll(".link")
          .data(graph.links)
        .enter().append("line")
          .attr("class", "link")
          .style("stroke-width", function(d) { return (cquart[d.source.ind][d.target.ind] + 1) / 2; })//0.5; })//Math.sqrt(d.value); });
          .style("stroke", function(d) { 
            return makeGradientColor(gray, dgray, 100 * Math.abs(cquart[d.source.ind][d.target.ind] - (-1)) / Math.abs(1 - (-1))).cssColor; 
            //return makeGradientColor(gray, dgray, 100 * Math.abs(cquart[d.source.ind][d.target.ind] - csrt[0]) / Math.abs(csrt[csrt.length - 1] - csrt[0])).cssColor; 
          })//color[cquart[d.source.ind][d.target.ind]]; } )

      node = svg.selectAll(".node")
          .data(graph.nodes)
        .enter().append("circle")
          .attr("class", "node")
          .attr("r", 5)
          .style("fill", function(d) { return color(sec[d.category]); })//makeGradientColor(yellow, red, 100 * Math.abs(arr[d.ind] - srt[0]) / Math.abs(srt[srt.length - 1] - srt[0])).cssColor; })
          .style("stroke", function(d) { return (d.name==highlighted ? "#000000" : "#FFFFFF")})
          .style("stroke-width", function(d) { return (d.name==highlighted ? 2 : 0); })
          .call(force.drag)
          .on("mouseover", function(d) {      
              div.transition()        
                  .duration(200)      
                  .style("opacity", .9);      
              div .html(d.name + (d.category != "" ? " - " : "") + d.category)  
                  .style("left", (d3.event.pageX) + "px")     
                  .style("top", (d3.event.pageY - 28) + "px");    
              })                  
          .on("mouseout", function(d) {       
              div.transition()        
                  .duration(500)      
                  .style("opacity", 0);   
          })
          .on("click", function(d) {
            //window.open(d.url, '_blank');
          });

      node.append("title")
          .text(function(d) { return d.name; });

      force.on("tick", function() {
        link.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        node.attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });
      });

      var zoom = d3.behavior.zoom()
        .on("zoom",function() {
            node.attr("transform","translate("+ 
                d3.event.translate.join(",")+")scale("+d3.event.scale+")");
            link.attr("transform","translate("+ 
                d3.event.translate.join(",")+")scale("+d3.event.scale+")"); 
        });

      svg.call(zoom);

    });

  });

}