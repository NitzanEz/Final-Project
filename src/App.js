// src/index.js or src/App.js
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from '../src/Login';
import PatientClassification from '../src/PatientClassification';

ReactDOM.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/patient-classification" element={<PatientClassification />} />
      </Routes>
    </Router>
  </React.StrictMode>,
  document.getElementById('root')
);
