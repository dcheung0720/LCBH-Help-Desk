import logo from './logo.svg';
import './App.css';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import InquiryForm from './components/inquiryForm';
import env from "react-dotenv";

function App() {
  return (
    <div className = "content">
      <Button variant="primary" onClick={() =>
        fetch("https://api.helpscout.net/v2/conversations?status=active", {
            method: "GET",
            headers: { 
              "Content-Type": 'application/json',
              // "Access-Control-Allow-Origin": "*",
              "Authorization" : `Bearer ${env.HS_SECRET_KEY}`
            }
          }
        ).then(res => res.json())
        .then(data => console.log(data))

      }>Primary</Button>

      <Button variant="primary" onClick={() =>
        fetch("https://api.helpscout.net/v2/conversations/2157256241/tags", {
            method: "PUT",
            headers: { 
              "Content-Type": 'application/json',
              // "Access-Control-Allow-Origin": "*",
              "Authorization" : `Bearer ${env.HS_SECRET_KEY}`
            },
            body: JSON.stringify({
                "tags" : [ "eviction" ]
            })

          }
        ).then(res => console.log(res))

      }>Primary</Button>  
      <InquiryForm></InquiryForm>
    </div>
  ) 
}

export default App;
