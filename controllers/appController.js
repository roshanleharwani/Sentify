
const axios = require('axios');

exports.index = (req,res)=>{
    return res.render('index')
}

exports.about = (req,res) =>{
    return res.render('about')
}





exports.search = async (req, res) => {
    const ticker = req.body.ticker || "";
    const keywords = req.body.keywords || "";
    
    try {
        // Add protocol to the URL and await the response, then access .data
        const response = await axios.post(`http://localhost:5000/analyse?ticker=${ticker}&keywords=${keywords}`);
        const result = response.data;  // Access the data property of the response
        
        return res.render('sentiment_result', { result: result });
    } catch (error) {
        console.error("Error in search function:", error);
        return res.status(500).send("An error occurred while processing your request.");
    }
};
