import "./styles/main.scss";

import ChartContainer from "./components/ChartContainer";
import Stacked from "./charts/Stacked";
import Sidebar from "./components/SideBar";
import Footer from "./components/Footer";

function App() {
  return (
    <div className="App">
      <div id="wrapper">
        <Sidebar />
        <div id="content-wrapper" className="d-flex flex-column">
          <div id="content">
            <div className="container-fluid">
              <div className="d-sm-flex align-items-center justify-content-between mb-4">
                <h1 className="h3 mb-0 text-gray-800"></h1>
              </div>

              <div className="row">
                <ChartContainer>
                  <Stacked />
                </ChartContainer>
              </div>
            </div>
          </div>

          <Footer />
        </div>
      </div>
    </div>
  );
}

export default App;
