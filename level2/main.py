
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


def calculComission(totalAmount, objective):
    """calculation of commission on the total amount

    :param totalAmount: total sales amount  for each user
    :type totalAmount: float
    :param objective: target amount of commission that each user wants to achieve
    :type objective: float
    :return: a number
    :rtype: float
    """
    demiObjective = objective * 0.5
    comission = 0.05*demiObjective
    if (totalAmount > objective):
        comission += 0.15*(totalAmount-objective)
        comission += demiObjective * 0.1
    elif (totalAmount > demiObjective):
        comission += 0.1*(totalAmount-(objective*0.5))
        comission += demiObjective * 0.05

    return comission


def applyCalcul(data):
    """calculation of total sales amount  and the objective each user to calculate the commission 
    :param data: json Array
    :return: the id of user and his comissions
    :rtype: list
    """
    dictJson = []

    for user in data["users"]:
        userId = user["id"]
        objective = user["objective"]
        output_user = [deal for deal in data['deals']
                       if deal['user'] == userId]
        totalAmount = sum(x["amount"] for x in output_user)
        comission = calculComission(totalAmount, objective)
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
    input_path = 'data/input.json'
    output_path = "data/output.json"
    # load data
    print("***Load Data**")
    data = readData(input_path)
    print(data)
    # Calcul des comissions
    print("***Calcul des comissions***")
    comissions = applyCalcul(data)
    # Write in json file
    print("***Json output""")
    print(dataToJson(comissions, output_path))
