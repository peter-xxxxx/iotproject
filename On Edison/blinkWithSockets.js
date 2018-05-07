var m = require('mraa'); //IO Library
var app = require('express')(); //Express Library
var server = require('http').Server(app); //Create HTTP instance

var io = require('socket.io')(server); //Socket.IO Library

var blinkInterval = 200; //set default blink interval to 200 milliseconds (0.2 second)
var ledState = 1; //set default LED state

var myLed = new m.Gpio(13); //LED hooked up to digital pin 13
myLed.dir(m.DIR_OUT); //set the gpio direction to output

app.get('/', function (req, res) {                  
	    res.sendFile(__dirname + '/index.html'); //serve the static html file
});                                                 

io.on('connection', function(socket){
	    socket.on('changeBlinkInterval', function(data){ //on incoming websocket message...
		            blinkInterval = data; //update blink interval
			        });
});                                                   

server.listen(3000); //run on port 3000

blink(); //start the blink function

function blink(){                                                                               
	    myLed.write(ledState); //write the LED state
	        ledState = 1 - ledState; //toggle LED state
		    setTimeout(blink,blinkInterval); //recursively toggle pin state with timeout set to blink interval
}  
