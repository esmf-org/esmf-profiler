import React from "react";
import { useState } from "react";

import Offcanvas from "react-bootstrap/Offcanvas";

import Button from "react-bootstrap/Button";

import Modal from "react-bootstrap/Modal";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";

import { Link } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faHubspot } from "@fortawesome/free-brands-svg-icons";
import {
  faBox,
  faClock,
  faChartBar,
  faProjectDiagram,
  faHdd,
  faArrowCircleLeft,
} from "@fortawesome/free-solid-svg-icons";
import styled, { ThemeProvider } from "styled-components";

const open = styled.div`
  text-decoration: none;
  font-size: 1.1rem;
  padding: 1.5rem 1rem;
  text-align: center;
  letter-spacing: 0.05rem;
`;

const closed = styled.div`
  width: 10px;
`;

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

      <Nav className="flex-column" bg="gradient-dark">
        <ul
          data-toggle="collapse"
          className={`navbar-nav bg-gradient-dark sidebar sidebar-dark accordion ${
            show ? "" : "toggled"
          }`}
          id="accordionSidebar"
        >
          {/* Sidebar - Brand */}
          <div className="sidebar-brand d-flex align-items-center justify-content-center">
            <div className="sidebar-brand-text">
              ESMF Profiler{" "}
              <div>
                {/* TODO Add JS to dynamically update version based on tag */}
                <img src="https://img.shields.io/badge/version-0.1.1-success"></img>
              </div>
            </div>
          </div>

          {/* Divider */}
          <hr className="sidebar-divider my-10" />
          <div className="sidebar-heading">Application Info</div>
          <li className="nav-item">
            <Link className="nav-link text-muted" to="/">
              <FontAwesomeIcon icon={faBox} />
              <span> Component Configuration</span>
            </Link>
          </li>

          {/* Divider */}
          <hr className="sidebar-divider" />

          {/* Heading */}
          <div className="sidebar-heading">Timing</div>

          {/* Nav Item - Pages Collapse Menu */}
          <li className="nav-item">
            <Link className="nav-link text-muted" to="/">
              <FontAwesomeIcon icon={faClock} />
              <span> Timing Summary</span>
            </Link>
          </li>
          <li className="nav-item">
            <Link className="nav-link" to="#">
              <FontAwesomeIcon icon={faChartBar} />
              <span> Load Balance</span>
            </Link>
          </li>
          <li className="nav-item">
            <Link className="nav-link text-muted" to="/">
              <FontAwesomeIcon icon={faProjectDiagram} />
              <span> MPI Profile</span>
            </Link>
          </li>

          {/* Divider */}
          <hr className="sidebar-divider" />

          {/* Heading */}
          <div className="sidebar-heading"> Memory</div>

          {/* Nav Item - Pages Collapse Menu */}
          <li className="nav-item">
            <Link className="nav-link text-muted" to="/">
              <FontAwesomeIcon icon={faHubspot} />
              <span> Memory Profile</span>
            </Link>
          </li>

          {/* Nav Item - Charts */}
          <div className="sidebar-heading">I/O</div>
          <li className="nav-item">
            <Link className="nav-link text-muted" to="/">
              <FontAwesomeIcon icon={faHdd} />
              <span> NetCDF Profile</span>
            </Link>
          </li>

          {/* Divider */}
          <hr className="sidebar-divider d-none d-md-block" />

          {/* Sidebar Toggler (Sidebar) */}

          {/* <button className="rounded-circle border-0" id="sidebarToggler">
            <FontAwesomeIcon icon={faArrowCircleLeft} />
          </button> */}

          <div className="text-center d-none d-md-inline">
            <button
              className="rounded-circle border-0"
              id="sidebarToggle"
              onClick={() => {
                toggleSidebar();
                console.log("CLICK");
              }}
            ></button>
          </div>
        </ul>
      </Nav>
    </React.Fragment>
  );
}
