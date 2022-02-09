/**
 * 
 * @param {String} path 
 * @returns 
 */
function readJsonFile(path) {
    //read the json file
    try {
        var json = require(path);
        return json;
    }
    catch (err) { throw err; }
}
/**
 * 
 * @param {Array} objectArray 
 * @param {String} property 
 * @returns 
 */
function groupBy(objectArray, property) {
    //Grouped an array by a property
    return objectArray.reduce((acc, obj) => {
        const key = obj[property];
        if (!acc[key]) {
            acc[key] = [];
        }
        // Add object to list for given key's value
        acc[key].push(obj);
        return acc;
    }, {});
}
/**
 * 
 * @param {String} date 
 * @returns 
 */
function extractDate(date) {
    //extract the year and mouth from date
    return date.slice(0, -3);

}
/**
 * 
 * @param {Array} array 
 */
function setDate(array) {
    // for each deal change the date format from YYYY-MM-DD to YYYY-MM
    array.forEach((deal) => {

        deal.close_date = extractDate(deal.close_date);
        deal.payment_date = extractDate(deal.payment_date);

    });

}
/**
 * 
 * @param {Json} data 
 * @returns 
 */
function groupBydate(data) {
    // group the data by user and close date
    deals = [];
    setDate(data.deals)
    var result = groupBy(data.deals, "user")
    for (i in result) {

        var objective = data.users.find(el => el.id === Number(i)).objective;


        var resultmouth = groupBy(result[i], "close_date");
        for (key in resultmouth) {
            let cumsum = 0;

            const newData = resultmouth[key].map(({ id, amount, user, close_date, payment_date }) => ({ id, amount, user, close_date, payment_date, currentAmount: cumsum += amount }));// cumulative sum of the amount
            const comissions = newData.map(({ id, amount, user, close_date, payment_date, currentAmount }) => ({ id, amount, user, close_date, payment_date, comission: calculComission(amount, currentAmount, objective) }));
            deals.push(comissions);

        }
    }
    return deals;
}
/**
 * 
 * @param {Number} amount 
 * @param {Number} currentAmount 
 * @param {Number} objective 
 * @returns 
 */
function calculComission(amount, currentAmount, objective) {
    comission = 0
    precedentAmount = currentAmount - amount
    demiObjective = 0.5 * objective
    if (currentAmount > objective) {
        if (precedentAmount >= objective) {
            comission = 0.15 * amount;
        }
        else if (precedentAmount >= demiObjective) {
            comission = (currentAmount - objective) * 0.15;
            comission += (amount - (currentAmount - objective)) * 0.1;
        }
        else {
            comission = (currentAmount - objective) * 0.15;
            comission += demiObjective * 0.15;
        }
    }
    else if (currentAmount > demiObjective) {
        if (precedentAmount >= demiObjective) {
            comission = amount * 0.1;
        }
        else {

            comission = (currentAmount - demiObjective) * 0.1;
            comission += (amount - (currentAmount - demiObjective)) * 0.05;
        }
    }
    else {
        comission = amount * 0.05;
    }
    return comission;
}
/**
 * 
 * @param {Array} data 
 * @returns 
 */
function objectComissions(data) {
    //Create the object comissions
    comissionsObject = []

    var dataUser = groupBy(data.flat(), "user")
    for (id in dataUser) {
        comissions = {}
        var dealDate = groupBy(dataUser[id], "payment_date");
        for (deal in dealDate) {
            var Totalcomission = dealDate[deal].map(x => x.comission).reduce((a, b) => a + b);// sum the amount of comission for each user grouped by payment date

            comissions[deal] = Totalcomission
        }
        comissionsObject.push({ "user_id": Number(id), "comissions": comissions })
    }
    return comissionsObject
}
//write output in json file
/**
 * 
 * @param {Array} comissions 
 * @param {Array} users 
 * @param {String} pathFileOutput 
 */
function dataToJson(comissions, users, pathFileOutput) {
    var deals = comissions.flat().map(({ id, amount, user, close_date, payment_date, comission }) => ({ id, comission }));// create the deals object
    var output = { "comissions": users, "deals": deals };
    var outputData = JSON.stringify(output, null, 4);

    console.log(outputData);
    var fs = require("fs");
    fs.writeFile(pathFileOutput, outputData, (err) => {
        if (err) {
            throw err;
        }
        console.log("JSON data is saved.");
    });



}


var data = readJsonFile('./data/input.json');
var deals = groupBydate(data);
var users = objectComissions(deals);
dataToJson(deals, users, './data/output.json');



