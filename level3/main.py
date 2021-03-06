import json
import pandas as pd


def extractDate(date):
    """Extract the year and mouth from date

    :param date
    :type date: str
    :return: str
    """
    dateListe = date.split("-")
    return "-".join(dateListe[:2])


def readData(pathFileInput):
    """Read a json file into a dataframe and merge the two objects json

    :param pathFileInput: the path of the input file
    :type pathFileInput: str
    :return: dataframe
    """

    with open(pathFileInput, 'r') as f:
        data = json.load(f)

    df_users = pd.json_normalize(data, record_path=['users']).rename(
        columns={"id": "user_id"})
    df_deals = pd.json_normalize(data, record_path=['deals']).rename(
        columns={"user": "user_id"})
    # Merge of two objects
    df = pd.merge(df_users, df_deals, on='user_id')
    df["close_date"] = df["close_date"].apply(
        lambda x: extractDate(x))  # modify the value of date:YYYY-MM
    df["payment_date"] = df["payment_date"].apply(
        lambda x: extractDate(x))  # modify the value of date:YYYY-MM

    return df


def calculComission(amount, currentAmount, objective):
    """calculation of commission for each deal

    :param amount: the amount of a deal
    :type amount: float
    :param currentAmount: the cumulative sum of amount
    :type amount: float
    :param objective: target amount of commission that each user wants to achieve
    :type objective: float
    :return: a number
    :rtype: float
    """
    comission = 0
    precedentamount = currentAmount-amount
    demiObjective = 0.5*objective
    if currentAmount > objective:
        if precedentamount >= objective:
            comission = 0.15*amount
        elif precedentamount >= demiObjective:
            comission = (currentAmount-objective)*0.15
            comission += (amount-(currentAmount-objective)) * \
                0.1  # interval[50%-100%]
        else:
            comission = (currentAmount-objective)*0.15
            comission += demiObjective*0.15  # two intervals
    elif currentAmount > demiObjective:
        if precedentamount >= demiObjective:
            comission = amount*0.1
        else:

            comission = (currentAmount-demiObjective)*0.1
            comission += (amount-(currentAmount-demiObjective))*0.05
    else:
        comission = amount*0.05  # intervall[0%-50%]
    return comission


def applyCalcul(data):
    """calculation of comission for each deal of a user grouped by the close date
    :param data: json Array
    :return: dataframe
    """
    data['currentAmount'] = data.groupby(['user_id', 'close_date'])['amount'].apply(
        lambda x: x.cumsum())  # add up the amount for each month for each user

    data["comission"] = data.apply(lambda x: calculComission(
        x.amount, x.currentAmount, x.objective), axis=1)

    # data["comission"]=data.groupby(['user_id','close_date'])["comission"].diff().fillna(data['comission'])
    data = data.reset_index()

    return data


def comissionToDict(data):
    """Creat the object json comissions in the output file
    :param data: json Array
    :return: dict
    """
    comissions = {}
    comissionsObject = []
    data = data.groupby(['user_id', 'payment_date']).agg(
        comissionUser=('comission', 'sum'))
    for i, j in data.index:
        if i not in comissions:
            comissions[i] = {j: data.loc[i, j]['comissionUser']}
        else:
            comissions[i][j] = data.loc[i, j]['comissionUser']
    for i, j in zip(comissions.keys(), comissions.values()):
        comissionsObject.append({"user_id": i, "comission": j})

    return comissionsObject


def dataToJson(data, pathFileOutput):
    """ create the comissions and the deals object and write the output in a json file
    :param data: dataframe
    :return: dict

    """

    comissionsObject = comissionToDict(data)

    # transform the lines of the columns"id"  and "comission" into a dictionary
    dealsObject = data[["id", "comission"]].to_dict(orient="records")

    data = data.reset_index()

    outputJson = {"commissions": comissionsObject, "deals": dealsObject}
    #write in file.json
    with open(pathFileOutput, 'w') as outfile:
        outfile.write(json.dumps(outputJson, indent=4))
    return outputJson


if __name__ == "__main__":
    input_path = 'data/input.json'
    output_path = "data/output.json"

    print("***Load Data**")
    data = readData(input_path)
    print(data.head())
    # Calcul des comissions
    print("***Calcul des comissions***")
    newData = applyCalcul(data)
    print("***Json output""")
    print(dataToJson(newData, output_path))
