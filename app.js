const express = require("express")
const app = express()
const controller = require('./controllers/appController.js')
const path = require('path')
const bodyParser = require('body-parser')
const fs = require('fs')
const ejsmate = require('ejs-mate')

app.set('view engine', 'ejs')
app.engine("ejs", ejsmate);
app.use(express.json())
app.use(express.urlencoded({ extended: true }))
app.use(express.static(path.join(__dirname, "public")))
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());


app.get('/sentiment',controller.sentiment)

app.get('/about',controller.about)

app.post('/search',controller.search)

app.get('/stockPrice',controller.predictions)

app.post('/predict',controller.predict)

app.get('/',controller.index)

app.get('/test',controller.test)

app.get('/marketMood',controller.marketMood)

app.post('/marketSentiment',controller.mood)

app.listen(3000)