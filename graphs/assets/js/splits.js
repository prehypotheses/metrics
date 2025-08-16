
$.getJSON('../../warehouse/numerics/abstracts/tree.json', function (data) {

    let cluster,
        split_index = 0,
        section_index,
        annotation_index,
        split_point,
        section_point,
        annotation_point,
        split,
        section,
        annotation;

    const points = [],
        annotationName = {
            miscellaneous: 'Miscellaneous',
            beginning: 'Beginning',
            inside: 'Inside'
        };

    for (split in data) {
        if (Object.hasOwnProperty.call(data, split)) {
            cluster = 0;
            split_point = {
                id: 'id_' + split_index,
                name: split,
                color: Highcharts.getOptions().colors[split_index]
            };
            section_index = 0;
            for (section in data[split]) {
                if (Object.hasOwnProperty.call(data[split], section)) {
                    section_point = {
                        id: split_point.id + '_' + section_index,
                        name: section,
                        parent: split_point.id
                    };
                    points.push(section_point);
                    annotation_index = 0;
                    for (annotation in data[split][section]) {
                        if (Object.hasOwnProperty.call(
                            data[split][section], annotation
                        )) {
                            annotation_point = {
                                id: section_point.id + '_' + annotation_index,
                                name: annotationName[annotation],
                                parent: section_point.id,
                                value: Math.round(+data[split][section][annotation])
                            };
                            cluster += annotation_point.value;
                            points.push(annotation_point);
                            annotation_index = annotation_index + 1;
                        }
                    }
                    section_index = section_index + 1;
                }
            }
            split_point.value = Math.round(cluster / section_index);
            points.push(split_point);
            split_index = split_index + 1;
        }
    }


    Highcharts.chart('container', {
        series: [{
            name: 'Splits',
            type: 'treemap',
            layoutAlgorithm: 'squarified',
            allowDrillToNode: true,
            animationLimit: 1000,
            dataLabels: {
                enabled: false
            },
            levels: [{
                level: 1,
                dataLabels: {
                    enabled: true
                },
                borderWidth: 3,
                levelIsConstant: false
            }, {
                level: 1,
                dataLabels: {
                    style: {
                        fontSize: '13px'
                    }
                }
            }],
            accessibility: {
                exposeAsGroupOnly: true
            },
            data: points
        }],
        subtitle: {
            text: 'Click points to drill down. Source: <a href="https://github.com/membranes/numerics">numerics</a>.',
            align: 'left'
        },
        title: {
            text: 'The training, validating, testing split.',
            align: 'left'
        }
    });


}).fail(function () {
    console.log("Missing");
    $('#container').empty();
});
