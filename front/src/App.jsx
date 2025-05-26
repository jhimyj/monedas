import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./App.css";
import LoginScreen from "./screens/LoginScreen";
import RegisterScreen from "./screens/RegisterScreen";
import TransaccionScreen from "./screens/TransaccionScreen";
import CurrencyScreen from "./screens/CurrencyScreen";

function App() {
  return (
    <div>
      <Router>
        <Routes>
          <Route path="/" element={<LoginScreen />} />
          <Route path="/login" element={<LoginScreen />} />
          <Route path="/register" element={<RegisterScreen />} />
          <Route path="/transaccion" element={<TransaccionScreen />} />
          <Route path="/currency" element={<CurrencyScreen />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
