<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>pie chart sample</title>
<div class="one-graph"></div>
<script src="https://d3js.org/d3.v4.min.js"></script>
 
<body>
    
</body>

    
<script>
var w = 400, h = 400;

// 예상 UI 색감과 맞추어 다홍색 계열의 색조합 사용
var colorData = ["#A64E6E", "#F2BB77", "#F2A25C", "#FFE2DF", "#FFC001", "#FF6F61", "#F8A39D", "#81894E"];

var dataName = [];
var dataValue = [];

// json 파일 연동하여 label(감성), value(빈도) 가져오기
d3.json("./output_video_data/sample_data.json",function(data) {
             
        for (var i = 0; i < data.length; i++) {
             //json 파일의 label, value 를 각각의 dataName, 
            dataName.push(data[i].label);
            dataValue.push(data[i].value);
        }
});


setTimeout(function(){

    var pie = d3.pie();
    var arc = d3.arc().innerRadius(70).outerRadius(200);
     
    var svg = d3.select(".one-graph")
        .append("svg")
        .attr("width", w)
        .attr("height", h)
        .attr("id", "graphWrap");
     
    var g = svg.selectAll(".pie")
        .data(pie(dataValue))
        .enter()
        .append("g")
        .attr("class", "pie")
        .attr("transform","translate("+w/2+","+h/2+")");
     
    g.append("path")
        .style("fill", function(d, i) {
            return colorData[i];
        }) 
        .transition()
        .duration(400)
        .delay(function(d, i) { 
            return i * 400;
        })
        .attrTween("d", function(d, i) { 
            var interpolate = d3.interpolate(
                {startAngle : d.startAngle, endAngle : d.startAngle}, 
                {startAngle : d.startAngle, endAngle : d.endAngle} 
            );
            return function(t){
                return arc(interpolate(t)); 
            }
        });
     
    g.append("text")
        .attr("transform", function(d) { return "translate(" + arc.centroid(d) + ")"; })
        .attr("dy", ".30em")
        .style("text-anchor", "middle")
        .text(function(d, i) {
            return  d.endAngle-d.startAngle > 0.2 ?
                    dataName[i] + " (" + Math.round(1000*(d.endAngle-d.startAngle)/(Math.PI*2))/10 + "%)" : ""
        });

     
 }, 100);
 
</script>