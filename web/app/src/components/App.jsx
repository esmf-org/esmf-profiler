import "../styles/main.scss";
import React from "react";
import Report from "./Report";
import { Helmet, HelmetProvider } from "react-helmet-async";

function App() {
  return (
    <div>
      <HelmetProvider>
        <Helmet>
          <title>ESMF Profiler</title>
          <link rel="canonical" href="#" />
        </Helmet>
        <Report />
      </HelmetProvider>
    </div>
  );
}

export default App;
