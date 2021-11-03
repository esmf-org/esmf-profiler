import ChartContainer from "./ChartContainer";
import Stacked from "../charts/Stacked";
import Sidebar from "./SideBar";
import React, { useState, useEffect } from "react";
import axios from "axios";

import { Helmet } from "react-helmet-async";

function Report() {
  const [data, setData] = useState(undefined);
  const [site, setSite] = useState({
    name: "",
    timestamp: "",
  });

  const headers = {
    "Access-Control-Allow-Origin": "*",
  };

  useEffect(() => {
    _fetchData();
    _fetchSite();
  }, []);

  const _fetchData = (path) => {
    axios
      .get("data/load_balance.json")
      .then((resp) => setData(() => resp.data))
      .catch((err) => console.log(err));
  };

  const _fetchSite = (path) => {
    axios
      .get("data/site.json")
      .then((resp) => setSite(() => resp.data))
      .catch((err) => console.log(err));
  };

  return (
    <div className="App">
      <Helmet title={`${site ? site.name : ""} - ESMF Profiler`}></Helmet>
      <div id="wrapper">
        <Sidebar />
        <div id="content-wrapper" className="d-flex flex-column">
          <div id="content">
            <div className="container-fluid bg-white">
              <div className="d-sm-flex align-items-center justify-content-between mb-4">
                <h1 className="h3 mb-0 text-gray-800">
                  {site ? site.name : ""}
                </h1>
                <sup>{site ? site.timestamp : ""}</sup>
              </div>

              <div className="row">
                {data && (
                  <ChartContainer>
                    <Stacked options={data} />
                  </ChartContainer>
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
