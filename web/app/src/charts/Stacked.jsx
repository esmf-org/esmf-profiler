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
  const [level, setLevel] = useState(["/ROOT"]);
  const [error, setError] = useState("");
  const [history, setHistory] = useState(["/ROOT"]);

  useEffect(() => {
    updateLevel();
  }, [level]);

  const updateLevel = () => {
    console.debug(`updateLevel()`);
    if (!level.join) {
      return;
    }
    const key = level.join("/");
    if (!key in props.options || props.options[key] == undefined) {
      setLevel(level.slice(0, level.length - 1));
      setError("That branch contains no data");
      return;
    }
    if (!"xvals" in props.options[key] || !"yvals" in props.options[key]) {
      console.log(error);
      setLevel(history);
      setError("You've reached the tree limit");
      return;
    }

    let chartData = {
      title: {
        text: key,
      },
      xAxis: {
        categories: props.options[key].xvals,
      },
      series: props.options[key].yvals,
    };
    setOptions({
      ...defaultConfig,
      ...chartData,
      ...seriesEvents,
    });
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
    console.debug(`clickLevel(${_level})`);
    setError("");
    let position = level.indexOf(_level);
    console.log(`Position is ${position}`);

    if (position === -1) {
      setLevel(() => [...level, _level]);
    } else {
      setLevel(() => level.slice(0, position + 1));
    }
    console.log(level);
  };

  const ChartCrumbs = () => {
    console.debug("ChartCrumbs()");

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
      <ButtonGroup size="sm" className="me-2">
        <Button onClick={toggleOn} className="m-1">
          Select All
        </Button>
        <Button onClick={toggleOff} className="m-1">
          Select None
        </Button>
      </ButtonGroup>
    </StackedContainer>
  );
}

export default Stacked;
