import Stacked from "../charts/Stacked";
import Sidebar from "./SideBar";
import React, { useState, useEffect } from "react";

import { Helmet } from "react-helmet-async";
import { appName } from "../constants";
import ChartContainer from "../charts/ChartContainer";

function Page(props) {
  return (
    <React.Fragment>
      <div id="wrapper">{props.children}</div>
    </React.Fragment>
  );
}

function Header(props) {
  return (
    <React.Fragment>
      <div className="d-sm-flex align-items-center justify-content-between mb-4">
        <h1 className="h3 mb-0 text-gray-800">{props ? props.name : ""}</h1>

        <sup>{props ? props.timestamp : ""}</sup>
      </div>
    </React.Fragment>
  );
}

function ContentContainer(props) {
  return (
    <React.Fragment>
      <div className="container-fluid bg-white">{props.children}</div>
    </React.Fragment>
  );
}

function Chart(props) {
  // TODO: Dyamically change charts
  if (props.data) {
    return (
      <ChartContainer>
        <Stacked size={props.size ? props.size : 12} options={props.data} />
      </ChartContainer>
    );
  }
  return null;
}

function Report() {
  const [data, setData] = useState(undefined);
  const [site, setSite] = useState({
    name: "",
    timestamp: "",
  });

  useEffect(() => {
    _fetchData();
    _fetchSite();
  }, []);

  const _fetchData = () => {
    fetch("data/load_balance.json")
      .then((resp) => resp.json())
      .then((data) => {
        setData(() => data);
      })
      .catch((err) => console.log(err));
  };

  const _fetchSite = () => {
    fetch("data/site.json")
      .then((resp) => resp.json())
      .then((data) => {
        setSite(() => data);
      })
      .catch((err) => console.log(err));
  };

  const title = (name) => `${name ? name : ""} - ${appName}`;

  return (
    <div className="App">
      <Helmet title={title(site.name)}></Helmet>
      <Page>
        <Sidebar />
        <ContentContainer>
          <Header name={site.name} timestamp={site.timestamp} />
          <div className="row">
            <Chart data={data} size={12} />
          </div>
        </ContentContainer>
      </Page>
    </div>
  );
}

export default Report;
