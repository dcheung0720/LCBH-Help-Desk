

import { Formik } from 'formik';
import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import './inquiryForm.css';


function InquiryForm(){
    const [data, setData] = useState("");
    const textChanged = (event) =>{
        setData(
            event.target.value
        );
    }
    
    return(<div>
        <h1>Inquiry</h1>
        <Formik
          initialValues={{ inquiry: '' }}
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
              }).then(res =>{return res.json()})
              .then(data => setData(data["inquiry"]))
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
                style = {{"marginRight": "13px"}}
              />
              <Button type="submit" onClick ={handleSubmit} variant="primary">Submit</Button>
              </div>
                </form>
          )}
        </Formik>
            <br></br>
          <h2>Sample response:</h2>
          <textarea style = {{"height" : "200px"}} value={data} onChange={textChanged} > </textarea>
      </div>)
}


export default InquiryForm;