import { Alert, Button } from "react-bootstrap";
import { useState, useEffect } from "react";

// import styled from "styled-components";

// const DismissButton = styled.div`
//   padding: 0px;
// `;

function AlertDismissible(props) {
  const [show, setShow] = useState(true);

  return (
    // <Alert variant="danger">
    //   <div className="d-flex justify-content-end">
    //     <button
    //       type="button"
    //       class="close"
    //       data-dismiss="alert"
    //       aria-hidden="true"
    //     >
    //       x
    //     </button>
    //   </div>
    //   <Alert.Heading>Error</Alert.Heading>
    //   <p>{props.message}</p>
    // </Alert>
    <Alert show={show} variant={props.variant ? props.variant : "danger"}>
      <div className="d-flex justify-content-end">
        <Button onClick={() => setShow(false)} variant="outline-danger">
          X
        </Button>
      </div>
      {props.message}
    </Alert>
  );
}

export default AlertDismissible;
