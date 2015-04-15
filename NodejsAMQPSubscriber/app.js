//amqp://ontpcbos:7G7Ilh2wbERfJNHZMhfHTHJPaj4GDGu1@bunny.cloudamqp.com/ontpcbos

var amqp = require('amqplib');

amqp.connect('amqp://ontpcbos:7G7Ilh2wbERfJNHZMhfHTHJPaj4GDGu1@bunny.cloudamqp.com/ontpcbos').then(function (conn) {
    process.once('SIGINT', function () { conn.close(); });
    return conn.createChannel().then(function (ch) {
        
        var ok = ch.assertQueue('temperature', { durable: false });
        
        ok = ok.then(function (_qok) {
            return ch.consume('temperature', function (msg) {
                console.log(" [x] Received '%s'", msg.content.toString());
            }, { noAck: true });
        });
        
        return ok.then(function (_consumeOk) {
            console.log(' [*] Waiting for messages. To exit press CTRL+C');
        });
    });
}).then(null, console.warn);
