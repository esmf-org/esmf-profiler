import { faHubspot } from "@fortawesome/free-brands-svg-icons";
import {
  faBox,
  faChartBar,
  faClock,
  faHdd,
  faProjectDiagram,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useState } from "react";
import Nav from "react-bootstrap/Nav";
import styled from "styled-components";

export default function Sidebar() {
  const [show, setShow] = useState(true);

  const toggleSidebar = () => {
    if (!show) {
      document.body.classList.add("sidebar-toggled");
    } else {
      document.body.classList.remove("sidebar-toggled");
    }
    setShow(!show);
  };

  return (
    <React.Fragment>
      <br />

      <Wrapper toggle={toggleSidebar} show={show}>
        <Divider />

        <Section title="Application Info">
          <Button name="Component Configuration" icon={faBox} muted />
        </Section>

        <Section title="Timing">
          <Button name="Timing Summary" icon={faClock} muted />
          <Button name="Load Balance" icon={faChartBar} />
          <Button name="MPI Profiler" icon={faProjectDiagram} muted />
        </Section>

        <Section title="Memory">
          <Button name="Memory Profile" icon={faHubspot} muted />
        </Section>

        <Section title="I/O">
          <Button name="NetCDF Profile" icon={faHdd} muted />
        </Section>
      </Wrapper>
    </React.Fragment>
  );
}

const Button = (props) => (
  <React.Fragment>
    <StyledNavItem>
      <li className="nav-item">
        <StyledButton className={`nav-link ${props.muted ? "text-muted" : ""}`}>
          <FontAwesomeIcon icon={props.icon} />
          <span>{` ${props.name}`}</span>
        </StyledButton>
      </li>
    </StyledNavItem>
  </React.Fragment>
);

const StyledButton = styled.button`
  background-color: #5a5c69;
  background-size: contain;
  border: 0;
`;

const StyledNavItem = styled.div`
  font-size: 1em;
  border: 0px;
  color: #858796;
`;

function ToggleButton(props) {
  return (
    <React.Fragment>
      <div className="text-center d-none d-md-inline">
        <button
          className="rounded-circle border-0"
          id="sidebarToggle"
          onClick={() => {
            props.click();
          }}
        ></button>
      </div>
    </React.Fragment>
  );
}

function Wrapper(props) {
  return (
    <React.Fragment>
      <Nav className="flex-column" bg="gradient-dark">
        <ul
          data-toggle="collapse"
          className={`navbar-nav bg-dark sidebar sidebar-dark accordion ${
            props.show ? "" : "toggled"
          }`}
          id="accordionSidebar"
        >
          <Brand />
          {props.children}
          <ToggleButton click={props.toggle} />
        </ul>
      </Nav>
    </React.Fragment>
  );
}

function Section(props) {
  return (
    <React.Fragment>
      <Heading name={props.title} />
      {props.children}
      <Divider />
    </React.Fragment>
  );
}

function Brand() {
  return (
    <React.Fragment>
      <div className="sidebar-brand d-flex align-items-center justify-content-center">
        <div className="sidebar-brand-text">
          ESMF Profiler{" "}
          <div>
            {/* TODO Add JS to dynamically update version based on tag */}
            <img
              src="https://img.shields.io/badge/version-0.2.0-success"
              alt="shield"
            ></img>
          </div>
        </div>
      </div>
    </React.Fragment>
  );
}

function Heading(props) {
  return <div className="sidebar-heading">{props.name}</div>;
}

function Divider() {
  return <hr className="sidebar-divider my-10" />;
}
