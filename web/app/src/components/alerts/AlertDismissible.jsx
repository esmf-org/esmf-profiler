import { Alert, Row, Col } from "react-bootstrap";

// const DismissButton = styled.div`
//   padding: 0px;
// `;

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
