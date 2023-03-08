import { Formik } from 'formik';
import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import './inquiryForm.css';
import SampleResponse from './sampleResponse';


function InquiryForm({access_token, conv_id, customerID, threads}){
    const [sampleRes, setSampleRes] = useState([]);
    const [currentText, setCurrentText] = useState('');
    const textChanged = (event) => {
      setCurrentText(event.target.value);
    };

    
    return(<div style = {{"display" : "flex", "justifyContent" : "center", "height" : "500px"}}>
          <div style = {{"width" : "50%", "margin" : "10px"}}>
            <h1> Most Recent Inquiry</h1>
            <Formik
              initialValues={{ inquiry: [] }}
              onSubmit={(values) => {
                setTimeout(() => {
                  fetch("http://localhost:5000/inquiry",
                  {
                    method: "POST",
                    headers:{
                      "Content-Type": 'application/json',
                      "Access-Control-Allow-Origin": "*"
                    },
                    body: JSON.stringify({
                      inquiry: values.inquiry
                    })
                  })
                    .then(res => res.json())
                    .then(data =>{ 
                      // console.log(data.inquiry)
                      setSampleRes(data.inquiry)
                    })
                    .catch(err => console.log(err))
                });
              }}
            >
              {({
                values,
                errors,
                touched,
                handleChange,
                handleBlur,
                handleSubmit,
                isSubmitting,
                /* and other goodies */
              }) => (
                <form>
                  <div className = "input">
                  <textarea
                    name="inquiry"
                    onChange={handleChange}
                    onBlur={handleBlur}
                    value={values.inquiry}
                    style = {{"width" : "90%", "marginRight": "13px", "height" : "333px"}}
                  />
                  <Button type="submit"  style = {{"backgroundColor": "#005ca4" }} onClick ={handleSubmit} variant="primary">Submit</Button>
                  </div>
                </form>
              )}
            
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
            />
          </div>
        </div>)
}


export default InquiryForm;