const express = require("express")
const app = express()
const controller = require('./controllers/appController.js')
const path = require('path')
const bodyParser = require('body-parser')


app.set('view engine', 'ejs')
app.use(express.json())
app.use(express.urlencoded({ extended: true }))
app.use(express.static(path.join(__dirname, "public")))
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.get('/',controller.index)

app.get('/about',controller.about)

app.post('/search',controller.search)

app.listen(3000)