import React from "react";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import HC_exporting from "highcharts/modules/exporting";

//import Boost from "highcharts/modules/boost";

import { useState, useEffect, useRef } from "react";
import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";

import AlertDismissible from "./../components/alerts/AlertDismissible";
import Breadcrumbs from "../components/Breadcrumbs";
import CheckBoxOption from "./CheckBoxOption";

import { toggleAxisInvert } from "./Utils";

HC_exporting(Highcharts);
//Boost(Highcharts);

function Stacked(props) {
  const chartOptions = {
    chart: {
      type: "column", // column / bar
      zoomType: "xy",
      displayErrors: false, //TODO set for prod and dev
      panKey: "ctrl",
      height: 50 + "%",
      spacingBottom: 0,
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
      accessibility: {
        rangeDescription: "Range: All PETs",
      },
    },
    yAxis: {
      min: 0,
      allowDecimals: true,
      tickInterval: 300,
      title: {
        text: "Total Time (s)",
      },
    },
    legend: {
      layout: "vertical",
      align: "right",
      verticalAlign: "middle",
      enabled: true,
      reversed: true,
      itemStyle: { fontSize: "8pt" },
    },

    plotOptions: {
      series: {
        stacking: "normal",
        //boostThreshold: 1,
        events: {
          click: function (e) {
            e.preventDefault();
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
  const prevLevel = useRef(["/TOP"]);
  const [options, setOptions] = useState(chartOptions);
  const chartComponent = useRef(null);

  useEffect(() => {
    if (prevLevel.current !== level) {
      prevLevel.current = level;
      setError("");

      const key = level.join("/");

      if (!props.options[key]) {
        setError(`No detail timing data for ${key}`);
        return;
      }

      let _new = {
        xAxis: {
          categories: [...props.options[key].xvals],
        },
        series: props.options[key].yvals.map((y) => {
          return { name: y.name, visible: true, data: [...y.data] };
        }),
      };

      setOptions((prevOptions) => {
        return { ...prevOptions, ..._new };
      });
    }
  }, [level, props]);

  const toggle = (show) => {
    const chart = chartComponent.current.chart;
    if (show) {
      chart.series.map((s) => s.setVisible(true, false));
    } else {
      chart.series.map((s) => s.setVisible(false, false));
    }
    chart.redraw();
  };

  const hasData = (check) => {
    const key = check.join("/");
    if (!props.options[key]) {
      return false;
    }
    return true;
  };

  const clickLevel = (_level) => {
    console.debug(`clickLevel(${_level})`);

    if (!hasData([...prevLevel.current, _level])) {
      setError(`No detail timing data for ${_level}`);
    } else {
      setLevel((current) => [...current, _level]);
    }
  };

  const clickCrumb = (idx, _level) => {
    console.debug(`clickCrumb(${idx}, ${_level})`);
    setLevel((prev) => prev.slice(0, idx + 1));
  };

  return (
    <React.Fragment>
      {error && <AlertDismissible message={error} />}

      <Breadcrumbs click={clickCrumb} level={level} />
      <HighchartsReact
        highcharts={Highcharts}
        options={options}
        ref={chartComponent}
      />

      <div className="d-flex justify-content-center">
        <CheckBoxOption
          label="Invert Axis"
          handleChange={toggleAxisInvert}
          chartRef={chartComponent}
        />

        <ButtonGroup size="sm" className="me-2">
          <Button onClick={() => toggle(true)} className="m-1">
            Select All
          </Button>
          <Button onClick={() => toggle(false)} className="m-1">
            Select None
          </Button>
        </ButtonGroup>
      </div>
    </React.Fragment>
  );
}

export default Stacked;
