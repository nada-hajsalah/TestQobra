import json
import pandas as pd



def read_data(name_file):
    
    with open(name_file, 'r') as f:
        data = json.load(f)

    df_users = pd.json_normalize(data, record_path =['users']).rename(columns={"id":"user_id"})
    df_deals = pd.json_normalize(data, record_path =['deals']).rename(columns={"user":"user_id","id":"deal_id"})
    #Fusion de deux tableaux
    df=pd.merge(df_users, df_deals, on='user_id')
    

    return df

def calcul_comissions(sum_amount,number_deals):
    comission=0
    if number_deals<3:
        comission=0.1*sum_amount
    else:
        comission=0.2*sum_amount
    if sum_amount>2000:
        comission+=500
    return comission

def apply_calcul(data):

    data=data.groupby('user_id').agg(sum_amount=('amount','sum'),
                             number_deals=('deal_id', 'count'))
    data["comission"]= data.apply(lambda x: calcul_comissions(x.sum_amount, x.number_deals), axis=1)
    data=data.reset_index()


    return data

def  data_to_json(data, path_file_output):
    output=data[["user_id","comission"]].to_dict(orient="records")
    output_json={"comissions":output}
    #write in file.json
    with open(path_file_output, 'w') as outfile:
        outfile.write(json.dumps(output_json,indent=4))
    return output_json


if __name__ == "__main__":
    input_path='data/input.json'
    output_path="data/output.json"
    #load data
    print("***Load Data**")
    data=read_data(input_path)
    print(data.head(10))
    #Calcul des comissions
    print("***Calcul des comissions***")
    comissions=apply_calcul(data)
    print(comissions.head(10))
    #Write in json file
    print("***Json output""")
    output=data_to_json(comissions,output_path)
    print(output)