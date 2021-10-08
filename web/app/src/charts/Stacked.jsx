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
      events: {
        click: function (event) {
          console.log(event.point);
          console.log(this.name);

          // alert("you clicked series: " + this.name);
        },
        click: function () {
          var name = this.name;
          var _i = this._i;
          Highcharts.each(this.chart.series, function (p, i) {
            // clicked(name, _i, p);
          });
        },
      },
    },
  },
  series: [1, 2, 3, 4],
  navigation: {
    menuStyle: {
      background: "#E0E0E0",
    },
  },
};

// function clicked(name, _i, p) {
//   console.log("click");
//   console.log(name, p.name);
//   console.log(_i, p._i);
//   console.log(name === p.name);
//   if (name === p.name) {
//     console.log(p.visible);
//     !p.visible ? p.show() : p.hide();
//     console.log(p.visible);
//   }
// }

function Stacked(props) {
  const [data, setData] = useState();

  useEffect(() => {
    setData({
      ...defaultConfig,
      ...props.config,
    });
  }, []);

  // constructor(props) {
  //   super(props);
  //   this.config = {
  //     ...defaultConfig,
  //     ...this.props.config,
  //   };
  //   console.log(this.props.config);
  // }

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
