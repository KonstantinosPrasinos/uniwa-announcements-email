require('dotenv').config();
const express = require('express');
const fs = require('fs');
const parseString = require('xml2js').parseString;

const app = express();

const checkForUpdates = () => {
    fetch('http://www.ice.uniwa.gr/feed/')
        .then(response => response.text())
        .then(data => parseString(data, function (err, result) {
            const latestItem = result.rss.channel[0].item[0]
            console.log(Date.parse(latestItem.pubDate));
        }));
}

app.listen(process.env.PORT, () => {
    console.log('Listening on port: ', process.env.PORT);
    checkForUpdates();
    setInterval(checkForUpdates, 5 * 60 * 1000);
})