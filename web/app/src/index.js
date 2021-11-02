import './styles/main.scss'
import React from "react";
import ReactDOM from "react-dom";
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";
import Report from "./components/Report"
import { Helmet, HelmetProvider } from 'react-helmet-async';


function App() {
  return (
    <div>
      <HelmetProvider>
        <Helmet>
          <title>ESMF Profiler</title>
          <link rel="canonical" href="#" />
        </Helmet>

        <Switch>
          <Route path="/">
            <Report />
          </Route>
        </Switch>
      </HelmetProvider>
    </div>
  );
}

ReactDOM.render(
  <Router>
    <App />
  </Router>,
  document.getElementById("root")
);
