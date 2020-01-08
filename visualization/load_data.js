var config_dict = {}; 
var chart;
var fontSize = 18;

var starting_config = { 
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true,
                    fontSize: fontSize
                }
            }],
            xAxes: [{
                ticks: {fontSize: fontSize}
            }]
        },
        legend: {
            align: 'center',
            position: 'bottom',
            labels: {fontSize: fontSize}
        }
    }
}


function setUp(is1x) {
    var folder = is1x ? "./data/1x/" : "./data/2x/";
    var folder2 = is1x ? "./data/2x/" : "./data/1x/";
    d3.csv(folder + 'engagement.csv').then(loadData1);
    d3.csv(folder + 'gender.csv').then(loadData3);
    d3.csv(folder + 'age.csv').then(loadData4);
    d3.csv(folder + 'age_semester.csv').then(loadData5);
    d3.csv(folder + 'education.csv').then(loadData6);
    d3.csv(folder + 'promo.csv').then(loadData7);
    d3.csv(folder + 'engagement_by_grade.csv').then(loadData8);
    d3.csv("./data/certified.csv").then(loadData9);


    d3.csv(folder2 + 'age.csv').then(loadIntroVsAdvancedAge, is1x);
}

function loadData9(data) {
    var config = JSON.parse(JSON.stringify(starting_config));
    config.type = "bar";
    config.data = {
            labels: ["oveall grade", "active days", "videos", "forum events"],
            datasets: [{
                label: 'Verified',
                backgroundColor: '#0d3473',
                borderColor: '#0d3473',
                data: data.map(function(d) {return d.Verified}),
            }, 
            {
                label: 'Non-verified',
                backgroundColor: '#a9c9f4',
                borderColor: '#a9c9f4',
                data: data.map(function(d) {return d.NonVerified}),
            }] 
        };
    config_dict["overall_certified"] = config;
}

function loadData8(data) {
    var config = JSON.parse(JSON.stringify(starting_config));
    config.type = "line";
    config.data = {
            labels: data.map(function(d) {return d.Bin}),
            datasets: [{
                label: 'active days',
                backgroundColor: '#204bfd',
                borderColor: '#204bfd',
                data: data.map(function(d) {return d.ActiveDays}),
                fill: false
            }, 
            {
                label: 'videos watched',
                backgroundColor: '#8aacf6',
                borderColor: '#8aacf6',
                data: data.map(function(d) {return d.Videos}),
                fill: false
            }, 
            {
                label: 'forum events',
                backgroundColor: '#03204f',
                borderColor: '#03204f',
                data: data.map(function(d) {return d.Forum}),
                fill: false
            }, ]
        };
    config_dict["overall_by_grade"] = config;
}



function loadData7(data) {
    var config = JSON.parse(JSON.stringify(starting_config));
    config.type = "bar";

    config.data = {
        labels: data.map(function(d) {return d.Semester}),
        datasets: [
        {
            label: 'total registered',
            data: data.map(function(d) {return d.Registered}),
            backgroundColor: '#0e3576',
            borderColor: '#0e3576',
            fill: false,
            type: 'line',
            yAxisID: 'A',
        },
        {
            label: 'number of promo emails',
            data: data.map(function(d) {return d.TotalPromo}),
            backgroundColor: '#c9e6f2',
            borderColor: '#c9e6f2',
            yAxisID: 'B',
        }]
    };

    config.options.scales.yAxes = [
        {
            id: 'A',
            ticks: {beginAtZero: true, fontSize: fontSize},
            position: 'left',
            scaleLabel: {
                display: true,
                labelString: 'Number of learners',
                fontSize: fontSize
              }
        },
        {
            id: 'B',
            ticks: {beginAtZero: true, fontSize: fontSize},
            position: 'right',
            scaleLabel: {
                display: true,
                labelString: 'Number of emails',
                fontSize: fontSize
              }
        }
    ]

    config_dict["monetary_promo"] = config;
}

function loadData6(data) {
    var config = JSON.parse(JSON.stringify(starting_config));
    config.type = "pie";

    var keys = Object.keys(data[0]);
    var values = keys.map(function(key){return data[0][key];});

    config.data = {
        labels: keys,
        datasets: [{
            data: values,
        }]
    }

    config_dict["demo_education"] = config;
}

