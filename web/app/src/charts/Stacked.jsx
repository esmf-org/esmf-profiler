import React from "react";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import styled, { ThemeProvider } from "styled-components";
import data from "./data.json";

const StackedContainer = styled.div``;

const defaultConfig = {
  chart: {
    type: "column", // column / bar
    zoomType: "xy",
  },
  title: {
    text: "Default Chart Title", // graph title
  },
  xAxis: {
    categories: data.xvals, // single bar label
  },
  yAxis: {
    min: 0,
    allowDecimals: false,
    title: {
      text: "Default X Axis Title",
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
  series: data.yvals,
};

export default class Stacked extends React.Component {
  constructor(props) {
    super(props);
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
