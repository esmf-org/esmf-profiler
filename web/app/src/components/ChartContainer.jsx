import React from "react";
import styled, { ThemeProvider } from "styled-components";

const Container = styled.div`
  overflow: auto;
  min-height: 75vh;
  margin: 25px;
`;

export default class ChartContainer extends React.Component {
  render() {
    return (
      <div className="col-xl-12 col-lg-12">
        {/* Card Header - Dropdown */}
        <div
          className="
                      card-header
                      py-3
                      d-flex
                      flex-row
                      align-items-center
                      bg-white
                      justify-content-between
                      "
        >
          <h6 className="m-0 text-dark">Load Balance</h6>
        </div>
        {/* Card Body */}
        <Container>
          <div className="chart-area">{this.props.children}</div>
        </Container>
      </div>
    );
  }
}
