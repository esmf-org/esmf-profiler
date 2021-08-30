import Highcharts from 'highcharts';

export default class StackedChart {
    constructor(container, chartObject) {
        this.containerNameString = container;
        this.chartObject = chartObject;
    }

    render() {
        Highcharts.chart(this.containerNameString, this.chartObject);
    }
}
