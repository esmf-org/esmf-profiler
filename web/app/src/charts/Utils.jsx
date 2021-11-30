const toggleAxisInvert = (checked, chartComponent) => {
  console.debug(`toggleRedrawOnHide(${checked})`);
  console.log(chartComponent.current.chart.options);
  chartComponent.current.chart.update({
    chart: {
      inverted: !checked,
    },
  });
  console.log(chartComponent.current.chart.options);
};

const toggleLogarithimic = (checked, chartComponent) => {
  console.debug("toggleLogarithimic");
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
};

export { toggleAxisInvert, toggleLogarithimic };
