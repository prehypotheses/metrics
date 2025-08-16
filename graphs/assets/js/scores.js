// noinspection DuplicatedCode

var Highcharts;
var optionSelected;
var dropdown = $('#option_selector');

var url = '../assets/menu/scores.json'


// Menu details
$.getJSON(url, function (data) {

    $.each(data, function (key, entry) {
        dropdown.append($('<option></option>').attr('value', entry.desc).text(entry.name));
    });

    // Load the first Option by default
    var defaultOption = dropdown.find("option:first-child").val();
    optionSelected = dropdown.find("option:first-child").text();

    // Generate
    generateChart(defaultOption);

});



// Dropdown
dropdown.on('change', function (e) {

    $('#option_selector_title').remove();

    // Save name and value of the selected option
    optionSelected = this.options[e.target.selectedIndex].text;
    var valueSelected = this.options[e.target.selectedIndex].value;

    //Draw the Chart
    generateChart(valueSelected);
});


function generateChart(fileNameKey) {


    $.getJSON('../../warehouse/numerics/card/spider/' + fileNameKey + '.json', function (calculations) {

        // https://api.highcharts.com/highstock/tooltip.pointFormat
        // https://jsfiddle.net/gh/get/library/pure/highcharts/highcharts/tree/master/samples/highcharts/demo/bubble
        // https://api.highcharts.com/highcharts/tooltip.headerFormat
        // https://www.highcharts.com/demo/stock/compare


        // Categories
        var categories = calculations.columns;

        // Selection's data
        var seriesOptions = [];

        // Curves
        for (var i = 0; i < calculations.data.length; i += 1) {

            seriesOptions[i] = {
                name: calculations.index[i][0],
                visible: true,
                data: calculations.data[i],
                pointPlacement: 'on'
            }

        }

        // Container
        Highcharts.chart('container', {

            chart: {
                polar: true,
                type: 'spline',
                marginTop: 105
            },

            title: {
                text: '<span style="font-size: 13px">Error Matrix Metrics</span>',
                x: 0
            },
            subtitle: {
                text: '\nEntity: <b>' + fileNameKey + '</b>\n',
                style: {
                    "fontSize": "11px",
                    "fontWeight": "light"
                }
            },

            credits: {
                enabled: false
            },

            // https://api.highcharts.com/highcharts/xAxis.tickmarkPlacement
            xAxis: {
                categories: categories,
                tickmarkPlacement: 'on',
                lineWidth: 0
            },

            // https://api.highcharts.com/highcharts/yAxis.gridLineInterpolation
            // https://api.highcharts.com/highcharts/yAxis.min
            yAxis: {
                gridLineInterpolation: 'polygon',
                lineWidth: 0,
                min: 0,
                max: 1,
                tickInterval: 0.5
            },

            legend: {
                align: 'center',
                verticalAlign: 'bottom',
                layout: 'vertical',
                width: '57.5%',
                margin: 25,
                itemMarginTop: 2,
                itemMarginBottom: 2,
                y: 25,
                x: 25
            },

            // https://api.highcharts.com/highcharts/pane
            pane: {
                size: '75%' // diagram only
            },

            tooltip: {
                shared: true,
                pointFormat: '<span style="color:{series.color}">{series.name}: <b>{point.y:,.2f}</b><br/>'
            },

            plotOptions: {
                spline: {
                    lineWidth: 1,
                    marker: {
                        radius: 3
                    }
                }
            },

            series: seriesOptions,

            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 600
                    }
                }]
            }

        });

    }).fail(function () {
        console.log("Missing");
        $('#container').empty();
    });


}

