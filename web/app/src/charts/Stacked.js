import Highcharts from 'highcharts';

const defaultConfig = {
    chart: {
        type: "column", // column / bar
    },
    title: {
        text: "Default Title", // graph title
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
};

export default class Stacked {
    constructor(container, chartObject) {
        this.containerNameString = container;

        this.chartConfig = {
            ...defaultConfig,
            ...chartObject
        }
    }

    render() {
        Highcharts.chart(this.containerNameString, this.chartConfig);
    }
}
