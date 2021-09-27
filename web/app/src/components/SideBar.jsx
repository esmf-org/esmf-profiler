import React from "react";
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

export default class Sidebar extends React.Component {
  render() {
    return (
      <ul
        className="navbar-nav bg-gradient-dark sidebar sidebar-dark accordion"
        id="accordionSidebar"
      >
        {/* Sidebar - Brand */}
        <a
          className="sidebar-brand d-flex align-items-center justify-content-center"
          href="index.html"
        >
          <div className="sidebar-brand-icon rotate-n-15">
            <i className="fas fa-laugh-wink"></i>
          </div>
          <div className="sidebar-brand-text mx-3">
            ESMF Profiler <sup>V0.0.1</sup>
          </div>
        </a>

        {/* Divider */}
        <hr className="sidebar-divider my-10" />
        <div className="sidebar-heading">Application Info</div>
        <li className="nav-item">
          <a className="nav-link" href="charts.html">
            <FontAwesomeIcon icon={faBox} />
            <span> Component Configuration</span>
          </a>
        </li>

        {/* Divider */}
        <hr className="sidebar-divider" />

        {/* Heading */}
        <div className="sidebar-heading">Timing</div>

        {/* Nav Item - Pages Collapse Menu */}
        <li className="nav-item">
          <a className="nav-link" href="charts.html">
            <FontAwesomeIcon icon={faClock} />
            <span> Timing Summary</span>
          </a>
        </li>
        <li className="nav-item">
          <a className="nav-link" href="charts.html">
            <FontAwesomeIcon icon={faChartBar} />
            <span> Load Balance</span>
          </a>
        </li>
        <li className="nav-item">
          <a className="nav-link" href="charts.html">
            <FontAwesomeIcon icon={faProjectDiagram} />
            <span> MPI Profile</span>
          </a>
        </li>

        {/* Divider */}
        <hr className="sidebar-divider" />

        {/* Heading */}
        <div className="sidebar-heading"> Memory</div>

        {/* Nav Item - Pages Collapse Menu */}
        <li className="nav-item">
          <a className="nav-link" href="charts.html">
            <FontAwesomeIcon icon={faHubspot} />
            <span> Memory Profile</span>
          </a>
        </li>

        {/* Nav Item - Charts */}
        <div className="sidebar-heading">I/O</div>
        <li className="nav-item">
          <a className="nav-link" href="charts.html">
            <FontAwesomeIcon icon={faHdd} />
            <span> NetCDF Profile</span>
          </a>
        </li>

        {/* Divider */}
        <hr className="sidebar-divider d-none d-md-block" />

        {/* Sidebar Toggler (Sidebar) */}
        <div className="text-center d-none d-md-inline">
          <button className="rounded-circle border-0" id="sidebarToggler">
            <FontAwesomeIcon icon={faArrowCircleLeft} />
          </button>
        </div>
      </ul>
    );
  }
}
