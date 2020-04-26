

var tex1=d3.select("#svg1")
           .append("text")
           .attr("class","text f3_text")
           .attr("transform", "translate(275,125)")
           .text("House Condition")
           .attr("font-size","70")

var p1 = d3.select("#svg1")
           .append("g")
           .attr("transform", "translate(175,225)");

var height = 518,
    width = 750;

var x1 = d3.scaleBand().range([0, width]).padding(0.2);

var y1 = d3.scaleLinear().rangeRound([height, 0]);

var xAxis1 = d3.axisBottom()
    .scale(x1);

var yAxis1 = d3.axisLeft()
    .scale(y1)

var fileRandTail = "?dev=" + Math.floor(Math.random() * 100)
d3.csv("data/web/OverallCond.csv" + fileRandTail).then(function(data) {

    data.forEach(function(d) {
        d.overall_condition = +d.overall_condition;
        d.predicted_price = +d.predicted_price;
    });
	
  x1.domain(data.map(function(d) { return d.overall_condition; }));
  y1.domain([d3.min(data, function(d) { return d.predicted_price; }) *7 /8, d3.max(data, function(d) { return d.predicted_price; })]);

  p1.append("g")
      .attr("class", "Xaxis")
      .attr("transform", "translate(0,"+height+")")
      .call(xAxis1)
    
  yAxis1.ticks(8, ".0s")
  p1.append("g")
      .attr("class", "Yaxis Y1")
      .call(yAxis1)
   
  p1.selectAll("bar")
      .data(data)
    .enter().append("rect")
      .style("fill", "#5bb2f5")
      .attr("class", "bar")
      .attr("x", function(d) { return x1(d.overall_condition); })
      .attr("width", x1.bandwidth())
      .attr("y", function(d) { return y1(d.predicted_price); })
      .attr("height", function(d) { return height - y1(d.predicted_price); });

});

var tex2=d3.select("#svg2")
           .append("text")
           .attr("class","text f3_text")
           .attr("transform", "translate(325,125)")
           .text("Neighborhood")
           .attr("font-size","70")

var p2 = d3.select("#svg2")
           .append("g")
           .attr("transform", "translate(175,225)");

var x2 = d3.scaleBand().range([0, width]).padding(0.2);

var y2 = d3.scaleLinear().rangeRound([height, 0]);

var xAxis2 = d3.axisBottom()
    .scale(x2);

var yAxis2 = d3.axisLeft()
    .scale(y2)

