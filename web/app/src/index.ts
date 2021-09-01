import Stacked from "./charts/Stacked";
import Comparison from "./charts/Comparison";
import BasicBar from "./charts/BasicBar";

import "./style.scss";
import DrillDown from "./charts/DrillDown";
import { chart } from "highcharts";

const chartConfig = {
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

const chart2 = new Comparison("container", {});
chart2.render();
const chart1 = new Stacked("container2", chartConfig);
chart1.render();
const chart3 = new BasicBar("basic-bar-container", {});
chart3.render();
const chart4 = new DrillDown("drill-down-container", {});
chart4.render();

const chart5 = new BasicBar("container", {}).render();
chart5.render();
console.log(chart5.chartConfig);
