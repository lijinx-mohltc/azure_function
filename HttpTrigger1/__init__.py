import logging

import azure.functions as func
from openpyxl import Workbook, load_workbook

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    file = req.body('file')
    if not file:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            file = req_body.get('file')

    if file:   
        # wb = load_workbook(file)  
        return func.HttpResponse(file)
        # return func.HttpResponse(wb.get_sheet_names())
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
