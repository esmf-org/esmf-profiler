import React from "react";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import HC_exporting from "highcharts/modules/exporting";
import styled, { ThemeProvider } from "styled-components";
import { useState, useEffect } from "react";
import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import Breadcrumb from "react-bootstrap/Breadcrumb";
import AlertDismissible from "./../components/alerts/AlertDismissible";

HC_exporting(Highcharts);

const StackedContainer = styled.div``;

const defaultConfig = {
  chart: {
    type: "column", // column / bar
    zoomType: "xy",
  },
  title: {
    text: "PET Timings", // graph title
  },
  credits: {
    enabled: false,
  },
  xAxis: {
    categories: [1, 2, 3], // single bar label
    title: {
      text: "PET Number",
    },
  },
  yAxis: {
    min: 0,
    allowDecimals: true,
    title: {
      text: "Time (s)",
    },
  },
  legend: {
    reversed: true,
    itemStyle: { fontSize: "12pt" },
  },
  plotOptions: {
    series: {
      stacking: "normal",
    },
  },
  series: [1, 2, 3, 4],
  navigation: {
    menuStyle: {
      background: "#E0E0E0",
    },
  },
};

function Stacked(props) {
  const [options, setOptions] = useState(props.options);
  const [level, setLevel] = useState(["/TOP"]);
  const [error, setError] = useState("");
  const [history, setHistory] = useState(["/TOP"]);

  useEffect(() => {
    updateLevel();
  }, [level]);

  const dataMap = () => {
    let map = {};
    for (let key in props.options) {
      map[key] = props.options[key];
    }
    return map;
  };

  const hasData = (key) => {
    const map = dataMap();
    if (!key in map || map == undefined) {
      console.debug("datamap is undefined or missing key");
      return false;
    }
    if (!map[key] || !"xvals" in map[key] || !"yvals" in map[key]) {
      console.debug("missing xvals or yvals");
      return false;
    }
    return true;
  };

  const updateLevel = () => {
    console.debug(`updateLevel()`);

    const key = level.join("/");
    let chartData = {
      title: {
        text: key,
      },
      xAxis: {
        categories: dataMap()[key].xvals,
      },
      series: dataMap()[key].yvals,
    };
    setOptions({
      // ...chartEvents,
      ...defaultConfig,
      ...chartData,
      ...seriesEvents,
    });
    console.log("The opptions are ", options);
    setHistory(history + level);
  };

  const toggleOn = () => toggleAllSeries(true);
  const toggleOff = () => toggleAllSeries(false);

  const toggleAllSeries = (value) => {
    console.debug(`toggleAllSeries(${value})`);
    setOptions({
      plotOptions: {
        series: {
          visible: value,
        },
      },
    });
  };

  const chartEvents = {
    chart: {
      events: {
        redraw: function (event) {
          console.log("REDRAW");
        },
        load: function (event) {
          console.log("LOAD");
        },
      },
    },
  };

  const seriesEvents = {
    plotOptions: {
      series: {
        stacking: "normal",
        events: {
          click: function (event) {
            clickLevel(this.name);
          },
        },
      },
    },
  };

  const clickLevel = (_level) => {
    if (level === _level) return;
    console.debug(`clickLevel(${_level})`);
    setError("");
    let position = level.indexOf(_level);

    let tempLevel;
    if (position === -1) {
      tempLevel = [...level, _level];
    } else {
      tempLevel = level.slice(0, position + 1);
    }

    const key = level.join("/");
    if (!tempLevel.join("/") in dataMap()) {
      console.error(tempLevel.join("/"), " not found in ", props.options);
      return;
    }

    if (!hasData(key)) {
      setError("No additional timing detail");
      return;
    }
    setLevel(tempLevel);
  };

  const ChartCrumbs = () => {
    return level.map
      ? level.map((item, idx) => {
          return (
            <Breadcrumb.Item key={idx} onClick={() => clickLevel(item)} href="">
              {item}
            </Breadcrumb.Item>
          );
        })
      : "";
  };

  return (
    <StackedContainer>
      {error && <AlertDismissible message={error} />}
      <Breadcrumb>{ChartCrumbs()}</Breadcrumb>
      <HighchartsReact highcharts={Highcharts} options={options} />
      <div className="d-flex justify-content-center">
        <ButtonGroup size="sm" className="me-2">
          <Button onClick={toggleOn} className="m-1">
            Select All
          </Button>
          <Button onClick={toggleOff} className="m-1">
            Select None
          </Button>
        </ButtonGroup>
      </div>
    </StackedContainer>
  );
}

export default Stacked;
