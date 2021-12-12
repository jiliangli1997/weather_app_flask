
let loc = "";

function disableform() {
    let check = document.getElementById("auto");
    if (check.checked) {
        axios.get('https://ipinfo.io/json?token=8dccb3b9c65547').then(function(response) {

            loc = response["data"]["loc"];
            var d = document.getElementById("div1");
            document.getElementById('city').classList.add("hide");
            document.getElementById('street').classList.add("hide");
            document.getElementById('state').classList.add("hide");
            // document.getElementById('city').style.color = "white";
            // document.getElementById('street').style.color = "white";
            // document.getElementById("state").style.color = "grey";
            document.getElementById('city').value = response["data"]["city"];
            document.getElementById('street').value = "***";
            document.getElementById('state').value = response["data"]["region"];
        }) .catch(function (error) {
            console.log('error');
        });
        check = true;
        // document.getElementById('city').disabled = true;
        // document.getElementById('street').disabled = true;
        // document.getElementById('state').disabled = true;
    } else {
        document.getElementById('city').classList.remove("hide");
        document.getElementById('street').classList.remove("hide");
        document.getElementById('state').classList.remove("hide");
        document.getElementById('city').value = null;
        document.getElementById('street').value = null;
        document.getElementById('state').value = null;
        check = false;
    }
}



let out = false;


function hide() {
    document.getElementById("hide").style.display="none";
}

let hData;
function show(date, hour_data) {
    console.log(hour_data);
    let cat = [];
    let temp = [];
    let mon = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    let mon_string;
    let month;
    let day;
    for (let i = 0; i < date.length; i++) {
        day = date[i]["startTime"].split('-')
        month = day[1]
        mon_string = mon[Number(day[1]) - 1]
        let cur = ""
        if (day[2][0] !== '0') {
            cur = String(day[2].substring(0,2)) + " " + String(mon_string)
        } else {
            cur = String(day[2].substring(1,2)) + " " + String(mon_string)
        }
        cat.push(cur)
        temp.push([Number(date[i]["values"]["temperatureMin"]), Number(date[i]["values"]["temperatureMax"])])

    }

    if (!out)
        document.getElementById("hide").style.display="inline";

            Highcharts.chart('container1', {

                chart: {
                    width: 800,
                    type: 'arearange',
                    zoomType: 'x',
                    scrollablePlotArea: {
                        minWidth: 500,
                        scrollPositionX: 1
                    }
                },

                title: {
                    text: 'Temperature Ranges (Min, Max)'
                },

                xAxis: {
                    type: 'datetime',
                    categories: cat,
                    tickColor: '#000000',
                    tickWidth: 1,
                    tickmarkPlacement: 'on',
                    tickInterval: 1
                },

                yAxis: {
                    title: {
                        text: null
                    }
                },

                tooltip: {
                    crosshairs: true,
                    shared: true,
                    valueSuffix: '°C',
                    xDateFormat: '%b %e, %Y'
                },

                legend: {
                    enabled: false
                },

                series: [{
                    name: 'Temperatures',
                    data: temp,
                    lineColor: '#f7aa30',
                    marker: {
                        fillColor: '#7cb4ec',
                    },
                    color: {
                        linearGradient : {
                            x1: 0,
                            y1: 1,
                            x2: 0,
                            y2: 0
                        },
                        stops : [
                            [0, Highcharts.Color('#f7aa30').setOpacity(1).get('rgba')],
                            [1, Highcharts.Color('#d9e6f2').setOpacity(1).get('rgba')],
                        ]
                    },
                    fillColor : {
                        linearGradient : {
                            x1: 0,
                            y1: 0,
                            x2: 0,
                            y2: 1,
                        },
                        stops : [
                            [0, Highcharts.Color('#f7aa30').setOpacity(1).get('rgba')],
                            [1, Highcharts.Color('#d9e6f2').setOpacity(0.2).get('rgba')],
                        ]
                    }
                }]

            });
            window.meteogram = new Meteogram(hour_data, 'container');



}
/**
 * This is a complex demo of how to set up a Highcharts chart, coupled to a
 * dynamic source and extended by drawing image sprites, wind arrow paths
 * and a second grid on top of the chart. The purpose of the demo is to inpire
 * developers to go beyond the basic chart types and show how the library can
 * be extended programmatically. This is what the demo does:
 *
 * - Loads weather forecast from www.yr.no in form of a JSON service.
 * - When the data arrives async, a Meteogram instance is created. We have
 *   created the Meteogram prototype to provide an organized structure of the
 *   different methods and subroutines associated with the demo.
 * - The parseYrData method parses the data from www.yr.no into several parallel
 *   arrays. These arrays are used directly as the data option for temperature,
 *   precipitation and air pressure.
 * - After this, the options structure is built, and the chart generated with
 *   the parsed data.
 * - On chart load, weather icons and the frames for the wind arrows are
 *   rendered using custom logic.
 */

