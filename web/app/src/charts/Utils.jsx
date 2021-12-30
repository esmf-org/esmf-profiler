const toggleAxisInvert = (checked, chartComponent) => {
  console.debug(`toggleRedrawOnHide(${checked})`);
  chartComponent.current.chart.update({
    chart: {
      inverted: !checked,
    },
  });
  console.log(chartComponent.current.chart.options);
};

const toggleLogarithimic = (checked, chartComponent) => {
  console.debug(`toggleLogarithimic(${checked}, ${chartComponent})`);
  const chart = chartComponent.current.chart;
  if (checked) {
    chart.yAxis[0].update({
      type: "linear",
    });
  } else {
    chart.yAxis[0].update({
      type: "logarithmic",
    });
  }
};

const setSize = (checked, chartComponent) => {
  console.debug(`setSize(${checked}, ${chartComponent})`);
  if (checked) {
    chartComponent.current.chart.setSize(null);
  } else {
    chartComponent.current.chart.setSize(600);
  }
};

export { toggleAxisInvert, toggleLogarithimic, setSize };
