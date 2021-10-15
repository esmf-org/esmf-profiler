import ChartContainer from "./ChartContainer";
import Stacked from "../charts/Stacked";
import Sidebar from "./SideBar";
import React, { useState, useEffect } from "react";

import { Helmet } from "react-helmet-async";

function Report() {
  const [data, setData] = useState(undefined);
  const [site, setSite] = useState({
    name: "",
    timestamp: "",
  });

  useEffect(() => {
    fetchData();
    fetchSite();
  }, []);

  const _fetchData = async (path) => {
    try {
      let res = await fetch("data/load_balance.json");
      return await res.json();
    } catch (error) {
      console.log(error);
    }
  };

  const fetchData = async () => {
    let data = await _fetchData();
    setData(() => data);
  };

  const fetchSite = async () => {
    let data = await _fetchSite();
    setSite(() => data);
  };

  const _fetchSite = async (path) => {
    try {
      let res = await fetch("data/site.json");
      return await res.json();
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="App">
      <Helmet title={`${site.name} - ESMF Profiler`}></Helmet>
      <div id="wrapper">
        <Sidebar />
        <div id="content-wrapper" className="d-flex flex-column">
          <div id="content">
            <div className="container-fluid bg-white">
              <div className="d-sm-flex align-items-center justify-content-between mb-4">
                <h1 className="h3 mb-0 text-gray-800">{site.name}</h1>
                <sup>{site.timestamp}</sup>
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
