import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import 'bootstrap/dist/css/bootstrap.min.css';

import React, { useState } from 'react';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import ToggleButton from 'react-bootstrap/ToggleButton';
import InputGroup from 'react-bootstrap/InputGroup';
import Form from 'react-bootstrap/Form';

function Comment(props) {
  let index = props.index;
  let data = props.data;
  let callback = props.callback;
  let prev = props.prev;
  let total = props.total;
  let expected = props.expected;
  let setSentiment = props.setSentiment;
  let reason = props.reason;
  let setReason = props.setReason;

  let gpt;
  data.sentiment_analysis.forEach((se) => {
    if (se?.classifier === "gpt") {
      gpt = se;
    }
  });

  function updateReason(newReason) {
    let newData = {
      "classifier" : "alshakoush",
      "sentiment" : expected,
      "reason" : reason
    };

    newData.reason = newReason;
    let ses = data.sentiment_analysis;
    for (let index in ses) {
      let se = ses[index];
      if (se && se.classifier === "alshakoush") {
        ses[index] = newData;
        setReason(newReason);
        return;
      }
    }
    data.sentiment_analysis.push(
      newData
    );
    setReason(newReason);
  }


  function updateResponse(event) {
    let newData = {
      "classifier" : "alshakoush",
      "sentiment" : expected,
      "reason" : reason
    };

    
    let response = event.target.value;
    newData.sentiment = response;
    let ses = data.sentiment_analysis;
    for (let index in ses) {
      let se = ses[index];
      if (se && se.classifier === "alshakoush") {
        ses[index] = newData;
        setSentiment(response);
        return
      }
    }
    data.sentiment_analysis.push(
      newData
    );
    setSentiment(response);
  }




  return (
    <>
    <Card className="text-center">
    <Card.Header>Comment #{index}</Card.Header>
    <Card.Body>
      <Card.Title></Card.Title>
      <Card.Text>
      {data.content.message}
      </Card.Text>
      <ButtonGroup aria-label="Basic example">
        <ToggleButton key={1} id='rad-1' type="radio" name='radio' checked={expected === "unknown"} variant="outline-info" value={"unknown"}   onChange={updateResponse}>Unknown</ToggleButton>
        <ToggleButton key={2} id='rad-2' type="radio" name='radio' checked={expected === "negative"} variant="outline-danger" value={"negative"}    onChange={updateResponse}>Negative</ToggleButton>
        <ToggleButton key={3} id='rad-3' type="radio" name='radio' checked={expected === "neutral"} variant="outline-secondary" value={"neutral"} onChange={updateResponse}>Neutral</ToggleButton>
        <ToggleButton key={4} id='rad-4' type="radio" name='radio' checked={expected === "positive"} variant="outline-success" value={"positive"}   onChange={updateResponse}>Positive</ToggleButton>
      </ButtonGroup>
      
      <br/>
      {
        expected !== "" ?
        <ButtonGroup aria-label="Basic example">
          <ToggleButton key={5} id='rad-5' type='radio' name='radio' checked={expected === ""} variant="outline-dark" value={""}  onChange={updateResponse}>Remove Sentiment</ToggleButton>
        </ButtonGroup>
        : 
        null
      }

      <br/>

      <>
      <InputGroup>
        <InputGroup.Text>Reason</InputGroup.Text>
        <Form.Control
          aria-label="Large"
          as="textarea"
          value={reason}
          onChange={(event) => updateReason(event.target.value)}
        >
        </Form.Control> 
      </InputGroup>
      </>

      <br/>
      
      <ButtonGroup aria-label="Basic example">
        <Button variant="secondary" onClick={prev}>Previous Comment</Button>
        <Button variant="primary" value={expected} onClick={callback}>Next Comment</Button>
      </ButtonGroup>

      <br/>


    </Card.Body>
    <Card.Footer className="text-muted">Total : {total} | left : {total - index}</Card.Footer>
  </Card>

  <br/>

  <Card className="text-center">
    <Card.Header>GPT - Comment #{index}</Card.Header>
    <Card.Body>
      <Card.Title></Card.Title>
      <Card.Text>
      
      <ButtonGroup aria-label="Basic examplex2">
        <ToggleButton key={8} id='rad-8' type="radio" name='radio-gpt' checked={gpt.sentiment === "unknown"} variant="outline-info" >Unknown</ToggleButton>
        <ToggleButton key={9} id='rad-9' type="radio" name='radio-gpt' checked={gpt.sentiment === "negative"} variant="outline-danger"  >Negative</ToggleButton>
        <ToggleButton key={10} id='rad-10' type="radio" name='radio-gpt' checked={gpt.sentiment === "neutral"} variant="outline-secondary"> Neutral</ToggleButton>
        <ToggleButton key={11} id='rad-11' type="radio" name='radio-gpt' checked={gpt.sentiment === "positive"} variant="outline-success" >Positive</ToggleButton>
      </ButtonGroup>

      <br/>
      <br/>
      <>
      <InputGroup>
        <InputGroup.Text>Reason</InputGroup.Text>
        <Form.Control
          aria-label="Large"
          as="textarea"
          value={gpt.reason}
          // readOnly
          disabled
        >
        </Form.Control> 
      </InputGroup>
      </>

      </Card.Text>

      <ButtonGroup aria-label="Basic examplex3">
        <Button variant="secondary" onClick={() => updateReason(gpt.reason)}>Use same reason</Button>
        <Button variant="primary" onClick={() => updateResponse({target: {value: gpt.sentiment}})}>Use same sentiment</Button>
      </ButtonGroup>

    </Card.Body>
  </Card>
  </>
  );  
}

export default Comment;
