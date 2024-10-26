const express = require("express")
const app = express()
const controller = require('./controllers/appController.js')
const path = require('path')



app.set('view engine', 'ejs')
app.use(express.json())
app.use(express.urlencoded({ extended: true }))
app.use(express.static(path.join(__dirname, "public")))


app.get('/',controller.index)

app.get('/about',controller.about)

app.listen(3000)