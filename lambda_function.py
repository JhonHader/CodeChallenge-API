import json
import boto3
from datetime import datetime
import pandas as pd
from io import StringIO
from sqlalchemy import create_engine
import psycopg2
import os

s3 = boto3.client('s3')

DATABASE_NAME = 'code_challenge_db'
USER = os.environ['USER']
PASSWORD = os.environ['PASSWORD']
ENDPOINT = 'code-challenge-db.c94kqyeqq7zp.us-east-2.rds.amazonaws.com'
PORT = 5432

conn_string = "postgresql://{}:{}@{}:{}/{}".format(USER, PASSWORD, ENDPOINT, PORT, DATABASE_NAME)
engine = create_engine(conn_string)

def lambda_handler(event, context):
    
    REQUEST = {
        ('GET', '/') : [build_response, [200, 'Welcome to Jhon Hader Code Challenge REST API']],
        ('GET', '/status') : [build_response, [200, "You're done! Begin to request API"]],
        ('GET', '/hired_employees') : [db_query, ["SELECT * FROM hired_employee;", True]],
        ('GET', '/departments') : [db_query, ["SELECT * FROM department;", True]],
        ('GET', '/jobs') : [db_query, ["SELECT * FROM job;", True]],
        ('POST', '/upload/hired_employee') : [post_upload, ["hired_employee", event['body']]],
        ('POST', '/upload/job') : [post_upload, ["job", event['body']]],
        ('POST', '/upload/department') : [post_upload, ["department", event['body']]]
    }       

    try:

        http_method = event.get('httpMethod')
        path = event.get('path')
        
        func, args = REQUEST[(http_method, path)]
        return func(*args)
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps('Error uploading file to S3: {}'.format(str(e)))
        }
        

def post_upload(table_name : str, event_body : str):
    try:
        # Upload the file to S3 bucket
        s3.put_object(Body=event_body, Bucket='code-challenge-jhon', Key="{}-{}.csv".format(table_name, datetime.now()))
            
        # Read as pandas DataFrame
        df = pd.read_csv(StringIO(event_body))
        
        # Insert new records into database
        insert_pandas_batch(df, table_name)
        response = build_response(200, "Data was inserted sucessfully to {} DB!".format(table_name))
    except Exception as e:
        response = build_response(500, 'Error uploading file to S3: {}'.format(str(e)))
        
    return response


def insert_pandas_batch(df : pd.DataFrame, table_name : str):
    with psycopg2.connect(
        database = DATABASE_NAME,
        user = USER,
        password = PASSWORD,
        host = ENDPOINT,
        port = PORT
    ) as conn:

        cur = conn.cursor()
        
        df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

        conn.commit()
        cur.close()
    
        
def db_query(query : str, is_select_query : bool):
    try:
        with psycopg2.connect(
            database = DATABASE_NAME,
            user = USER,
            password = PASSWORD,
            host = ENDPOINT,
            port = PORT
        ) as conn:
    
            cur = conn.cursor()
            cur.execute(query)
    
            if is_select_query:
                rows = cur.fetchall()
    
            conn.commit()
            cur.close()
    
            response = build_response(200, rows)
    except Exception as e:
        response = build_response(500, 'Error inserting records in DB: {}'.format(str(e)))
        
    return response
    
    
def build_response(status_code : int, body : str):
    return {
        'statusCode': status_code,
        'body': json.dumps(body)
    }