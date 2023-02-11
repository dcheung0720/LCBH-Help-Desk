import logo from './logo.svg';
import './App.css';
import React, {useState, useEffect} from 'react'
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { Formik } from 'formik';


function App() {
  const [data, setData] = useState("");
  return (
    <div>
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
          }).then(res =>{console.log(res); return res.json()})
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
          <input
            name="inquiry"
            onChange={handleChange}
            onBlur={handleBlur}
            value={values.inquiry}
          />
          <button type="submit" onClick ={handleSubmit}>
            Submit
          </button>
        </form>
      )}
    </Formik>
      <div>Sample response: {data}</div>
  </div>
  )

}

export default App;
