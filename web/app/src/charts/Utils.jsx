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

export { toggleAxisInvert };