function loadIntroVsAdvancedAge(data, is1x) {
    var config = JSON.parse(JSON.stringify(starting_config));
    config.type = "bar";

    config.data = {
            labels: data.map(function(d) {return d.Range}),
            datasets: [
            {
                label: (is1x ? '2x' : '1x'),
                data: config_dict["demo_age_agg"].data.datasets[0].data,
                backgroundColor: '#0e3576',
                borderColor: '#0e3576',
            },
            {
                label: (is1x ? '1x' : '2x'),
                data: data.map(function(d) {return d.Number}),
                backgroundColor: '#c9e6f2',
                borderColor: '#c9e6f2',
            }]
        };
    config_dict["level_age"] = config;

}


function loadData1(data) {
    var config = JSON.parse(JSON.stringify(starting_config));
    config.type = "bar";
    config.data = {
            labels: data.map(function(d) {return d.Semester}),
            datasets: [{
                label: 'viewed',
                backgroundColor: '#204bfd',
                borderColor: '#204bfd',
                data: data.map(function(d) {return d.ViewedPercent})
            }, 
            {
                label: 'explored',
                backgroundColor: '#8aacf6',
                borderColor: '#8aacf6',
                data: data.map(function(d) {return d.ExploredPercent})
            }, 
            {
                label: 'completed',
                backgroundColor: '#03204f',
                borderColor: '#03204f',
                data: data.map(function(d) {return d.CompletedPercent})
            }, ]
        };
    config_dict["overall_per"] = config;

    var config = JSON.parse(JSON.stringify(starting_config));
    config.type = "bar";
    config.data = {
            labels: data.map(function(d) {return d.Semester}),
            datasets: [{
                label: 'registered',
                backgroundColor: '#c9e6f2',
                borderColor: '#c9e6f2',
                data: data.map(function(d) {return d.Registered})
            }, 
            {
                label: 'viewed',
                backgroundColor: '#204bfd',
                borderColor: '#204bfd',
                data: data.map(function(d) {return d.Viewed})
            }, 
            {
                label: 'explored',
                backgroundColor: '#8aacf6',
                borderColor: '#8aacf6',
                data: data.map(function(d) {return d.Explored})
            }, 
            {
                label: 'completed',
                backgroundColor: '#03204f',
                borderColor: '#03204f',
                data: data.map(function(d) {return d.Completed})
            }, ]
        };
    config_dict["overall_raw"] = config;
}

function loadData3(data) {
    var config = JSON.parse(JSON.stringify(starting_config));
    config.type = "line";
    config.data = {
            labels: data.map(function(d) {return d.Semester}),
            datasets: [{
                label: 'female',
                data: data.map(function(d) {return d.Female}),
                fill: false,
                borderColor: '#0e3576',
                backgroundColor: '#0e3576',
                borderWidth: 8
            }, 
            {
                label: 'male',
                data: data.map(function(d) {return d.Male}),
                fill: false,
                borderColor: '#c9e6f2',
                backgroundColor: '#c9e6f2',
                borderWidth: 8
            }]
        };
    config_dict["demo_gender"] = config;
}

function loadData4(data) {
    var config = JSON.parse(JSON.stringify(starting_config));
    config.type = "bar";
    config.data = {
            labels: data.map(function(d) {return d.Range}),
            datasets: [{
                label: "Number of learners",
                data: data.map(function(d) {return d.Number}),
                backgroundColor: '#c9e6f2',
                borderColor: '#c9e6f2',
            }]
        };
    config_dict["demo_age_agg"] = config;
}

function loadData5(data) {
    var config = JSON.parse(JSON.stringify(starting_config));
    config.type = "line";
    var datasets = []
    for (var i in data) {
        if (i === 'columns') {
            continue;
        }
        var values = Object.keys(data[i]).map(function(key){return data[i][key];});
        var dataset = {
            label: data[i].Semester,
            data: values.slice(1),
            fill: false,
            borderColor: getRandomColor()
        }
        datasets.push(dataset);
    }

    config.data = {
            labels: Object.keys(data[0]).slice(1),
            datasets: datasets
        };
    config_dict["demo_age_sem"] = config;
}