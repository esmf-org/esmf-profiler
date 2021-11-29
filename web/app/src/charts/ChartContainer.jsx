import React from "react";
import styled from "styled-components";

const StyledContainer = styled.div`
  overflow: auto;
  margin: 0px;
`;

const StyledTitle = styled.h6`
  color: #5a5c69 !important;
  margin-bottom: 0 !important;
`;

function Header(props) {
  return (
    <React.Fragment>
      <div
        className="
                      card-header
                      py-0
                      d-flex
                      flex-row
                      align-items-center
                      bg-white
                      justify-content-between
                      "
      >
        {props.children}
      </div>
    </React.Fragment>
  );
}

function Container(props) {
  return (
    <React.Fragment>
      <div className={`col-xl-${props.size || 12} col-lg-${props.size || 12}`}>
        {props.children}
      </div>
    </React.Fragment>
  );
}

export default function ChartContainer(props) {
  return (
    <Container size={props.size ? props.size : 12}>
      <Header>
        <StyledTitle>{props.title ? props.title : ""}</StyledTitle>
      </Header>
      <StyledContainer>{props.children}</StyledContainer>
    </Container>
  );
}
