import logging
import io
import azure.functions as func
import base64
import json
import pandas as pd
from .validation import validate

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    file = req.get_json()
    data = file['body']['$content']
    decrypted=base64.b64decode(data)
    toread = io.BytesIO()
    toread.write(decrypted)
    # toread.seek(0)
    df = pd.read_excel(toread, sheet_name='Fin_CMHP1', usecols="C:K",skiprows=7)
    df.rename(columns={"LHIN Program:  Revenue & Expenses":"RevExp","Total":"total","YTD Actual":"YTDA",
                            "Budget":"budget", "Budget Adjustments":"budgetA",
                            "Q4 Forecast":"Q4F","Q4 $ Forecast Variance to Budget":"Q4FTB","Q4 % Forecast Variance to Budget":"Q4FTBP",
                            "Comments\nExplanations are required where \nthe Q4 Forecasted % exceeds +/-10%":"comments"},inplace=True)
    error = validate(df)
    for i in range(0, len(error['row'])):
        df.at[error['row'][i],error['column'][i]] = "error"
    df.to_excel("error.xlsx", sheet_name='Fin_CMHP1')
    # print(df.to_json())
    # db = json.loads(file['body']['$content']) 
    # df = pd.DataFrame(db)
  
        # wb = load_workbook(file)  
    with open("error.xlsx", "rb") as f:
        errordata = f.read()
    
    # output = StringIO.StringIO()
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Fin_CMHP1')
    writer.save()

    encoded = base64.b64encode(output.getvalue()) 
    jsonback = {"message":"", "data": str(encoded)}

    return func.HttpResponse(json.dumps(jsonback))
        # return func.HttpResponse(wb.get_sheet_names())
