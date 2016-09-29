var express = require('express');
var app = express();

app.use(function(req, res, next){
	console.info(req.headers)
	req.on("data", function(chunk){
		console.info("Chunk:", chunk)
	})	
	req.on("end", function(){
		next()
	})
})


app.get('/', function(req, res) {
	res.sendStatus(200)
	res.send("Hello World!");
	res.set("Connection", "close")
	res.end()

})

app.listen(3000, function() {
	console.log("Example app listening on port 3000!");
})

