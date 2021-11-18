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

// import styled from "styled-components";

// const open = styled.div`
//   text-decoration: none;
//   font-size: 1.1rem;
//   padding: 1.5rem 1rem;
//   text-align: center;
//   letter-spacing: 0.05rem;
// `;

// const closed = styled.div`
//   width: 10px;
// `;

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
      ;
    </React.Fragment>
  );
}

function Wrapper(props) {
  return (
    <React.Fragment>
      <Nav className="flex-column" bg="gradient-dark">
        <ul
          data-toggle="collapse"
          className={`navbar-nav bg-gradient-dark sidebar sidebar-dark accordion ${
            props.show ? "" : "toggled"
          }`}
          id="accordionSidebar"
        >
          <SidebarBrand />
          {props.children}
          <ToggleButton click={props.toggle} />
        </ul>
      </Nav>
      ;
    </React.Fragment>
  );
}

function Section(props) {
  return (
    <React.Fragment>
      <SidebarHeading name={props.title} />
      {props.children}
      <SidebarDivider />
    </React.Fragment>
  );
}

function SidebarBrand(props) {
  return (
    <React.Fragment>
      <div className="sidebar-brand d-flex align-items-center justify-content-center">
        <div className="sidebar-brand-text">
          ESMF Profiler{" "}
          <div>
            {/* TODO Add JS to dynamically update version based on tag */}
            <img
              src="https://img.shields.io/badge/version-0.1.1-success"
              alt="shield"
            ></img>
          </div>
        </div>
      </div>
      ;
    </React.Fragment>
  );
}

function SidebarHeading(props) {
  return <div className="sidebar-heading">{props.name}</div>;
}

function SidebarDivider() {
  return <hr className="sidebar-divider my-10" />;
}

function SidebarButton(props) {
  return (
    <React.Fragment>
      <li className="nav-item">
        <button className="nav-link text-muted">
          <FontAwesomeIcon icon={props.icon} />
          <span>{` ${props.name}`}</span>
        </button>
      </li>
    </React.Fragment>
  );
}

export default function Sidebar() {
  const [show, setShow] = useState(true);

  const toggleSidebar = () => {
    if (!show) {
      document.body.classList.add("sidebar-toggled");
    }
    document.body.classList.remove("sidebar-toggled");
    setShow(!show);
  };

  return (
    <React.Fragment>
      <br />

      <Wrapper toggle={toggleSidebar} show={show}>
        <SidebarDivider />

        <Section title="Application Info">
          <SidebarButton name="Component Configuration" icon={faBox} />
        </Section>

        <Section title="Timing">
          <SidebarButton name="Timing Summary" icon={faClock} />
          <SidebarButton name="Load Balance" icon={faChartBar} />
          <SidebarButton name="MPI Profiler" icon={faProjectDiagram} />
        </Section>

        <Section title="Memory">
          <SidebarButton name="Memory Profile" icon={faHubspot} />
        </Section>

        <Section title="I/O">
          <SidebarButton name="NetCDF Profile" icon={faHdd} />
        </Section>
      </Wrapper>
    </React.Fragment>
  );
}
