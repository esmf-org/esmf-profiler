import React from "react";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import HC_exporting from "highcharts/modules/exporting";

//import Boost from "highcharts/modules/boost";

import { useState, useEffect, useRef } from "react";
import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import { Form } from "react-bootstrap";
import AlertDismissible from "./../components/alerts/AlertDismissible";
import Breadcrumbs from "../components/Breadcrumbs";

HC_exporting(Highcharts);
//Boost(Highcharts);

function CheckBox(props) {
  const [isChecked, setIsChecked] = useState(false);

  const handleChange = (e) => {
    setIsChecked(!isChecked);
    props.handleChange(isChecked);
  };

  return (
    <React.Fragment>
      <Form.Check
        checked={isChecked}
        onChange={handleChange}
        type="checkbox"
        label={props.label}
      />
    </React.Fragment>
  );
}

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
      title: {
        text: "Total Time (s)",
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
        //boostThreshold: 1,
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
  const prevLevel = useRef(["/TOP"]);
  const [options, setOptions] = useState(chartOptions);
  const chartComponent = useRef(null);
  const [isLoading, setIsLoading] = useState(false);

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
    setIsLoading(false);
  }, [level, props]);

  const toggleLogarithimic = () => {
    console.debug("toggleLogarithimic");
    setIsLoading(true);
    const chart = chartComponent.current.chart;
    const currentChartType = chart.yAxis[0].userOptions.type;
    if (currentChartType === "logarithmic") {
      chart.yAxis[0].update({
        type: "linear",
      });
    } else {
      chart.yAxis[0].update({
        type: "logarithmic",
      });
    }
    setIsLoading(false);
  };

  const toggleAllSeries = (show) => {
    setIsLoading(true);
    const chart = chartComponent.current.chart;
    if (show) {
      chart.series.map((s) => s.setVisible(true, false));
    } else {
      chart.series.map((s) => s.setVisible(false, false));
    }
    setIsLoading(false);
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
      setIsLoading(true);
      setLevel((current) => [...current, _level]);
    }
  };

  const clickCrumb = (idx, _level) => {
    setIsLoading(true);
    console.debug(`clickCrumb(${idx}, ${_level})`);
    setLevel((prev) => prev.slice(0, idx + 1));
  };

  return (
    <ChartContainer>
      {error && <AlertDismissible message={error} />}
      <Breadcrumbs click={clickCrumb} level={level} />
      <div className="d-flex justify-content-center m-2">
        {isLoading && <Spinner animation="border" role="status" />}
      </div>
      <HighchartsReact
        highcharts={Highcharts}
        options={options}
        ref={chartComponent}
      />

      <div className="d-flex justify-content-center">
        <ButtonGroup size="sm" className="me-2">
          <Button onClick={() => toggleAllSeries(true)} className="m-1">
            Select All
          </Button>
          <Button onClick={() => toggleAllSeries(false)} className="m-1">
            Select None
          </Button>
        </ButtonGroup>
        <CheckBox
          label="Logarithmic Y-Axis"
          handleChange={() => toggleLogarithimic()}
        />
      </div>
    </ChartContainer>
  );
}

export default Stacked;
