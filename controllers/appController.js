const axios = require('axios');
const fs = require('fs')
const path = require('path')



exports.index = (req,res)=>{
    return res.render('landing')
}

exports.sentiment = (req,res)=>{
    return res.render('index')
}

exports.about = (req,res) =>{
    return res.render('about')
}


exports.test = (req, res) => {
    fs.readFile('./sentiment.json', 'utf-8', (err, data) => {
        if (err) {
            console.error('Error reading file:', err);
            return res.status(500).send('Server Error');
        }
        const result = JSON.parse(data);
        return res.render('test', { result });
    });
};

exports.search = async (req, res) => {
    const ticker = req.body.ticker || "";
    const keywords = req.body.keywords || "";
    const country = req.body.country.replace(/\s+/g, '') || "";
    
    try {
        const response = await axios.post(`http://localhost:5000/analyse?ticker=${ticker}&keywords=${keywords}&country=${country}`);
        const result = response.data;          
        return res.render('sentiment_result', { result: result });
    } catch (error) {
        console.error("Error in search function:", error);
        return res.status(500).send("An error occurred while processing your request.");
    }
};

exports.predictions = (req,res)=>{
    return res.render('stockPredict')
}

exports.predict = async (req, res) => {
    const ticker = req.body.ticker || "";
    const date = req.body.date != null? req.body.date: "2020-01-01";
    const period = req.body.period || 1;

    try {
        // Send data in POST body
        const result = await axios.post(`http://localhost:5000/predict?ticker=${ticker}&date=${date}&period=${period}`);
        return res.render('predictions', { result: result.data });
    } catch (error) {
        console.log(error);
        res.status(500).send("Error fetching predictions");
    }
};


exports.marketMood = async (req, res) => {
    res.render("marketMood")
}

exports.mood = async (req, res) => {
    const ticker = req.body.ticker || "";
    
    try {
        const response = await axios.get(`http://localhost:5000/marketMood?ticker=${ticker}`);
        const result = response.data;          
        return res.render('sentiment_result', { result: result });
    } catch (error) {
        console.error("Error in search function:", error);
        return res.status(500).send("An error occurred while processing your request.");
    }
};