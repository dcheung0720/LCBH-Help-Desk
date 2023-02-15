import { useState, useEffect } from "react"

function SampleResponse({ sampleRes, textChanged }) {

    const [currentIndex, setCurrentIndex] = useState(0);

    const handlePrevClick = () => {
      setCurrentIndex((currentIndex - 1 + sampleRes.length) % sampleRes.length);
    };
  
    const handleNextClick = () => {
      setCurrentIndex((currentIndex + 1) % sampleRes.length);
    };

    return (
    <>
        <h2>Sample response:</h2>
        {
            sampleRes.length !== 0 && 
                <div className="carousel">
                    <button className="prev" onClick={handlePrevClick}>Prev</button>
                    <div className="response">
                        <p>Category: {sampleRes[currentIndex][1]}</p>
                        <p>Original Inquiry: {sampleRes[currentIndex][2]}</p>
                        <textarea style={{ "height": "200px" }} value={sampleRes[currentIndex][0]} onChange={textChanged} > </textarea>
                    </div>
                    <button className="next" onClick={handleNextClick}>Next</button>
                </div>
        }
    </>
    )
}






export default SampleResponse;