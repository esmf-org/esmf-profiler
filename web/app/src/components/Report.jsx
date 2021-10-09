import ChartContainer from "./ChartContainer";
import Stacked from "../charts/Stacked";
import Sidebar from "./SideBar";
import React, { useState } from "react";
import Footer from "./Footer";

import { Helmet } from "react-helmet-async";
import AlertDismissible from "./alerts/AlertDismissible";

function Report() {
  const [data, setData] = useState();
  const [timeStamp, setTimeStamp] = useState(Date.now().toString());

  // Fetch Function
  fetch("data/load_balance.json")
    .then(function (res) {
      return res.json();
    })
    .then(function (_data) {
      setData(_data);
    })
    .catch(function (err) {
      console.log(err, "Error loading JSON data");
    });

  return (
    <div className="App">
      <Helmet title={timeStamp}></Helmet>
      <div id="wrapper">
        <Sidebar />
        <div id="content-wrapper" className="d-flex flex-column">
          <div id="content">
            <div className="container-fluid bg-white">
              <div className="d-sm-flex align-items-center justify-content-between mb-4">
                <h1 className="h3 mb-0 text-gray-800"></h1>
              </div>

              <div className="row">
                <AlertDismissible />
                {data ? (
                  <ChartContainer>
                    <Stacked options={data} />
                  </ChartContainer>
                ) : (
                  <div>{data}</div>
                )}
              </div>
            </div>
          </div>

          {/* <Footer /> */}
        </div>
      </div>
    </div>
  );
}

export default Report;
