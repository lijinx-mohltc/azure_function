import pandas_schema
from pandas_schema import Column, Schema
from pandas_schema.validation import CustomElementValidation, LeadingWhitespaceValidation, InListValidation,CustomSeriesValidation
from pandas_schema.validation import TrailingWhitespaceValidation, CanConvertValidation, MatchesPatternValidation, InRangeValidation 
    
from decimal import *
import numpy as np
import math



def check_decimal(dec):
    try:
        int(dec)
    except ValueError:
        return False
    return True

def validate(data):
    decimal_validation = [CustomElementValidation(lambda d: check_decimal(d), 'is not decimal')]
    null_validation = [CustomElementValidation(lambda d: d , 'this field cannot be null')]
    test = [CustomElementValidation(lambda d: check_decimal(d), 'invalideted') | CustomElementValidation(lambda d: str(d).__contains__('nan'),"")]
    range_text = [CustomElementValidation(lambda d: (d>=0)&(d<100), 'not range')]
    range_number = [CustomElementValidation(lambda d: (d>=0)&(d<10000000), 'not range') | CustomElementValidation(lambda d: str(d).__contains__('nan'),"")]
   
    schema = pandas_schema.Schema([
                Column('RevExp'),
                Column('budget', test + range_number),
                Column('budgetA', test),
                Column('total', test),
                Column('YTDA', test),
                Column('Q4F', test),
                Column('Q4FTB',test),
                Column('Q4FTBP', test),
                Column('comments')
                ])
    errors = schema.validate(data)
    # for e in errors:
    #     print(e)
    # errors_index = {"row":[e.row for e in errors],"column":[e.column for e in errors]}
    return errors