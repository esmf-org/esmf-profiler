import React from 'react';
import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official'
import data from './data.json'



const defaultConfig = {
  chart: {
    type: "column", // column / bar
    zoomType: "xy",
  },
  title: {
    text: "Default Title", // graph title
  },
  xAxis: {
    categories: data.xvals, // single bar label
  },
  yAxis: {
    min: 0,
    allowDecimals: false,
    title: {
      text: "Default Title",
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
  series: data.yvals
};

export default class Stacked extends React.Component {


  render() {
    return (
      <HighchartsReact highcharts={Highcharts} options={defaultConfig} />
    )
  }
}
