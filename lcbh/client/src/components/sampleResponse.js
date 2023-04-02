import { useState, useEffect } from "react"
import Button from 'react-bootstrap/Button';

function SampleResponse({ sampleRes, currentText, setCurrentText, access_token, conv_id, customerID}) {

    const [currentIndex, setCurrentIndex] = useState(0);

    const handlePrevClick = () => {
      setCurrentIndex((currentIndex - 1 + sampleRes.length) % sampleRes.length);
      setCurrentText(sampleRes[currentIndex][0])
    };
  
    const handleNextClick = () => {
      setCurrentIndex((currentIndex + 1) % sampleRes.length);
      setCurrentText(sampleRes[currentIndex][0])
    };


    const createReplyToThread = () => {
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
    }

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
    }, [sampleRes])


    return (
    <>
        <h1>Sample response:</h1>
        {
            sampleRes.length !== 0 && 
            <>
                <div className="carousel" >
                    <div style = {{ "width" : "100%",  "height": "350px"}} className="response">
                        <div style = {{"marginBottom": "10px", "display" : "flex", "justifyContent": "space-between"}}>
                            <Button variant="primary" style = {{"backgroundColor": "#005ca4" }} onClick={handlePrevClick}>Prev </Button>
                            <Button variant="primary"  style = {{"backgroundColor": "#005ca4" }} onClick={handleNextClick}>Next </Button>
                        </div>
                        <div style={{"borderStyle" : "solid", "marginBottom": "10px", "padding": "10px", "height": "30%", "overflowY" : "scroll"}}>
                            <p> <b>Category:</b> {sampleRes[currentIndex][1]}</p>
                            <p> <b>Original Inquiry:</b> {sampleRes[currentIndex][2]} </p>
                        </div>
                        <div style = {{"display" : "flex", "alignItems" : "center", "height": "50%"}}>
                            <div style={{"width" : "100%", "height" : "100%"}}>
                                <textarea 
                                    style={{"width": "100%", "height" : "100%", "padding": "none"}}
                                    value={currentText}
                                    onChange={(e) => {
                                        setCurrentText(e.target.value);
                                    }} > 
                                </textarea>
                            </div>  
                            <Button variant="primary"  style = {{"backgroundColor": "#005ca4", "height" : "40%", "marginLeft" : "20px" }} onClick={createReplyToThread}>Send to HelpScout</Button>
                        </div>                     
                    </div>
                
                </div>
            </>
        }
    </>
    )
}






export default SampleResponse;