import React from "react";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import HC_exporting from "highcharts/modules/exporting";
import styled, { ThemeProvider } from "styled-components";
import { useState, useEffect } from "react";
import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import Breadcrumb from "react-bootstrap/Breadcrumb";

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

  useEffect(() => {
    let chartData = {
      title: {
        text: level.join("/"),
      },
      xAxis: {
        categories: props.options[level.join("/")].xvals,
      },
      series: props.options[level.join("/")].yvals,
    };
    setOptions({
      ...defaultConfig,
      ...chartData,
      ...seriesEvents,
    });
  }, [level]);

  const toggleOn = () => toggleAllSeries(true);
  const toggleOff = () => toggleAllSeries(false);

  const toggleAllSeries = (value) => {
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
            clicker(this.name);
            // alert("you clicked series: " + this.name);
          },
        },
      },
    },
  };

  const clicker = (_level) => {
    console.log(`clicker(${_level})`);
    setLevel(() => [...level, _level]);

    setOptions({
      title: {
        text: level.join("/"),
      },
      xAxis: {
        categories: props.options[level.join("/")].xvals,
      },
      series: props.options[level.join("/")].yvals,
    });
  };

  const ChartCrumbs = () => {
    return level.map((item) => {
      return (
        <Breadcrumb.Item onClick={() => setLevel([item])} href="">
          {item}
        </Breadcrumb.Item>
      );
    });
  };

  const Chart = () => {
    return props.options ? (
      <HighchartsReact highcharts={Highcharts} options={options} />
    ) : (
      ""
    );
  };

  return (
    <StackedContainer>
      <Breadcrumb>{ChartCrumbs()}</Breadcrumb>
      {Chart}
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
