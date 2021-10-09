import React from "react";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import HC_exporting from "highcharts/modules/exporting";
import styled, { ThemeProvider } from "styled-components";
import { useState, useEffect } from "react";
import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";

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
  const [data, setData] = useState();

  useEffect(() => {
    let level = "/ROOT";
    let chartData = {
      title: {
        text: level,
      },
      xAxis: {
        categories: props.config[level].xvals,
      },
      series: props.config[level].yvals,
    };
    setData({
      ...defaultConfig,
      ...chartData,
      ...seriesShit,
    });
    // clicker();
  }, []);

  const toggleOn = () => toggleAllSeries(true);
  const toggleOff = () => toggleAllSeries(false);

  const toggleAllSeries = (value) => {
    setData({
      plotOptions: {
        series: {
          visible: value,
        },
      },
    });
  };

  const seriesShit = {
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

  const clicker = (level) => {
    console.log("This level " + level);
    console.log(props.config);
    level = "/ROOT/" + level;

    let chartData = {
      title: {
        text: level,
      },
      xAxis: {
        categories: props.config[level].xvals,
      },
      series: props.config[level].yvals,
    };
    setData({
      ...chartData,
    });
  };

  return (
    <StackedContainer>
      <HighchartsReact highcharts={Highcharts} options={data} />
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
