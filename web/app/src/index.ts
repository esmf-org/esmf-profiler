import Stacked from "./charts/Stacked";
import Comparison from "./charts/Comparison";
import BasicBar from "./charts/BasicBar";

import "../styles/sb-admin-2.scss";
import rawData from "./charts/data.json";
import DrillDown from "./charts/DrillDown";
import { chart } from "highcharts";
import Pie from "./charts/Pie";

interface IStackedDataPoint {
  name: string;
  data: number;
  petId: number;
}

class StackedDataChart {
  seriesData: IStackedDataPoint[];
  constructor(seriesData: IStackedDataPoint[]) {
    this.seriesData = seriesData;
  }
}

const chartConf = {
  title: {
    text: "Default Title", // graph title
  },

  xAxis: {
    categories: rawData["xvals"],
  },
  yAxis: {
    min: 0,
    allowDecimals: false,
    title: {
      text: "Stacked Test Chart",
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
  series: rawData["yvals"],
};

new Stacked("myAreaChart", chartConf).render();
new Pie("myPieChart", {}).render();
// const chart2 = new Comparison("container", {});
// chart2.render();
// const chart3 = new BasicBar("basic-bar-container", {});
// chart3.render();
// const chart4 = new DrillDown("drill-down-container", {});
// chart4.render();
