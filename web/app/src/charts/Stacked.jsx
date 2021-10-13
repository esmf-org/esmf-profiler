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

function Stacked(props) {
  let chartOptions = {
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
        events: {
          click: function () {
            clickLevel(this.name);
          },
        },
      },
    },
    series: [],
    navigation: {
      menuStyle: {
        background: "#E0E0E0",
      },
    },
  };

  const [error, setError] = useState("");
  const [level, setLevel] = useState(["/TOP"]);
  const [options, setOptions] = useState(chartOptions);
  useEffect(() => {
    updateLevel();
  }, [props, level]);

  const updateLevel = () => {
    setError("");
    console.debug(
      `updateLevel() current level: ${level}  length: ${level.length}`
    );

    const key = level.join("/");
    console.log("level: ", level);
    console.log(`stringed key: ${key}`);
    if (!props.options[key]) {
      setError("no data available");
      return;
    }
    console.log(level, key, props.options[key], props.options);

    const newxVals = props.options[key].xvals;
    const newyVals = props.options[key].yvals;
    setOptions({
      ...options.series.yvals,
      xVals: newxVals,
      series: newyVals,
    });
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

  const clickLevel = (_level) => {
    console.debug(`clickLevel(${_level})`);
    let position = level.lastIndexOf(_level);
    let key = level.join("/");
    if (position < 0) {
      console.debug(`Appending ${_level} to ${level}`);
      key = [...level, _level];
    } else {
      key = level.slice(0, position + 1);
    }
    console.debug(
      `clickLevel(${_level}): key is (${key}): position is (${position})`
    );
    setLevel(key);
  };

  const clickCrumb = (idx, _level) => {
    console.debug(`clickCrumb(${idx}, ${_level})`);
    let newLevel = level;
    if (idx === 0) {
      console.log("idx is 0!!");
      newLevel = ["/TOP"];
    } else if (idx < level.length) {
      newLevel = level.slice(0, idx + 1);
    } else {
      newLevel = [...level, _level];
    }
    setLevel(newLevel);
    console.log(idx, level);
  };

  return (
    <StackedContainer>
      {error && <AlertDismissible message={error} />}

      <Breadcrumb>
        {level.map
          ? level.map((_level, idx) => {
              return (
                <Breadcrumb.Item
                  key={idx}
                  onClick={() => clickCrumb(idx, _level)}
                  href=""
                >
                  {_level}
                </Breadcrumb.Item>
              );
            })
          : ""}
      </Breadcrumb>

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
