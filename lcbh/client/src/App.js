import logo from './logo.svg';
import './App.css';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import InquiryForm from './components/inquiryForm';
import Threads from './components/threads';
import env from "react-dotenv";
import { useEffect, useState } from 'react';

function App() {
  const [access_token, set_access_token] = useState(undefined);
  const [customerID, setCustomerID] = useState(0)
  const [threads, setThreads] = useState(undefined);
  const [user_inquiry, setInquiry] = useState(undefined);

  // getting conversation id
  const link = window.location.href.split("/");
  const conv_id = link[link.length - 1];

  // getting the access tokens
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
      .then(data => {
        set_access_token(data)
        return data.access_token
      })
      .then((token) => {
        fetch(`https://api.helpscout.net/v2/conversations/${conv_id}`, {
          method: "GET",
          headers: {
            "Content-Type": 'application/json',
            "Authorization": `Bearer ${token}`
          }
        })
          .then((res) => res.json())
          .then((data) => setCustomerID(data.primaryCustomer.id))
          .catch(err => console.log(err))
      }
      )
      .catch(err => console.log(err))
  }
  
  // authenticate us
  useEffect(() => {
    authenticate();
  }, [])
  
  return (
    <div className="content">
      {
        access_token ? 
          <>
            <InquiryForm access_token={access_token.access_token} conv_id={conv_id} customerID={customerID} threads = {threads} user_inquiry = {user_inquiry} setInquiry = {setInquiry} ></InquiryForm>
            <Threads threads={ threads} setThreads = {setThreads} access_token={access_token.access_token} conv_id={conv_id} user_inquiry= {user_inquiry} setInquiry = {setInquiry}/>
          </> : <></>}
    </div>
  )
}

export default App;
