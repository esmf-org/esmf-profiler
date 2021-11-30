import React from "react";
import { useState } from "react";
import { Form } from "react-bootstrap";

export default function CheckBox(props) {
  const [isChecked, setIsChecked] = useState(props.checked);

  const handleChange = (e) => {
    console.debug(`handleChange(${e})`);
    setIsChecked(!isChecked);
    props.handleChange(isChecked, props.chartRef);
  };

  return (
    <Form.Check
      inline
      checked={isChecked}
      onChange={handleChange}
      type="checkbox"
      label={props.label}
      name="optionsGroup"
    />
  );
}
