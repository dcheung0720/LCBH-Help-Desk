import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import 'bootstrap/dist/css/bootstrap.min.css';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <>
    <Navbar style = {{"backgroundColor": "#005ca4" }}>
    <Container style ={{"marginLeft" : "15px", }}>
      <Navbar.Brand style ={{"color" : "white", "fontSize" : "25px"}} href="#home">LCBH Help Desk: ResponseGenie</Navbar.Brand>
    </Container>
  </Navbar>
    <App />
  </>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