d3.csv("data/web/Neighborhood.csv" + fileRandTail).then(function(data) {
    var neib = ["Excellent","Good","Fair","Poor"];
    var i = 0;
    data.forEach(function(d) {
        d.Neighborhood = neib[i];
        i = i +1;
        d.predicted_price = +d.predicted_price;
    });
	
  x2.domain(data.map(function(d) { return d.Neighborhood; }));
  y2.domain([d3.min(data, function(d) { return d.predicted_price; }) *7 /8, d3.max(data, function(d) { return d.predicted_price; })]);

  p2.append("g")
      .attr("class", "Xaxis")
      .attr("transform", "translate(0,"+height+")")
      .call(xAxis2)
  
  yAxis2.ticks(8, ".0s")  
  p2.append("g")
      .attr("class", "Yaxis Y1")
      .call(yAxis2)

  p2.selectAll("bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .style("fill", "#f5a05b")
      .attr("x", function(d) { return x2(d.Neighborhood); })
      .attr("width", x2.bandwidth())
      .attr("y", function(d) { return y2(d.predicted_price); })
      .attr("height", function(d) { return height - y2(d.predicted_price); });

// plots
var controller = new ScrollMagic.Controller();

var tlCurtain = new TimelineMax();
    tlCurtain
    .from('.f3_text', 0.5, {css:{opacity:0}})
    .from('.Y1', 1, {scaleY: 0, transformOrigin: "bottom", ease:Power4.easeOut})
    .from('.bar', 1, {scaleY: 0, transformOrigin: "bottom", ease:Power4.easeOut})

var scene = new ScrollMagic.Scene({triggerElement: ".floor3"})
    .addTo(controller)
    .setTween(tlCurtain);
});

var tex3=d3.select("#svg3")
           .append("text")
           .attr("class","text f4_text")
           .attr("transform", "translate(75,145)")
           .text("Predicted Price in Different Months")
           .attr("font-size","60")

var p3 = d3.select("#svg3")
           .append("g")
           .attr("transform", "translate(175,225)");

var x3 = d3.scaleBand().range([0, width]).padding(0.2);

var y3 = d3.scaleLinear().rangeRound([height, 0]);

var xAxis3 = d3.axisBottom()
    .scale(x3);

var yAxis3 = d3.axisLeft()
    .scale(y3)

d3.csv("data/web/MoSold.csv" + fileRandTail).then(function(data) {

    data.forEach(function(d) {
        d.Month_Sold = +d.Month_Sold;
        d.predicted_price = +d.predicted_price;
    });

  x3.domain(data.map(function(d) { return d.Month_Sold; }));
  y3.domain([d3.min(data, function(d) { return d.predicted_price; }) *69 /70, d3.max(data, function(d) { return d.predicted_price; })]);

  p3.append("g")
      .attr("class", "Xaxis")
      .attr("transform", "translate(0,"+height+")")
      .call(xAxis3)

  yAxis3.ticks(8, ".0s")
  p3.append("g")
      .attr("class", "Yaxis Y3")
      .call(yAxis3)

  p3.selectAll("bar")
      .data(data)
    .enter().append("rect")
      .style("fill", "#5bb2f5")
      .attr("class", "bar3")
      .attr("x", function(d) { return x3(d.Month_Sold); })
      .attr("width", x3.bandwidth())
      .attr("y", function(d) { return y3(d.predicted_price); })
      .attr("height", function(d) { return height - y3(d.predicted_price); });

// plots
var controller5 = new ScrollMagic.Controller();

var tlCurtain5 = new TimelineMax();
    tlCurtain5
    .from('.f4_text', 0.5, {css:{opacity:0}})
    .from('.Y3', 1, {scaleY: 0, transformOrigin: "bottom", ease:Power4.easeOut})
    .from('.bar3', 1, {scaleY: 0, transformOrigin: "bottom", ease:Power4.easeOut})

var scene = new ScrollMagic.Scene({triggerElement: ".floor4"})
    .addTo(controller5)
    .setTween(tlCurtain5);

});


var tex4=d3.select("#svg4")
           .append("text")
           .attr("class","text f5_text")
           .attr("transform", "translate(275,125)")
           .text("Kitchen Condition")
           .attr("font-size","70")

var p4 = d3.select("#svg4")
           .append("g")
           .attr("transform", "translate(175,225)");

var x4 = d3.scaleBand().range([0, width]).padding(0.2);

var y4 = d3.scaleLinear().rangeRound([height, 0]);

var xAxis4 = d3.axisBottom()
    .scale(x4);

var yAxis4 = d3.axisLeft()
    .scale(y4)

d3.csv("data/web/KitchenQual.csv" + fileRandTail).then(function(data) {
    var neib = ["Excellent","Good","Fair","Poor"];
    var i = 0;
    data.forEach(function(d) {
        d.Kitchen_Quality = neib[i];
        i = i +1;
        d.predicted_price = +d.predicted_price;
    });

  x4.domain(data.map(function(d) { return d.Kitchen_Quality; }));
  y4.domain([d3.min(data, function(d) { return d.predicted_price; }) *19 /20, d3.max(data, function(d) { return d.predicted_price; })]);

  p4.append("g")
      .attr("class", "Xaxis")
      .attr("transform", "translate(0,"+height+")")
      .call(xAxis4)

  yAxis4.ticks(8, ".0s")
  p4.append("g")
      .attr("class", "Yaxis Y4")
      .call(yAxis4)

  p4.selectAll("bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar4")
      .style("fill", "#f5a05b")
      .attr("x", function(d) { return x4(d.Kitchen_Quality); })
      .attr("width", x4.bandwidth())
      .attr("y", function(d) { return y4(d.predicted_price); })
      .attr("height", function(d) { return height - y4(d.predicted_price); });


// plots
var controller6 = new ScrollMagic.Controller();

var tlCurtain6 = new TimelineMax();
    tlCurtain6
    .from('.f5_text', 0.5, {css:{opacity:0}})
    .from('.Y4', 1, {scaleY: 0, transformOrigin: "bottom", ease:Power4.easeOut})
    .from('.bar4', 1, {scaleY: 0, transformOrigin: "bottom", ease:Power4.easeOut})

var scene6 = new ScrollMagic.Scene({triggerElement: ".floor5"})
    .addTo(controller6)
    .setTween(tlCurtain6);
});






//house
var tl = new TimelineMax();
tl.from('.ground', 0.6, {scaleX: 0, transformOrigin: "bottom", ease: Power3.easeOut})
  .from('.tree', 1, {scaleY: 0, transformOrigin: "bottom", ease: Power4.easeOut})
  .from('.house', 1, {scaleY: 0, transformOrigin: "bottom", ease: Power4.easeOut})
  .from('.text1', 0.5, {css:{opacity:0}})

// words
var controller2 = new ScrollMagic.Controller();
var tl2 = new TimelineMax();
    tl2.from('.text2', 0.5, {css:{opacity:0}})
var scene2 = new ScrollMagic.Scene({triggerElement: ".text2"})
    .addTo(controller2)
    .setTween(tl2);


var controller3 = new ScrollMagic.Controller();
var tl3 = new TimelineMax();
    tl3.from('.text3', 0.5, {css:{opacity:0}})
var scene3 = new ScrollMagic.Scene({triggerElement: ".text3"})
    .addTo(controller3)
    .setTween(tl3);


var controller4 = new ScrollMagic.Controller();
var tl4 = new TimelineMax();
    tl4.from('.text4', 0.5, {css:{opacity:0}})
var scene4 = new ScrollMagic.Scene({triggerElement: ".text4"})
    .addTo(controller4)
    .setTween(tl4);




