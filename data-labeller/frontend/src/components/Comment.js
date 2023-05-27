import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import 'bootstrap/dist/css/bootstrap.min.css';

import React, { useState } from 'react';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import ToggleButton from 'react-bootstrap/ToggleButton';


function Comment(props) {
  let index = props.index;
  let data = props.data;
  let callback = props.callback;
  let prev = props.prev;
  let total = props.total;
  let expected = props.expected;
  let setSentiment = props.setSentiment;

  function updateResponse(event) {
    let response = event.target.value;
    data.sentiment_analysis.push(
      {
        "classifier": "alshakoush",
        "sentiment": response,
        "reason": ""
      }
    );
    setSentiment(response);
  }

  return (
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
      
      <ButtonGroup aria-label="Basic example">
        <Button variant="secondary" onClick={prev}>Previous Comment</Button>
        <Button variant="primary" value={expected} onClick={callback}>Next Comment</Button>
      </ButtonGroup>

    </Card.Body>
    <Card.Footer className="text-muted">Total : {total} | left : {total - index}</Card.Footer>
  </Card>
  );  
}

export default Comment;
