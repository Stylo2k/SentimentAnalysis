import './App.css';
import Comment from './components/Comment.js'
import axios from 'axios';


import 'bootstrap/dist/css/bootstrap.min.css';

import React, { useEffect, useState } from 'react';

const BACKEND_PORT = 8080;

axios.defaults.baseURL = `http://localhost:${BACKEND_PORT}/api`;


function getComment(index, setIndex, data, setData, total, sentiment, setSentiment, reason, setReason) {

  function next(event) {
    if(!data) return;
    axios.put(`/commits/${index}`, data).then((response) => {
      setIndex(index + 1);
      setData(response.data);
      setSentiment("");
      setReason("");
    }).catch((error) => {
      console.log(error);
    });
  }


  function prevIndex() {
    if(!data) return;
    axios.put(`/commits/${index}`, data).then((response) => {
      if (index - 1 >= 0) setIndex(index - 1);
      setData(response.data);
      setSentiment("");
      setReason("");
    }).catch((error) => {
      console.log(error);
    }
    );
  }

  if (!data) {
    return <div>Loading...</div>
  }
  
  return <Comment index={index} data={data} callback={next} prev={prevIndex} total={total} expected={sentiment} setSentiment={setSentiment} reason={reason} setReason={setReason}/>
}


function App() {
  const [index, setIndex] = useState(0);
  const [total, setTotal] = useState(0);
  const [data, setData] = useState();
  const [sentiment, setSentiment] = useState();
  const [reason, setReason] = useState();

  useEffect(() => {
    axios.get(`/commits/${index}`).then((response) => {
      setData(response.data);
      let expected = "";
      let reason = "";
      let sentiments = response.data.sentiment_analysis;
      for (let index in sentiments) {
        let sentiment = sentiments[index];
        if (sentiment?.classifier === "alshakoush") {
          expected = sentiment.sentiment;
          reason = sentiment.reason;
        }
      }
      setSentiment(expected);
      setReason(reason);
    }).catch((error) => {
      console.log(error);
    });
  },[index]);

  useEffect(() => {
    axios.get(`/commits/total`).then((response) => {
      setTotal(response.data.total);
    }).catch((error) => {
      console.log(error);
    });
  },[]);

  return (
    <div className="App">
      <header className="App-header">
        <h1 className="app-name">Data labeller</h1>
        {
          getComment(index, setIndex, data, setData, total, sentiment, setSentiment, reason, setReason)
        }
        
      </header>
    </div>
  );  
}

export default App;
