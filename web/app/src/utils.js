export default class StackedChart {
    constructor(container, chartObject) {
        this.containerNameString = container
        this.chartObject = chartObject
    }

    render() {
        Highcharts.chart(containerNameString, chartObject)
    }
}
