import Highcharts, { XrangePointOptionsObject } from "highcharts";

var defaultConfig = {
  chart: {
    plotBackgroundColor: null,
    plotBorderWidth: null,
    plotShadow: false,
    type: "pie",
  },
  title: {
    text: "Browser market shares in January, 2018",
  },
  tooltip: {
    pointFormat: "{series.name}: <b>{point.percentage:.1f}%</b>",
  },
  accessibility: {
    point: {
      valueSuffix: "%",
    },
  },
  plotOptions: {
    pie: {
      allowPointSelect: true,
      cursor: "pointer",
      dataLabels: {
        enabled: true,
        format: "<b>{point.name}</b>: {point.percentage:.1f} %",
      },
    },
  },
  series: [
    {
      name: "Brands",
      colorByPoint: true,
      data: [
        {
          name: "Chrome",
          y: 61.41,
          sliced: true,
          selected: true,
        },
        {
          name: "Internet Explorer",
          y: 11.84,
        },
        {
          name: "Firefox",
          y: 10.85,
        },
        {
          name: "Edge",
          y: 4.67,
        },
        {
          name: "Safari",
          y: 4.18,
        },
        {
          name: "Sogou Explorer",
          y: 1.64,
        },
        {
          name: "Opera",
          y: 1.6,
        },
        {
          name: "QQ",
          y: 1.2,
        },
        {
          name: "Other",
          y: 2.61,
        },
      ],
    },
  ],
};

interface IChartTypes {
  type: "column" | "bar" | "line";
}

interface IPie {
  chart?: IChartTypes;
  title?: {
    text: string;
  };
  subtitle?: {
    text: string;
  };
  xAxis?: {
    categories: any[];
    crosshair?: boolean;
  };
  yAxis?: {
    min: number;
    title: {
      text: string;
    };
  };
  tooltip?: {
    headerFormat?: string;
    pointFormat?: string;
    footerFormat?: string;
    shared?: boolean;
    useHTML?: boolean;
  };
  plotOptions?: {
    column: {
      pointPadding?: number;
      borderWidth?: number;
    };
  };
  series?: any;
}

export default class Pie {
  containerNameString: string;
  chartConfig: object;

  constructor(container: string, chartObject: IPie) {
    this.containerNameString = container;

    this.chartConfig = {
      ...defaultConfig,
      ...chartObject,
    };
  }

  render(): Pie {
    Highcharts.chart(this.containerNameString, this.chartConfig);
    return this;
  }
}
