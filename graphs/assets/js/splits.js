
$.getJSON('../../warehouse/metrics/abstracts/tree.json', function (data) {



    Highcharts.chart('container', {
        series: [{
            name: 'Splits',
            type: 'treemap',
            allowTraversingTree: true,
            alternateStartingDirection: true,
            dataLabels: {
                format: '{point.name}',
                style: {
                    textOutline: 'none'
                }
            },
            borderRadius: 3,
            nodeSizeBy: 'leaf',
            levels: [{
                level: 1,
                layoutAlgorithm: 'sliceAndDice',
                groupPadding: 3,
                dataLabels: {
                    headers: true,
                    enabled: true,
                    style: {
                        fontSize: '0.6em',
                        fontWeight: 'normal',
                        textTransform: 'uppercase',
                        color: 'var(--highcharts-neutral-color-100, #000)'
                    }
                },
                borderRadius: 3,
                borderWidth: 1,
                colorByPoint: true

            }, {
                level: 2,
                dataLabels: {
                    enabled: true,
                    inside: false
                }
            }],
            accessibility: {
                exposeAsGroupOnly: true
            },
            data: data
        }],
        subtitle: {
            text: 'Click points to drill down; <a href="https://github.com/prehypotheses/metrics/graphs/assets/js/splits.js">code</a>.',
            align: 'left'
        },
        title: {
            text: 'The training, validating, testing split.',
            align: 'left'
        },
        tooltip: {
            useHTML: true,
            pointFormat: 'The frequency of <b>{point.name}</b> is \
            <b>{point.value}</b>'
        }
    });


}).fail(function () {
    console.log("Missing");
    $('#container').empty();
});