function Meteogram(json, container) {
    // Parallel arrays for the chart data, these are populated as the JSON file
    // is loaded
    console.log(json);

    this.symbols = [];
    this.hum = [];
    this.precipitations = [];
    this.precipitationsError = []; // Only for some data sets
    this.winds = [];
    this.temperatures = [];
    this.pressures = [];

    // Initialize
    this.json = json;
    this.container = container;

    // Run
    this.parseYrData();
}





/**
 * Draw blocks around wind arrows, below the plot area
 */
Meteogram.prototype.drawBlocksForWindArrows = function (chart) {
    const xAxis = chart.xAxis[0];

    for (
        let pos = xAxis.min, max = xAxis.max, i = 0;
        pos <= max + 36e5; pos += 36e5,
            i += 1
    ) {

        // Get the X position
        const isLast = pos === max + 36e5,
            x = Math.round(xAxis.toPixels(pos)) + (isLast ? 0.5 : -0.5);

        // Draw the vertical dividers and ticks
        const isLong = this.resolution > 36e5 ?
            pos % this.resolution === 0 :
            i % 2 === 0;

        chart.renderer
            .path([
                'M', x, chart.plotTop + chart.plotHeight + (isLong ? 0 : 28),
                'L', x, chart.plotTop + chart.plotHeight + 25,
                'Z'
            ])
            .attr({
                stroke: chart.options.chart.plotBorderColor,
                'stroke-width': 1
            })
            .add();
    }

    // Center items in block
    chart.get('windbarbs').markerGroup.attr({
        translateX: chart.get('windbarbs').markerGroup.translateX + 8
    });

};

/**
 * Build and return the Highcharts options structure
 */
