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
        {/* <textarea style={{ "height": "200px" }} value={sampleRes} onChange={textChanged} > </textarea> */}
        <div className="carousel">
            <button className="prev" onClick={handlePrevClick}>Prev</button>
            <div className="item">
                <p>{sampleRes[currentIndex]}</p>
            </div>
            <button className="next" onClick={handleNextClick}>Next</button>
        </div>
    </>
    )
}






export default SampleResponse;