import { Formik, Form, Field } from 'formik';
import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import './inquiryForm.css';
import SampleResponse from './sampleResponse';


function InquiryForm({access_token, conv_id, customerID, threads, user_inquiry, setInquiry, lang, setLang}){
    const [sampleRes, setSampleRes] = useState([]);
    const [currentText, setCurrentText] = useState('');
    const textChanged = (event) => {
      setCurrentText(event.target.value);
    };
    const inquiryChanged = (event) => {
      setInquiry(event.target.value);
    };

    let submitAction =  undefined;

    const handleSubmit = (values, { setSubmitting }) => {
      // Check which submit button was clicked and perform the corresponding action
      switch (submitAction) {
        case 'submit':
          setTimeout(() => {
            fetch("http://localhost:5000/inquiry",
            {
              method: "POST",
              headers:{
                "Content-Type": 'application/json',
                "Access-Control-Allow-Origin": "*"
              },
              body: JSON.stringify({
                inquiry: user_inquiry
              })
            })
              .then(res => res.json())
              .then(data =>{ 
                setSampleRes(data.inquiry)
              })
              .catch(err => console.log(err))
          });
          break;
        case 'translate':
          console.log(lang)
          setTimeout(() => {
            fetch("http://localhost:5000/translation",
            {
              method: "POST",
              headers:{
                "Content-Type": 'application/json',
                "Access-Control-Allow-Origin": "*"
              },
              body: JSON.stringify({
                inquiry: user_inquiry,
                lang: lang
              })
            })
              .then(res => res.json())
              .then(data =>{ 
                console.log(data)
                setInquiry(data["translation"]);
              })
              .catch(err => console.log(err))
          });
          break;
        default:
          console.log('Unknown submit action:', values.submitAction);
      }
      setSubmitting(false);
    };

    return(<div style = {{"display" : "flex", "justifyContent" : "center", "height" : "500px"}}>
          <div style = {{"width" : "50%", "margin" : "10px"}}>
            <h1> Most Recent Inquiry</h1>

            <Formik
              initialValues={{ inquiry: [],  submitAction: ''  }}

              onSubmit={handleSubmit}

            >
              {({
                handleChange,
                handleBlur,
                handleSubmit,
                /* and other goodies */
              }) =>{  
                
                function handleCombinedChange(event) {
                  inquiryChanged(event);
                  handleChange(event);
                }

                return(
                <Form onSubmit={handleSubmit}>
                  <div className = "input">
                  <textarea
                    name="inquiry"
                    onChange={handleCombinedChange}
                    onBlur={handleBlur}
                    value={user_inquiry}
                    style = {{"width" : "90%", "marginRight": "13px", "height" : "333px"}}
                  />
                  <div>
                    <Button id = "button" type="submit"  style = {{"backgroundColor": "#005ca4" }} variant="primary" onClick = {() =>{submitAction = "submit"; handleSubmit();}} name = "submitAction" value = "submit">Generate Response</Button>
                    
                    <Button id = "button" type="submit"  style = {{"backgroundColor": "#005ca4" }} variant="primary" onClick = {() =>{submitAction = "translate"; handleSubmit();}} name = "submitAction" value = "translate">Translate</Button>
                  </div>
                  </div>
                </Form>
              )}}
            </Formik>
          
          </div>
          <div style = {{"width" : "50%", "margin" : "10px"}}>
            <SampleResponse 
              sampleRes={sampleRes}
              currentText={currentText}
              setCurrentText={setCurrentText} 
              access_token={access_token}
              conv_id={conv_id}
              customerID={customerID}
              lang = {lang}
            />
          </div>
        </div>)
}


export default InquiryForm;