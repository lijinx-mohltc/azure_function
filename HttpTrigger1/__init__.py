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
    decrypted=base64.b64decode(file['$content'])
    toread = io.BytesIO()
    toread.write(decrypted)
    # toread.seek(0)
    df = pd.read_excel(toread, usecols="C:K",skiprows=7)
    df.rename(columns={"LHIN Program:  Revenue & Expenses":"RevExp","Total":"total","YTD Actual":"YTDA",
                            "Budget":"budget", "Budget Adjustments":"budgetA",
                            "Q4 Forecast":"Q4F","Q4 $ Forecast Variance to Budget":"Q4FTB","Q4 % Forecast Variance to Budget":"Q4FTBP",
                            "Comments\nExplanations are required where \nthe Q4 Forecasted % exceeds +/-10%":"comments"},inplace=True)
    error = validate(df)
    # print(df.to_json())
    # db = json.loads(file['body']['$content']) 
    # df = pd.DataFrame(db)
    if not file:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            file = req_body.get('file')

    if file:   
        # wb = load_workbook(file)  
        return func.HttpResponse(str(error))
        # return func.HttpResponse(wb.get_sheet_names())
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
