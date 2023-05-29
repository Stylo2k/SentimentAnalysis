const express = require('express');
const bodyParser = require('body-parser');
var cors = require('cors')
const app = express();
const fs = require('fs');

var logger = require('express-logger');

let port = 80;
let clean = false;

app.use(logger({path: "./logfile.txt"}));
app.use(cors());
app.use(bodyParser.json());


// get port from dotenv
require('dotenv').config();
if (process.env.PORT) {
    port = process.env.PORT;
}


let commitsData, issuesData;
if (clean) {
    console.log("Starting server with clean data");
    commitsData =require('../../dataset_labelled_v3.json');
    issuesData = require('../../dataset_issues_sentiment_v2.json');
} else {
    commitsData = require('./dataset_labelled_v4.json');
    issuesData = require('./dataset_issues_sentiment_v3.json');
}

async function saveIssues(version) {
    fs.writeFile(`./labelled-data/dataset_issues_sentiment_v${version-1}.json`, JSON.stringify(issuesData, null, 4), (err) => {
        if (err) {
            console.log(err);
            return;
        }
        console.log("Saved issues");
    });
}

async function saveCommits(version) {
    fs.writeFile(`./labelled-data/dataset_labelled_v${version}.json`, JSON.stringify(commitsData, null, 4), (err) => {
        if (err) {
            console.log(err);
            return;
        }
        console.log("Saved commits");
    });
}

async function saveData(type) {
    let version = 4;
    if (clean) {
        version += '_clean_'
    }
    if (type === 'issues') saveIssues(version);
    if (type === 'commits') saveCommits(version);
}



app.get('/api/commits/total', (req, res) => {
    res.send({total: commitsData.length});
    }
);

app.get('/api/issues/total', (req, res) => {
    res.send({total: issuesData.length});
    }
);


app.get('/api/commits/:index', (req, res) => {
    const index = req.params.index;
    res.send(commitsData[index]);
    }
);

app.get('/api/issues/:index', (req, res) => {
    const index = req.params.index;
    res.send(issuesData[index]);
    }
);

app.put('/api/commits/:index', (req, res) => {
    const index = req.params.index;
    const data = req.body;
    commitsData[index] = data;
    saveData('commits');
    res.send(commitsData[index]);
    }
);

app.put('/api/issues/:index', (req, res) => {
    const index = req.params.index;
    const data = req.body;
    issuesData[index] = data;
    saveData('issues');
    res.send(issuesData[index]);
    }
);


app.listen(port, () => console.log(`Listening on port - ${port}`));