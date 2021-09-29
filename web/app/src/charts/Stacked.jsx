import React from "react";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import styled, { ThemeProvider } from "styled-components";

const StackedContainer = styled.div``;

const defaultConfig = {
  chart: {
    type: "column", // column / bar
    zoomType: "xy",
  },
  title: {
    text: "PET Timings", // graph title
  },
  xAxis: {
    categories: [1, 2, 3], // single bar label
    title: {
      text: "PET Number",
    },
  },
  yAxis: {
    min: 0,
    allowDecimals: false,
    title: {
      text: "Time (s)",
    },
  },
  legend: {
    reversed: true,
  },
  plotOptions: {
    series: {
      stacking: "normal",
    },
  },
  series: [1, 2, 3, 4],
};

export default class Stacked extends React.Component {
  constructor(props) {
    super(props);
    console.log(this.props.config);
  }

  render() {
    return (
      <StackedContainer>
        <HighchartsReact
          highcharts={Highcharts}
          options={this.props.config || defaultConfig}
        />
      </StackedContainer>
    );
  }
}
