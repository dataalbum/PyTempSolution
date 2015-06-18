var mongoose = require("mongoose");
var Schema = mongoose.Schema;

var LogSchema = new Schema( {
    displayname: String, 
    location: String,
    measurename: String,
    unitofmeasure: String,
    value: String,
    timestamp: String
}, { versionKey: false });
mongoose.model('Log', LogSchema);