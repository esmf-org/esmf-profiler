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

const chartOptions = {
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
    enabled: true,
    reversed: true,
    itemStyle: { fontSize: "12pt" },
  },
  plotOptions: {
    series: {
      stacking: "normal",
    },
  },
  series: [],
  navigation: {
    menuStyle: {
      background: "#E0E0E0",
    },
  },
};

function Stacked(props) {
  let plotOptions_series_events = {
    plotOptions: {
      series: {
        events: {
          click: function (event) {
            clickLevel(this.name);
          },
        },
      },
    },
  };

  const [error, setError] = useState("");
  const [level, setLevel] = useState(["/ROOT"]);
  const [levelHistory, setLevelHistory] = useState([]);
  const [options, setOptions] = useState({ ...chartOptions });

  useEffect(() => {
    updateLevel();
  }, [props.options, level]);

  const updateLevel = () => {
    setError("");
    if (!props.options) {
      setError("No data available");
      return;
    }

    console.debug(`updateLevel() current level: ${level}`);

    const key = level.join("/");
    if (!props.options[key]) {
      setError("No data available");
      return;
    }
    const newOptions = {
      ...options,
      ...props?.options[key],
      xAxis: {
        categories: props?.options[key]?.xvals,
      },

      series: props?.options[key]?.yvals,
      ...plotOptions_series_events,
    };
    setOptions(newOptions);
  };

  const toggleOn = () => toggleAllSeries(true);
  const toggleOff = () => toggleAllSeries(false);

  const toggleAllSeries = (value) => {
    console.debug(`toggleAllSeries(${value})`);
    setOptions({
      ...options.plotOptions,
      plotOptions: {
        series: {
          visible: value,
        },
      },
    });
  };

  const clickLevel = (_level) => {
    let position = level?.indexOf(_level);
    let key = level.join("/");
    if (position === -1) {
      console.debug(`Appending ${_level} to ${level}`);
      key = [...level, _level];
    } else {
      console.debug(`Popping ${position}`);
      key = [...level].slice(0, position + 1);
    }
    setLevelHistory(...level);
    setLevel(key);

    console.debug(
      `clickLevel(${_level}): key is (${key}): position is (${position})`
    );
  };

  return (
    <StackedContainer>
      {error && <AlertDismissible message={error} />}
      <Breadcrumb>
        {level.map
          ? level.map((item, idx) => {
              return (
                <Breadcrumb.Item
                  key={idx}
                  onClick={() => clickLevel(item)}
                  href=""
                >
                  {item}
                </Breadcrumb.Item>
              );
            })
          : ""}
      </Breadcrumb>

      <HighchartsReact highcharts={Highcharts} options={{ ...options }} />

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
