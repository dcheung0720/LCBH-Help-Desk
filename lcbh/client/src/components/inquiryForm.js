import { Formik, Form, Field } from 'formik';
import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import './inquiryForm.css';
import SampleResponse from './sampleResponse';


function InquiryForm({access_token, conv_id, customerID, threads, user_inquiry, setInquiry}){
    const [sampleRes, setSampleRes] = useState([]);
    const [currentText, setCurrentText] = useState('');
    const textChanged = (event) => {
      setCurrentText(event.target.value);
    };
    const inquiryChanged = (event) => {
      setInquiry(event.target.value);
    };


    // function MyForm() {
    //   const handleSubmit = (values, { setSubmitting }) => {
    //     // Check which submit button was clicked and perform the corresponding action
    //     switch (values.submitAction) {
    //       case 'save':
    //         console.log('Saving form with values:', values);
    //         // Add code to save form here
    //         break;
    //       case 'submit':
    //         console.log('Submitting form with values:', values);
    //         // Add code to submit form here
    //         break;
    //       default:
    //         console.log('Unknown submit action:', values.submitAction);
    //     }
    //     setSubmitting(false);
    //   };
    //   return (
    //     <Formik initialValues={{}} onSubmit={handleSubmit}>
    //       {({ handleSubmit }) => (
    //         <Form onSubmit={handleSubmit}>
    //           <Field name="fieldOne" />
    //           {/* Save button */}
    //           <button type="submit" name="submitAction" value="save">
    //             Save
    //           </button>
    //           {/* Submit button */}
    //           <button type="submit" name="submitAction" value="submit">
    //             Submit
    //           </button>
    //         </Form>
    //       )}
    //     </Formik>
    //   );
    // }

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
          console.log('Submitting form with values:', values);
          // Add code to submit form here
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
                  <Button type="submit"  style = {{"backgroundColor": "#005ca4" }} variant="primary" onClick = {() =>{submitAction = "submit"; handleSubmit();}} name = "submitAction" value = "submit">Submit</Button>
                  <Button type="submit"  style = {{"backgroundColor": "#005ca4" }} variant="primary" onClick = {() =>{submitAction = "translate"; handleSubmit();}} name = "submitAction" value = "translate">Translate</Button>
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
            />
          </div>
        </div>)
}


export default InquiryForm;