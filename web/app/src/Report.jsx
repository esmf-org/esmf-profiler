import "./styles/main.scss";

import ChartContainer from "./components/ChartContainer";
import Stacked from "./charts/Stacked";
import Sidebar from "./components/SideBar";
import Footer from "./components/Footer";
import data from "./data.json";
import { Helmet } from "react-helmet-async";

const defaultConfig = {
  chart: {
    type: "column", // column / bar
    zoomType: "xy",
  },
  title: {
    text: "PET Timings", // graph title
  },
  xAxis: {
    categories: data.xvals, // single bar label
    title: {
      text: "PET Number",
    },
  },
  yAxis: {
    min: 0,
    allowDecimals: false,
    title: {
      text: "Time (s)",
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
  series: data.yvals,
};

function Report() {
  return (
    <div className="App">
      <Helmet title={Date.now().toString()}></Helmet>
      <div id="wrapper">
        <Sidebar />
        <div id="content-wrapper" className="d-flex flex-column">
          <div id="content">
            <div className="container-fluid">
              <div className="d-sm-flex align-items-center justify-content-between mb-4">
                <h1 className="h3 mb-0 text-gray-800"></h1>
              </div>

              <div className="row">
                <ChartContainer>
                  <Stacked config={defaultConfig} />
                </ChartContainer>
              </div>
            </div>
          </div>

          <Footer />
        </div>
      </div>
    </div>
  );
}

export default Report;
