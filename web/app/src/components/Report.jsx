import ChartContainer from "./ChartContainer";
import Stacked from "../charts/Stacked";
import Sidebar from "./SideBar";
import React, { useState, useEffect } from "react";

import { Helmet } from "react-helmet-async";

function Report() {
  const [data, setData] = useState();
  const [title, setTitle] = useState({
    title: "",
    timestamp: "",
  });

  useEffect(() => {
    // Fetch Function
    fetch("data/load_balance.json")
      .then(function (res) {
        //console.log("lb response")
        return res.json();
      })
      .then(function (_data) {
        //console.log("lb setData")
        setData(_data);
      })
      .catch(function (err) {
        console.log(err, "Error loading data/load_balance.json");
      });
  }, []);

  useEffect(() => {
    fetch("data/site.json")
      .then(function (res) {
        return res.json();
      })
      .then(function (_site) {
        setTitle({
          title: _site.name,
          timestamp: _site.timestamp,
        });
      })
      .catch(function (err) {
        console.log(err, "Error loading data/site.json");
      });
  }, []);

  return (
    <div className="App">
      <Helmet title={`${title.title} - ESMF Profiler`}></Helmet>
      <div id="wrapper">
        <Sidebar />
        <div id="content-wrapper" className="d-flex flex-column">
          <div id="content">
            <div className="container-fluid bg-white">
              <div className="d-sm-flex align-items-center justify-content-between mb-4">
                <h1 className="h3 mb-0 text-gray-800">{title.title}</h1>
                <sup>{title.timestamp}</sup>
              </div>

              <div className="row">
                {data && <ChartContainer>
                  <Stacked options={data} />
                </ChartContainer> }
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
