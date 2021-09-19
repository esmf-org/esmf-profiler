import Stacked from "./charts/Stacked";
import Comparison from "./charts/Comparison";
import BasicBar from "./charts/BasicBar";

import "../styles/sb-admin-2.scss";
import rawData from "./charts/data.json";
import DrillDown from "./charts/DrillDown";
import { chart } from "highcharts";

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

  categories() {
    return new Set(
      this.seriesData.map((x) => {
        return x["petId"];
      }, this.seriesData)
    );
  }

  parse() {
    let valuesMap = {};
    for (let point of this.seriesData) {
      let petId = point["petId"];
      if (!valuesMap.hasOwnProperty(petId)) {
        valuesMap[petId] = [];
      }
      valuesMap[petId].push(point["data"]);
    }

    let test = Object.entries(valuesMap).map((x, y) => {
      console.log(x, y);
      return {
        name: x[0],
        data: x[1],
      };
    });

    console.log(test);
    return test;

    const points = this.seriesData.map((dataPoint) => {
      return {
        name: dataPoint["petId"],
        value: dataPoint["data"],
      };
    });
    return [];
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

new Stacked("container2", chartConf).render();

const chart2 = new Comparison("container", {});
chart2.render();
const chart3 = new BasicBar("basic-bar-container", {});
chart3.render();
const chart4 = new DrillDown("drill-down-container", {});
chart4.render();
