import { useEffect, useState } from "react";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';


function Threads({access_token, threads, setThreads, conv_id,user_inquiry, setInquiry}){

    useEffect(()=>{
        if(threads !== undefined){
            let thread_concat = threads.reduce((txt_cat, cur) => txt_cat + cur.body, '')
            if(thread_concat !== ''){
                const regex = new RegExp(/Inquiry:\s*(.*?)</);
                const match = regex.exec(thread_concat);
                if(user_inquiry === undefined)
                    setInquiry(match[1])
                if(user_inquiry !== undefined){
                    fetch('http://localhost:5000/lang',{
                        method: "POST",
                        headers:{
                        "Content-Type": 'application/json',
                        "Access-Control-Allow-Origin": "*"
                        },
                        body: JSON.stringify({
                        inquiry: user_inquiry
                        })
                    }).then(res => res.json())
                    .then(data => console.log(data))
                    .catch(err => console.log(err))
                }
            }
        }
    }, [threads, user_inquiry])



    useEffect(() =>{
        getThreads();
    }, []);

    function getThreads(){
        fetch(`https://api.helpscout.net/v2/conversations/${conv_id}/threads`, {
            method: "GET",
            headers:{
                "Content-Type": 'application/json',
                "Authorization" : `Bearer ${access_token}`
            }
        })
        .then(res => res.json())
        //set threads state
        .then(data =>{setThreads( data._embedded.threads.reverse());}
        );
    }

    return(threads?
        <Container fluid="md">
            {threads.map(thread =>
                <Row style ={{borderStyle: "solid", marginBottom: "10px", padding: "15px"}}>{thread.body}</Row>
            )}
        </Container> : <></>)

}


export default Threads;