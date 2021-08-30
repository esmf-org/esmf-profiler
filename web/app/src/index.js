import StackedChart from './charts'
import "./style.scss";

const chartConfig = {
    series: [
        {
            name: "OCN",
            data: [0.8344, 2],
        },
        {
            name: "MED",
            data: [0.8203, 1.5],
        },
        {
            name: "ATM",
            data: [0.6387],
        },
        {
            name: "ATM-TO-MED",
            data: [0.5975],
        },
    ],
};

const chart = new StackedChart("container2", chartConfig)
chart.render()

