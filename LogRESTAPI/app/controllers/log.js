var mongoose = require('mongoose'),
    Log = mongoose.model("Log"),
    ObjectId = mongoose.Types.ObjectId

exports.createLog = function (req, res, next) {
    var logModel = new Log(req.body);
    logModel.save(function (err, log) {
        if (err) {
            res.status(500);
            res.json({
                type: false,
                data: "Error occured: " + err
            })
        } else {
            res.json({
                type: true,
                data: log
            })
        }
    })
}

exports.viewLog = function (req, res, next) {
    Log.findById(new ObjectId(req.params.id), function (err, log) {
        if (err) {
            res.status(500);
            res.json({
                type: false,
                data: "Error occured: " + err
            })
        } else {
            if (log) {
                res.json({
                    type: true,
                    data: log
                })
            } else {
                res.json({
                    type: false,
                    data: "Log: " + req.params.id + " not found"
                })
            }
        }
    })
}

exports.viewLog_v2 = function (req, res, next) {
    Log.findById(new ObjectId(req.params.id), function (err, log) {
        if (err) {
            res.status(500);
            res.json({
                type: false,
                data: "Error occured: " + err
            })
        } else {
            if (log) {
                log.title = log.title + " v2"
                res.json({
                    type: true,
                    data: log
                })
            } else {
                res.json({
                    type: false,
                    data: "Log: " + req.params.id + " not found"
                })
            }
        }
    })
}

exports.updateLog = function (req, res, next) {
    var updatedLogModel = new Log(req.body);
    Log.findByIdAndUpdate(new ObjectId(req.params.id), updatedLogModel, function (err, log) {
        if (err) {
            res.status(500);
            res.json({
                type: false,
                data: "Error occured: " + err
            })
        } else {
            if (log) {
                res.json({
                    type: true,
                    data: log
                })
            } else {
                res.json({
                    type: false,
                    data: "Log: " + req.params.id + " not found"
                })
            }
        }
    })
}

exports.deleteLog = function (req, res, next) {
    Log.findByIdAndRemove(new Object(req.params.id), function (err, log) {
        if (err) {
            res.status(500);
            res.json({
                type: false,
                data: "Error occured: " + err
            })
        } else {
            res.json({
                type: true,
                data: "Log: " + req.params.id + " deleted successfully"
            })
        }
    })
}