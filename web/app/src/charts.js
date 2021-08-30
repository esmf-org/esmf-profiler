import Highcharts from 'highcharts';

export default class StackedChart {
    constructor(container, chartObject) {
        this.containerNameString = container;
        this.defaultConfig = {
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
        this.chartConfig = {
            ...this.defaultConfig,
            ...chartObject
        }
    }

    render() {
        Highcharts.chart(this.containerNameString, this.chartConfig);
    }
}
