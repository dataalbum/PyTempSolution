var mqtt = require('mqtt'), url = require('url');
// Parse 
var mqtt_url = url.parse(process.env.CLOUDMQTT_URL || 'mqtt://cceilikx:xeRm-2E3Wmby@m20.cloudmqtt.com:11455');
var auth = (mqtt_url.auth || ':').split(':');

// Create a client connection
var client = mqtt.createClient(mqtt_url.port, mqtt_url.hostname, {
    username: auth[0],
    password: auth[1]
});

client.on('connect', function () { // When connected
    
    // subscribe to a topic
    client.subscribe('pytemp-ins/temperature', function () {
        // when a message arrives, do something with it
        client.on('message', function (topic, message, packet) {
            console.log("Received: " + message + "' on '" + topic + "'");
            data = JSON.parse(message);
            console.log(data.timestamp);
        });
    });
    
    // publish a message to a topic
    /*client.publish('hello/world', 'my message', function () {
        console.log("Message is published");
        client.end(); // Close the connection when published
    });*/
});