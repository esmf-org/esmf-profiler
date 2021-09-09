import Stacked from "./charts/Stacked";
import Comparison from "./charts/Comparison";
import BasicBar from "./charts/BasicBar";

import "./style.scss";
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

class StackedDataPoint {
  jsonData: string;

  constructor(jsonData: string) {
    this.jsonData = jsonData;
  }

  parse() {
    let data = JSON.parse(this.jsonData);

    return {
      name: data["id"],
      data: parseInt(data["total"]),
      petId: data["pet"],
    };
  }
}

function getData(): any[] {
  const dataPoints = rawData.map((x) => {
    return new StackedDataPoint(x).parse();
  });
  console.log(dataPoints);
  const stackedDataChart = new StackedDataChart(dataPoints);
  return stackedDataChart.parse();
}

const chartConf = {
  title: {
    text: "Default Title", // graph title
  },
  xAxis: {
    categories: ["PET_0", "PET_1"], // single bar label
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
  series: getData(),
};

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

const chart1 = new Stacked("container2", chartConf).render();
const chart2 = new Comparison("container", {});
chart2.render();
const chart3 = new BasicBar("basic-bar-container", {});
chart3.render();
const chart4 = new DrillDown("drill-down-container", {});
chart4.render();
