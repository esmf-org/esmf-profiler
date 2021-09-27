import React from 'react';
import ReactDOM from 'react-dom';
import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official'
import Stacked from './charts/Stacked'

export default class CardText extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="card shadow mb-4">
                <div className="card-header py-3">
                    <h6 className="m-0 font-weight-bold text-primary">
                        Development Approach
                    </h6>
                </div>
                <div className="card-body">
                    <p>
                        SB Admin 2 makes extensive use of Bootstrap 4 utility
                        classes in order to reduce CSS bloat and poor page
                        performance. Custom CSS classes are used to create custom
                        components and custom utility classes.
                    </p>
                    <p className="mb-0">
                        Before working with this theme, you should become familiar
                        with the Bootstrap framework, especially the utility
                        classes.
                    </p>
                </div>
            </div>

        )
    }
}