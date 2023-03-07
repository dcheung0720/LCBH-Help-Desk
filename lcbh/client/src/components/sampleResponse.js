import { useState, useEffect } from "react"

function SampleResponse({ sampleRes, textChanged, currentText, setCurrentText }) {
    
    const [currentIndex, setCurrentIndex] = useState(0);
    console.log(sampleRes[currentIndex])
    console.log("whole sample res", sampleRes)
    


    const handlePrevClick = () => {
      console.log("before change: ", currentIndex);
      setCurrentIndex((currentIndex - 1 + sampleRes.length) % sampleRes.length);
      console.log("after change", currentIndex);
      setCurrentText(sampleRes[currentIndex][0]);
    };
  
    const handleNextClick = () => {
     console.log("before change: ", currentIndex);
      setCurrentIndex((currentIndex + 1) % sampleRes.length);
      console.log("after change: ", currentIndex);
      setCurrentText(sampleRes[currentIndex][0]);
    };

    useEffect(() => {
        sampleRes.forEach((res) => {
            if (res[0].startsWith('\n\n\n'))
                res[0] = res[0].split('\n\n\n')[1]
            // 12 empty spaces in the beginning
            if(res[0].startsWith('            '))
                res[0] = res[0].split('            ')[1]
        })

    }, [sampleRes])
      

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
                        <textarea 
                            style={{ "height": "200px" }}
                            value={currentText}
                            onChange={(e) => {
                                textChanged(e);
                                setCurrentText(e.target.value);
                              }} > 
                        </textarea>

                    </div>
                    <button className="next" onClick={handleNextClick}>Next</button>
                </div>
        }
    </>
    )
}






export default SampleResponse;