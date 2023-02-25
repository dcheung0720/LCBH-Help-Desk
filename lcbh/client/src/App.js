import logo from './logo.svg';
import './App.css';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import InquiryForm from './components/inquiryForm';
import env from "react-dotenv";
import { useEffect } from 'react';

function App() {
  const authenticate = () => {
    fetch('https://api.helpscout.net/v2/oauth2/token', {
      method: 'POST', 
      headers: {
        "Content-Type": 'application/json',
      },
      body: JSON.stringify({
        client_id: `${env.CLIENT_ID}`,
        client_secret: `${env.CLIENT_SECRET}`,
        grant_type: 'client_credentials'
      })
    })
    .then(res => res.json())
    .then(data => console.log(data))
    .catch(err => console.log(err))
  }

  useEffect(() => {
    console.log(window.env.CLIENT_ID)
    authenticate()
    
  }, [])

  return (
    <div className="content"> 
      <InquiryForm></InquiryForm>
    </div>
  ) 
}

export default App;
