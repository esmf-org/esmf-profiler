import React from "react";
import ReactDOM from "react-dom";
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";
import Main from "./Report"
import { Helmet, HelmetProvider } from 'react-helmet-async';


function App() {
  return (
    <div>
      <HelmetProvider>
        <Helmet>
          <title>Hello World</title>
          <link rel="canonical" href="https://www.tacobell.com/" />
        </Helmet>

        <Switch>
          <Route path="/">
            <Main />
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
