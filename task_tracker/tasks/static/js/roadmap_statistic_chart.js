function set_data(range, array, check_ind){
    array.forEach(function(item, ind) {
        if (item[check_ind])
            range[item[0]].value = item[check_ind];
        else range[item[0]].value = 0;
    });
}

function set_score_data(range, array, check_ind){
    array.forEach(function(item, ind) {
        range[new Date(item[0]).getMonth()].value = item[check_ind];
    });
}

  d3.timeFormatDefaultLocale({
    "dateTime": "%A, %e %B %Y г. %X",
    "date": "%d.%m.%Y",
    "time": "%H:%M:%S",
    "periods": ["AM", "PM"],
    "days": ["воскресенье", "понедельник", "вторник", "среда", "четверг", "пятница", "суббота"],
    "shortDays": ["вс", "пн", "вт", "ср", "чт", "пт", "сб"],
    "months": ["январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"],
    "shortMonths": ["янв", "фев", "мар", "апр", "май", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"]
  });


var protocol = location.protocol+'//',
    hostname = location.hostname,
    port = location.port ? ':'+location.port : '';

var url_json_data = protocol+hostname+port+url_json_data,
    url_json_data2 = protocol+hostname+port+url_json_data2;


var svg = d3.select("svg.created-finished"),
    margin = {top: 40, right: 20, bottom: 30, left: 50},
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom,
    g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
var svg2 = d3.select("svg.sum-score"),
    margin = {top: 40, right: 20, bottom: 30, left: 50},
    width = +svg2.attr("width") - margin.left - margin.right,
    height = +svg2.attr("height") - margin.top - margin.bottom,
    g2 = svg2.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var parseTime = d3.timeParse("%W-%Y");

var x = d3.scaleTime()
    .rangeRound([0, width]);

var y = d3.scaleLinear()
    .rangeRound([height, 0]);

var line = d3.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.value); });

d3.json(url_json_data, function(error, data) {
  if (error) throw error;

  var data_range = new Array(),
      data_range2 = new Array(),
      weeks_count = 54, year = data.year,
      create_ind = 1, finish_ind = 2;

  for (var i = 0; i < weeks_count; i++){
      var date = parseTime(i+'-'+year);
      data_range.push({date:date,
                       value:0
                      });
      data_range2.push({date:date,
                       value:0
                      });
  }

set_data(data_range, data.object_list, create_ind);
set_data(data_range2, data.object_list, finish_ind);

  var start_date = new Date(data.year, 0, -7),
      end_date = new Date(data.year, 12, 31);
  x.domain([start_date, end_date]);

  y.domain([0, d3.max(data.object_list, function(d) {return Math.max(d[1], d[2]) }) ]);

  g.append("text")
        .attr("x", (width / 2))
        .attr("y", 0 - (margin.top / 2))
        .attr("text-anchor", "middle")
        .style("font-size", "2em")
        .style("text-decoration", "underline")
        .text("Статистика за "+data.year+" год");

  g.append("g")
      .style("font", "1em times")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

  g.append("g")
      .style("font", "1em times")
      .call(d3.axisLeft(y))
    .append("text")
      .attr("fill", "#000")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", "0.71em")
      .attr("text-anchor", "end")
      .text("Задач");

  var lines_width = 2.5;

  g.append("path")
      .datum(data_range)
      .attr("fill", "none")
      .attr("stroke-linejoin", "round")
      .attr("stroke-linecap", "round")
      .attr("stroke-width", lines_width)
      .attr("d", line)
      .classed("created", true);;

  g.append("path")
      .datum(data_range2)
      .attr("fill", "none")
      .attr("stroke-linejoin", "round")
      .attr("stroke-linecap", "round")
      .attr("stroke-width", lines_width)
      .attr("d", line)
      .classed("finished", true);;
});

d3.json(url_json_data2, function(error, data) {
  if (error) throw error;

  var data_range3 = new Array(),
      month_count = 12, year = data.year,
      score_ind = 1;

  for (var i = 0; i < month_count; i++){
      data_range3.push({date:new Date(year,i,1),
                       value:0
                      });
  }

  set_score_data(data_range3, data.object_list, score_ind);

  var start_date = new Date(data.year, 0, -7),
      end_date = new Date(data.year, 12, 31);
  x.domain([start_date, end_date]);

  y.domain([0, d3.max(data.object_list, function(d) {return parseFloat(d[1]) }) ]);

  g2.append("text")
        .attr("x", (width / 2))
        .attr("y", 0 - (margin.top / 2))
        .attr("text-anchor", "middle")
        .style("font-size", "2em")
        .style("text-decoration", "underline")
        .text("Статистика за "+data.year+" год");

  g2.append("g")
      .style("font", "1em times")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

  g2.append("g")
      .style("font", "1em times")
      .call(d3.axisLeft(y))
    .append("text")
      .attr("fill", "#000")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", "0.71em")
      .attr("text-anchor", "end")
      .text("Очков");

  var lines_width = 2.5;

  g2.append("path")
      .datum(data_range3)
      .attr("fill", "none")
      .attr("stroke-linejoin", "round")
      .attr("stroke-linecap", "round")
      .attr("stroke-width", lines_width)
      .attr("d", line)
      .classed("points", true);;
});
