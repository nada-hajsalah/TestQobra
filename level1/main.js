
/**
 * 
 * @param {String} path 
 * @returns 
 */
function readJsonFile(path) {
    try {
        var json = require(path);
        return json;
    }
    catch (err) { throw err; }
}



/**
 * 
 * @param {Number} TotalAmount 
 * @param {Number} numberDeals 
 * @returns 
 */
function calculComission(TotalAmount, numberDeals) {
    var comission = 0
    if (numberDeals < 3) {
        comission = 0.1 * TotalAmount;
    }
    else {
        comission = 0.2 * TotalAmount;
    }
    if (TotalAmount > 2000) {
        comission += 500;
    }
    return comission;
}
/**
 * 
 * @param {Json} data 
 * @returns 
 */
function applyCalcul(data) {
    var comissions = [];

    for (key in data.users) {
        var comission = 0;
        var userID = data.users[key].id;
        var outputUser = data['deals'].filter(x => x.user == userID);
        if (outputUser.length > 0) {
            var TotalAmount = outputUser.map(x => x.amount).reduce((a, b) => a + b);//calculate the sum of amount for each user
            var numberDeals = outputUser.length;
            var comission = calculComission(TotalAmount, numberDeals);
        }
        comissions.push({ user_id: userID, commission: comission });


    }
    return comissions;

}
/**
 * 
 * @param {Array} output 
 * @param {String} pathFileOutput 
 */
function dataToJson(output, pathFileOutput) {
    outputJson = { "comissions": output }
    outputData = JSON.stringify(outputJson);

    console.log(outputData);
    var fs = require("fs");
    fs.writeFile(pathFileOutput, outputData, (err) => {
        if (err) {
            throw err;
        }
        console.log("JSON data is saved.");
    });



}
const pathFileInput = './data/input.json'
const pathFileOutput  = './data/output.json';       

var dataUser = readJsonFile(pathFileInput);
comissions = applyCalcul(dataUser);
dataToJson(comissions, pathFileOutput);