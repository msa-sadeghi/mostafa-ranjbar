import { BrowserRouter, Route, Routes } from "react-router-dom";
import Documents from "./components/Documents";
import Login from "./components/Login";
function App() {
  return (
    <div className="container">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/dashboard" element={<Documents />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
