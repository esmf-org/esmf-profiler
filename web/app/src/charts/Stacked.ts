import Highcharts from "highcharts";

const defaultConfig = {
  chart: {
    type: "column", // column / bar
    zoomType: "xy",
  },
  title: {
    text: "Default Title", // graph title
  },
  xAxis: {
    categories: ["Category_1", "Category_2"], // single bar label
  },
  yAxis: {
    min: 0,
    allowDecimals: false,
    title: {
      text: "Default Title",
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
      name: "SubCategory 1",
      data: [1.8344, 2],
    },
    {
      name: "SubCategory 2",
      data: [2.8203, 1.5],
    },
    {
      name: "SubCategory 3",
      data: [6.6387],
    },
    {
      name: "SubCategory 4",
      data: [7.5975],
    },
  ],
};

export default class Stacked {
  containerNameString: string;
  chartConfig: object;
  chart: any;
  constructor(container: string, chartObject: {}) {
    this.containerNameString = container;
    this.chartConfig = {
      ...defaultConfig,
      ...chartObject,
    };
    this.chart = null;
  }

  render(): Stacked {
    this.chart = Highcharts.chart(this.containerNameString, this.chartConfig);
    return this;
  }
}
