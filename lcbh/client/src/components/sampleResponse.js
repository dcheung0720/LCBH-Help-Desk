import { useState, useEffect } from "react";
import { Formik, Form, Field } from 'formik';
import Button from 'react-bootstrap/Button';

function SampleResponse({ sampleRes, currentText, setCurrentText, access_token, conv_id, customerID, lang}) {

    const [currentIndex, setCurrentIndex] = useState(0);

    // go to previous response
    const handlePrevClick = () => {
        setCurrentIndex(currentIndex => (currentIndex - 1 + sampleRes.length) % sampleRes.length);
        setCurrentText(sampleRes[currentIndex][0])
    };
      
    //go to the next response
    const handleNextClick = () => {
    setCurrentIndex(currentIndex => (currentIndex + 1) % sampleRes.length);
    const mod_ind = currentIndex % sampleRes.length;
    setCurrentText(sampleRes[mod_ind][0]);
    };

    //creat reply thread
    const createReplyToThread = () => {
        navigator.clipboard.writeText(currentText);
        fetch(`https://api.helpscout.net/v2/conversations/${conv_id}/notes`, {
            method: "POST",
            headers: {
                "Content-Type": 'application/json',
                "Authorization": `Bearer ${access_token}`
            },
            body: JSON.stringify({
                "customer" : {
                    "id" : customerID
                },
                "text" : currentText
            })
        })
        .then(() => console.log("Reply was sent!"))
        .catch(err => console.log(err))
        .then(() => window.close());
    }

    const handleTranslate = (values, { setSubmitting }) => {
        // Check which submit button was clicked and perform the corresponding action
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
                  inquiry: currentText,
                  lang: lang
                })
              })
                .then(res => res.json())
                .then(data =>{ 
                  console.log(data)
                  setCurrentText(data["translation"]);
                })
                .catch(err => console.log(err))
            });    
      };

    useEffect(() => {
        sampleRes.forEach((res) => {
            if (res[0].startsWith('\n\n\n'))
                res[0] = res[0].split('\n\n\n')[1]
            // 12 empty spaces in the beginning
            if(res[0].startsWith('            '))
                res[0] = res[0].split('            ')[1]
        })
        if(sampleRes.length > 0)
            setCurrentText(sampleRes[currentIndex][0]);
    }, [sampleRes, currentIndex, setCurrentText])


    return (
    <>
        <h1>Sample Response</h1>
        {
            sampleRes.length !== 0 && 
            <>
                <div className="carousel" >
                    <div style = {{ "width" : "100%",  "height": "350px"}} className="response">
                        <div style = {{"marginBottom": "10px", "display" : "flex", "justifyContent": "space-between"}}>
                            <Button className  = "button" variant="primary" style = {{"backgroundColor": "#005ca4" }} onClick={handlePrevClick}>Prev </Button>
                            <Button className  = "button" variant="primary"  style = {{"backgroundColor": "#005ca4" }} onClick={handleNextClick}>Next </Button>
                        </div>
                        <div style={{"borderStyle" : "solid", "marginBottom": "10px", "padding": "10px", "height": "30%", "overflowY" : "scroll"}}>
                            <p> <b>Category:</b> {sampleRes[currentIndex][1]}</p>
                            <p> <b>Original Inquiry:</b> {sampleRes[currentIndex][2]} </p>
                        </div>
                        <div style = {{"display" : "flex", "alignItems" : "center", "height": "50%"}}>
                            <div style={{"width" : "100%", "height" : "100%"}}>
                            <Formik
                                initialValues={{ inquiry: [] }}

                                onSubmit={handleTranslate}

                                >
                                {({
                                    handleChange,
                                    handleBlur,
                                    handleSubmit,
                                    /* and other goodies */
                                }) =>{  
                                    
                                    function handleCombinedChange(event) {
                                    handleChange(event);
                                    }

                                    return(
                                    <Form onSubmit={handleSubmit}>
                                    <div className = "input">
                                    <textarea 
                                    style={{"width": "100%", "height" : "175px", "padding": "none"}}
                                    value={currentText}
                                    onChange={(e) => {
                                        setCurrentText(e.target.value);
                                        console.log(e.target.value);
                                    }} > 
                                    </textarea>
                                    <div id = "responseButton"> 
                                        <Button className  = "button" type="submit"  style = {{"backgroundColor": "#a44800" }} variant="primary" onClick = {() =>{handleTranslate();}} name = "submitAction" value = "translate">Translate</Button>
                                        <Button className  = "button" variant="primary"  style = {{"backgroundColor": "#005ca4", "height" : "40%", "marginLeft" : "20px" }} onClick={createReplyToThread}>Send to HelpScout</Button>
                                    </div>
                                    </div>
                                    </Form>
                                )}}
                            </Formik>  
                            </div>  
                    
                        </div>                     
                    </div>
                
                </div>
            </>
        }
    </>
    )
}






export default SampleResponse;