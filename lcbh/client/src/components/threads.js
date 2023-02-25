import { useEffect, useState } from "react";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';


function Threads({access_token}){
    const [threads, setThreads] = useState(undefined);

    useEffect(() =>{
        getThreads();
    }, []);

    function getThreads(){
        fetch(`https://api.helpscout.net/v2/conversations/${2157256241}/threads`, {
            method: "GET",
            headers:{
                "Content-Type": 'application/json',
                "Authorization" : `Bearer ${access_token}`
            }
        })
        .then(res => res.json())
        //set threads state
        .then(data =>{setThreads( data._embedded.threads);}
        );
    }

    return(threads?
        <Container fluid="md">
            {threads.map(thread =>
                <Row style ={{borderStyle: "solid", marginBottom: "10px", padding: "15px"}}>{thread.body}</Row>
            ) }
        </Container> : <></>)

}


export default Threads;