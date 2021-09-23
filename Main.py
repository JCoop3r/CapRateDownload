import os
import pyodbc
import pandas as pd
import numpy as np

def qdirect_odbc_connect() -> pyodbc.Connection:
    """
    :return: pyodbc connection object
    """
    server = 'investmentsdatamart.database.windows.net'
    database = 'QIR'
    username = 'QIR_User'
    password = 'Welcome100'
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    return conn

def retrieve_factor_data() -> pd.DataFrame:
    """
    :param segment: choice of data segment to use from database (one of 'CBSA', 'PropertyType', 'PropertySubType')
    :return: dataframe of raw data
    """
    query = f'''
        select a.Date,
            a.Ticker,
            a.FieldCode as Field,
            a.FieldValue as FieldValue
        from FieldValue a
        where  datename(weekday, a.Date) in ('Friday')
        and a.FieldCode IN ('Implied_Cap_Rate')
        and a.Date >= '2016-07-01'
        Order by 1 asc, 2 asc
        '''

    dataset = (
        pd.read_sql_query(query, con=qdirect_odbc_connect())
        #.assign(Date=lambda x: pd.to_datetime(x['Date'], format='%Y%m%d').dt.date)
    )
    return dataset

def main():
    dataset = retrieve_factor_data

if __name__ == '__main__':
        main()