Meteogram.prototype.getChartOptions = function () {
    return {
        chart: {
            width: 800,
            height: 500,
            renderTo: this.container,
            marginBottom: 70,
            marginRight: 40,
            marginTop: 50,
            plotBorderWidth: 1,
            height: 310,
            alignTicks: false,
            scrollablePlotArea: {
                minWidth: 720
            }
        },

        defs: {
            patterns: [{
                id: 'precipitation-error',
                path: {
                    d: [
                        'M', 3.3, 0, 'L', -6.7, 10,
                        'M', 6.7, 0, 'L', -3.3, 10,
                        'M', 10, 0, 'L', 0, 10,
                        'M', 13.3, 0, 'L', 3.3, 10,
                        'M', 16.7, 0, 'L', 6.7, 10
                    ].join(' '),
                    stroke: '#68CFE8',
                    strokeWidth: 1
                }
            }]
        },

        title: {
            text: 'Hourly Weather (For Next 5 Days)',
            align: 'center',
            style: {
                whiteSpace: 'nowrap',
                textOverflow: 'ellipsis',
            }
        },


        tooltip: {
            shared: true,
            useHTML: true,
            headerFormat:
                '<small>{point.x:%A, %b %e, %H:%M}</small><br>' +
                '<b>{point.point.symbolName}</b><br>'

        },

        xAxis: [{ // Bottom X axis
            type: 'datetime',
            tickInterval: 4 * 36e5, // two hours
            minorTickInterval: 36e5, // one hour
            tickLength: 0,
            gridLineWidth: 1,
            gridLineColor: 'rgba(128, 128, 128, 0.1)',
            startOnTick: false,
            endOnTick: false,
            minPadding: 0,
            maxPadding: 0,
            offset: 30,
            showLastLabel: true,
            labels: {
                format: '{value:%H}'
            },
            crosshair: true
        }, { // Top X axis
            linkedTo: 0,
            type: 'datetime',
            tickInterval: 24 * 3600 * 1000,
            labels: {
                format: '{value:<span style="font-size: 10px; font-weight: bold">%a</span> %b %e}',
                align: 'left',
                x: 3,
                y: -5,
                style: {
                    fontSize: '10px',
                }
            },
            opposite: true,
            tickLength: 20,
            gridLineWidth: 1
        }],

        yAxis: [{ // temperature axis
            title: {
                text: null
            },
            labels: {
                format: '{value}°',
                style: {
                    fontSize: '10px'
                },
                x: -3
            },
            plotLines: [{ // zero plane
                value: 0,
                color: '#BBBBBB',
                width: 1,
                zIndex: 2
            }],
            maxPadding: 0.3,
            minRange: 8,
            tickInterval: 1,
            gridLineColor: 'rgba(128, 128, 128, 0.1)'

        }, { // precipitation axis
            title: {
                text: null
            },
            labels: {
                enabled: false
            },
            gridLineWidth: 0,
            tickLength: 0,
            minRange: 10,
            min: 0

        }, { // Air pressure
            allowDecimals: false,
            title: { // Title on top of axis
                text: 'inHg',
                offset: 0,
                align: 'high',
                rotation: 0,
                style: {
                    fontSize: '10px',
                    color: '#deaf54'
                },
                textAlign: 'left',
                x: 3,
            },
            labels: {
                style: {
                    fontSize: '8px',
                    color: '#deaf54',
                },
                y: 2,
                x: 3
            },
            gridLineWidth: 0,
            opposite: true,
            showLastLabel: false
        }],

        legend: {
            enabled: false
        },

        plotOptions: {
            series: {
                pointPlacement: 'between'
            }
        },


        series: [
            {
            name: 'Temperature',
            data: this.temperatures,
            type: 'spline',
            marker: {
                enabled: false,
                states: {
                    hover: {
                        enabled: true
                    }
                }
            },
            tooltip: {
                pointFormat: '<span style="color:{point.color}">\u25CF</span> ' +
                    '{series.name}: <b>{point.y}°C</b><br/>'
            },
            zIndex: 1,
            color: '#FF3333',
            negativeColor: '#48AFE8'
        },  {

                type: 'column',
                pointWidth: 7,
                data: this.hum,
                dataLabels: {
                    enabled: true,
                    style: {
                        fontSize: '8px',
                        fontWeight: 'normal'
                    }
                },
                tooltip: {
                    pointFormat: '<span style="color:{point.color}">\u25CF</span> ' +
                        'Humidity: <b>{point.y}%</b><br/>'

                },
                //colorByPoint: true
            },
            {
            name: 'Air pressure',
            color: Highcharts.getOptions().colors[2],
            data: this.pressures,
            marker: {
                enabled: false
            },
            color: '#deaf54',
            shadow: false,
            tooltip: {
                valueSuffix: ' inHg'
            },
            dashStyle: 'shortdot',
            yAxis: 2
        }, {
            name: 'Wind',
            type: 'windbarb',
            id: 'windbarbs',
            lineWidth: 1.5,
            data: this.winds,
            vectorLength: 10,
            color: '#000',
            yOffset: -15,
            xOffset:-5,
        }]

    };
};

/**
 * Post-process the chart from the callback function, the second argument
 * Highcharts.Chart.
 */
Meteogram.prototype.onChartLoad = function (chart) {

    this.drawBlocksForWindArrows(chart);

};

/**
 * Create the chart. This function is called async when the data file is loaded
 * and parsed.
 */
Meteogram.prototype.createChart = function () {
    this.chart = new Highcharts.Chart(this.getChartOptions(), chart => {
        this.onChartLoad(chart);
    });
};


/**
 * Handle the data. This part of the code is not Highcharts specific, but deals
 * with yr.no's specific data format
 */
Meteogram.prototype.parseYrData = function () {

    let pointStart;

    if (!this.json) {
        console.log("not json")
        return this.error();
    } else {
        console.log("is json")
    }

    // Loop over hourly (or 6-hourly) forecasts
    this.json.forEach((node, i) => {
        const timeformat = node.startTime.substring(0, 19);
        const x = Date.parse(timeformat) - 7 * 36e5,
            to = x + 36e5;

        // Populate the parallel arrays
        this.temperatures.push({
            x,
            y: node.values["temperature"],
            // custom options used in the tooltip formatter
            to,
            format: timeformat
        });


        if (i % 2 === 0) {
            this.winds.push({
                x,
                value: node.values["windSpeed"],
                direction: node.values["windDirection"],
                format: timeformat
            });
        }
        this.hum.push({
            x,
            y: Math.floor(node.values["humidity"]),
            format: timeformat
        });
        this.pressures.push({
            x,
            y: node.values["pressureSeaLevel"],
            format: timeformat
        });

        if (i === 0) {
            pointStart = (x + to) / 2;
        }
    });

    // Create the chart when the data is loaded
    this.createChart();
};