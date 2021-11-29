import React from "react";
import { useState } from "react";
import { Form } from "react-bootstrap";

export default function CheckBox(props) {
  const [isChecked, setIsChecked] = useState(false);

  const handleChange = (e) => {
    setIsChecked(!isChecked);
    props.handleChange(isChecked);
  };

  return (
    <React.Fragment>
      <Form.Check
        checked={isChecked}
        onChange={handleChange}
        type="checkbox"
        label={props.label}
      />
    </React.Fragment>
  );
}
