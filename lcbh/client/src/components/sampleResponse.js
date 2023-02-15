function SampleResponse({sampleRes, sampleResType, textChanged}){
    return(<>
    {/* dropdown */}
    <select value  = {sampleResType} className="form-select" aria-label="Default select example">
        <option selected>{sampleResType}</option>
        {/* <option value="1">One</option>
        <option value="2">Two</option>
        <option value="3">Three</option> */}
    </select>
    <h2>Sample response:</h2>
    <textarea style = {{"height" : "200px"}} value={sampleRes} onChange={textChanged} > </textarea>
    </>)
}






export default SampleResponse;