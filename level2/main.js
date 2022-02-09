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
 * @param {Number} objective
 * @returns 
 */
function calculComission(totalAmount, objective) {

    var demiObjective = objective * 0.5;
    var comission = 0.05 * demiObjective;
    if (totalAmount > objective) {
        comission += 0.15 * (totalAmount - objective);
        comission += demiObjective * 0.1
    }
    else if (totalAmount > demiObjective) {
        comission += 0.1 * (totalAmount - (objective * 0.5));
        comission += demiObjective * 0.05
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
        var userID = data.users[key].id;
        var comission = 0;
        var outputUser = data['deals'].filter(x => x.user == userID);

        if (outputUser.length > 0) {

            var totalAmount = outputUser.map(x => x.amount).reduce((a, b) => a + b);//calculate the sum of amount for each user
            var objective = data.users[key].objective;
            var comission = calculComission(totalAmount, objective);
        }

        comissions.push({ user_id: userID, commission: comission });


    }
    return comissions;

}
//write output in json file
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
const pathFileOutput = './data/output.json';

var dataUser = readJsonFile(pathFileInput);
comissions = applyCalcul(dataUser);
dataToJson(comissions, pathFileOutput);