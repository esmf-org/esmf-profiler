import React from "react";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import HC_exporting from "highcharts/modules/exporting";

import { useState, useEffect } from "react";
import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import Breadcrumb from "react-bootstrap/Breadcrumb";
import AlertDismissible from "./../components/alerts/AlertDismissible";

HC_exporting(Highcharts);

// const StackedContainer = styled.div``;

function Stacked(props) {
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
        events: {
          click: function () {
            clickLevel(this.name);
          },
        },
      },
    },

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
  }, [props.options, level]);

  const updateLevel = () => {
    setError("");

    const key = level.join("/");

    if (!props.options[key]) {
      setError("no data available");
      // setLevel((prev) => [...prev.slice(0, prev.length)]);
      return;
    }

    const newxVals = props.options[key].xvals;
    const newyVals = props.options[key].yvals;

    let _new = {
      xAxis: {
        categories: newxVals,
      },
      series: newyVals,
    };
    setOptions((prevOptions) => {
      return { ...prevOptions, ..._new };
    });
  };

  const toggleOn = () => toggleAllSeries(true);
  const toggleOff = () => toggleAllSeries(false);

  const toggleAllSeries = (value) => {
    console.debug(`toggleAllSeries(${value})`);
    setOptions((prev) => {
      return {
        ...prev,
        plotOptions: {
          series: {
            visible: value,
          },
        },
      };
    });
  };

  let clickLevel = (_level) => {
    console.debug(`clickLevel(${_level})`);
    setLevel((current) => [...current, _level]);
  };

  const clickCrumb = (idx, _level) => {
    console.debug(`clickCrumb(${idx}, ${_level})`);
    setLevel((prev) => prev.slice(0, idx + 1));
  };

  return (
    <React.Fragment>
      {error && <AlertDismissible message={error} />}

      <Breadcrumb>
        {level?.map
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
    </React.Fragment>
  );
}

export default Stacked;
