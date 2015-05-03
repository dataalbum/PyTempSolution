var amqp = require('amqp');
var MongoClient = require('mongodb').MongoClient;

var amqpconn = amqp.createConnection({ url: 'amqp://ontpcbos:7G7Ilh2wbERfJNHZMhfHTHJPaj4GDGu1@bunny.cloudamqp.com/ontpcbos' });

amqpconn.on('ready', function () {
    amqpconn.exchange('temperature', {
        type: 'fanout',
        autoDelete: false
    }, function (exchange) {
        amqpconn.queue('tmp-' + Math.random(), { exclusive: true },
                         function (queue) {
            queue.bind('temperature', '');
            console.log(' [*] Waiting for messages. To exit press CTRL+C')
            
            queue.subscribe(function (msg) {
                console.log(" [x] Recieved: ", msg.data.toString('utf-8'));
                
                console.log(" Type: ", typeof msg.data);
                var tempData = JSON.parse(msg.data.toString('utf-8'));
                var tempDatatest = msg.data.toString('utf-8');
                
                console.log(" Message: ", tempData)
                console.log(" Lenght: ", tempData.length)

                //MongoDB connetion
                MongoClient.connect('mongodb://127.0.0.1:27017/logs', function (err, db) {
                    if (err) throw err;
                    console.log("Connected to Database");
                    
                    // insert multiple documents
                    db.collection('templog').insert(tempData, function (err, result) {
                        if (err) throw err;
                        console.log(" Record added as " + tempData[0]._id);
                    });
                });
               
            });
        })
    });
});