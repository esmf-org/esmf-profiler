import { Alert, Button, Row, Col, Fade } from "react-bootstrap";
import { useState } from "react";
import styled from "styled-components";

const DismissButton = styled.div`
  padding: 0px;
`;

function AlertDismissible(props) {
  return (
    <Alert variant="danger">
      <Row>
        <Col>{props.message}</Col>
      </Row>
    </Alert>
  );
}

export default AlertDismissible;
