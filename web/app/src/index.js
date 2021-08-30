import Highcharts from 'highcharts';
import StackedChart from './charts'
import "./style.scss";

const chartConfig = {
    chart: {
        type: "column", // column / bar
    },
    title: {
        text: "ESMF Profiler", // graph title
    },
    xAxis: {
        categories: ["ESM", "ABC"], // single bar label
    },
    yAxis: {
        min: 0,
        allowDecimals: false,
        title: {
            text: "Execution Times (in nanoseconds)",
        },
    },
    legend: {
        reversed: true,
    },
    plotOptions: {
        series: {
            stacking: "normal",
        },
    },
    series: [
        {
            name: "OCN",
            data: [0.8344, 2],
        },
        {
            name: "MED",
            data: [0.8203, 1.5],
        },
        {
            name: "ATM",
            data: [0.6387],
        },
        {
            name: "ATM-TO-MED",
            data: [0.5975],
        },
    ],
};

const chart = new StackedChart("container2", chartConfig)
chart.render()

