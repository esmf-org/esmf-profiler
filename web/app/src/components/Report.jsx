import ChartContainer from "./ChartContainer";
import Stacked from "../charts/Stacked";
import Sidebar from "./SideBar";
import React, { useState, useEffect } from "react";

import { Helmet } from "react-helmet-async";

function Report() {
  const [data, setData] = useState({});
  const [title, setTitle] = useState();

  useEffect(()=>{

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

       fetch("data/site.json")
         .then(function (res) {
          //console.log("site response = " + res)
          return res.json();
        })
        .then(function (_site) {
          //console.log("setting title")
          setTitle(_site.name + " - ESMF Profiler");
        })
        .catch(function (err) {
          console.log(err, "Error loading data/site.json");
        });
  }, []);

  return (
    <div className="App">
      <Helmet title={title}></Helmet>
      <div id="wrapper">
        <Sidebar />
        <div id="content-wrapper" className="d-flex flex-column">
          <div id="content">
            <div className="container-fluid bg-white">
              <div className="d-sm-flex align-items-center justify-content-between mb-4">
                <h1 className="h3 mb-0 text-gray-800"></h1>
              </div>

              <div className="row">
                  <ChartContainer>
                    <Stacked options={data} />
                  </ChartContainer>
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
