
import json


def readData(pathFileInput):
    """Read a json file

    :param pathFileInput: the path of the input file
    :type pathFileInput: str
    :return: json array

    """
    with open(pathFileInput, 'r') as f:
        data = json.load(f)

    return data


def calculComissions(sumAmount, numberDeals):
    """calculation of commission on the total amount

    :param sumAmount: total sales amount  for each user
    :type sumAmount: float
    :param numberDeals: number of total deals for each user
    :type numberDeals: int
    :return: a number
    :rtype: float
    """
    comission = 0
    if numberDeals < 3:
        comission = 0.1*sumAmount
    else:
        comission = 0.2*sumAmount
    if sumAmount > 2000:
        comission += 500
    return comission


def applyCalcul(data):
    """calculation of total sales amount  and number of dealsfor each user to calculate the commission 
    :param data: json Array
    :return: the id of user and his comissions
    :rtype: list
    """
    dictJson = []

    for user in data["users"]:
        userId = user["id"]
        # If the user don't have any deal yet, comission=0
        outputUser = [deal for deal in data['deals'] if deal['user'] == userId]
        totalAmount = sum(x["amount"] for x in outputUser)
        numberDeals = len(outputUser)
        comission = calculComissions(totalAmount, numberDeals)
        dictJson.append({"user_id": userId, "comission": comission})
    return dictJson


def dataToJson(output, pathFileOutput):
    """ write the output in a json file
    :param output: list of json data
    :return: dict

    """
    outputJson = {"comissions": output}
    #write in file.json
    with open(pathFileOutput, 'w') as outfile:
        outfile.write(json.dumps(outputJson, indent=4))
    return outputJson


if __name__ == "__main__":
    inputPath = 'data/input.json'
    outputPath = "data/output.json"
    # load data
    print("***Load Data**")
    data = readData(inputPath)
    print(data)
    # Calculation of commissions
    print("***Calcul des comissions***")
    comissions = applyCalcul(data)
    # Write in json file
    print("***Json output""")
    print(dataToJson(comissions, outputPath))
