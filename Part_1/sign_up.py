import boto3
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import time

ACCESS_KEY = ''
SECRET_KEY = ''
BUCKET = ""
REGION_NAME = 'us-east-2'

username = ''
password = ''

USER_POOL_ID = ''
CLIENT_ID = ''

client = boto3.client('cognito-idp', region_name=REGION_NAME, aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
dynamodb_client = boto3.client('dynamodb', region_name = REGION_NAME, aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
sign = False
message = ''


def signup_user(username, password):

    sign = False
    resp = client.sign_up(
        ClientId=CLIENT_ID,
        Username=username,
        Password=password
        )
    response = client.admin_confirm_sign_up(
        UserPoolId=USER_POOL_ID,
        Username=username
    )
    sign = True
    message = 'You have been successfully signed up'
    print(message)

    return message, sign


def initiate_authorize_user(username, password):
    cognito_resp = client.admin_initiate_auth(
        UserPoolId=USER_POOL_ID,
        ClientId=CLIENT_ID,
        AuthFlow='ADMIN_NO_SRP_AUTH',
        AuthParameters={
            "USERNAME": username,
            "PASSWORD": password
        }
    )

    AccessToken = str(cognito_resp['AuthenticationResult']['AccessToken'])
    print("This is access token {}".format(AccessToken))
    RefreshToken = str(cognito_resp['AuthenticationResult']['RefreshToken'])
    IdToken = str(cognito_resp['AuthenticationResult']['IdToken'])
    expiration = cognito_resp['AuthenticationResult']['ExpiresIn']

    expire_time = datetime.now() + timedelta(seconds=expiration)
    expire_time = expire_time.strftime("%Y-%m-%d %H:%M:%S")
    print(expire_time)

    add_to_db = dynamodb_client.put_item(
        TableName='UserToken', Item={

            'CurrentUser': {'S': str(username)},
            'IdToken': {'S': IdToken},
            'RefreshToken': {'S': RefreshToken},
            'AccessToken': {'S': AccessToken},
            'TokenTime': {'S': expire_time}
        })
    if cognito_resp['AuthenticationResult']['AccessToken']:
        if cognito_resp['ResponseMetadata']['HTTPStatusCode'] == 200:
            authorized = True
            return authorized, username, IdToken


signup_user('test1@gmail.com', 'Neu1#2021')
a, b, c = initiate_authorize_user('test1@gmail.com', 'Neu1#2021')
print(a)
print(b)
print(c)


