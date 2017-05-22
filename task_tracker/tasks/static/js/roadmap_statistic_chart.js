
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

url_json_data = protocol+hostname+port+url_json_data

var svg = d3.select("svg"),
    margin = {top: 40, right: 20, bottom: 30, left: 50},
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom,
    g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

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

  var new_data = data.object_list.map(function(d) {
    return {date:parseTime(d[0]+'-'+data.year),
            value:d[1]
           };
  });

  var start_date = new Date(data.year, 0, 0),
      end_date = new Date(data.year, 12, 31);
  x.domain([start_date, end_date]);
  y.domain([0, d3.max(new_data, function(d) {return d.value }) ]);

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
      .text("Очки");

  g.append("path")
      .datum(new_data)
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-linejoin", "round")
      .attr("stroke-linecap", "round")
      .attr("stroke-width", 1.5)
      .attr("d", line);
});
