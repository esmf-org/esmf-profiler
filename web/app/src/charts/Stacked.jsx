import React from "react";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import HC_exporting from "highcharts/modules/exporting";
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
  navigation: {
    menuStyle: {
      background: "#E0E0E0",
    },
  },
};

export default class Stacked extends React.Component {
  constructor(props) {
    super(props);
    this.config = {
      ...defaultConfig,
      ...this.props.config,
    };
    console.log(this.props.config);
  }

  render() {
    return (
      <StackedContainer>
        <HighchartsReact highcharts={Highcharts} options={this.config} />
      </StackedContainer>
    );
  }
}
