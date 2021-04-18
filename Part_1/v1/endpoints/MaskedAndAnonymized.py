from fastapi import APIRouter
import boto3
import json
import hashlib
import uuid
import os
import logging
from urllib.parse import urlparse

router=APIRouter()

ACCESS_KEY = ''
SECRET_KEY = ''
BUCKET = " "
REGION_NAME = 'us-east-2'

ddb = boto3.client('dynamodb', region_name=REGION_NAME, aws_access_key_id=ACCESS_KEY,
                   aws_secret_access_key=SECRET_KEY)

comprehend = boto3.client(service_name='comprehend', region_name=REGION_NAME, aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_KEY)

client = boto3.client(service_name='comprehendmedical', region_name=REGION_NAME, aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

s3 = boto3.resource(service_name='s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
os.environ["EntityMap"] = 'Anonymized'


def extract_entities_from_message(message):
    return client.detect_phi(Text=message)


def mask(i, entity_list, Mask_Entity):
    masked_message = mask_entities_in_message(i, entity_list, Mask_Entity)
    return masked_message


def mask_entities_in_message(message, entity_list, Mask_Entity):
    for entity in entity_list:
        check = any(item in entity['Type'] for item in Mask_Entity)
        if check is True:
            # if (entity['Type'] == Mask_Entity):
            message = message.replace(entity['Text'], '#' * len(entity['Text']))
    return message


def anonamizing(message, entity_list, deidentify_Ent):
    try:
        deidentified_message, entity_map = deidentify_entities_in_message(message, entity_list, deidentify_Ent)
        hashed_message = store_deidentified_message(deidentified_message, entity_map, os.environ['EntityMap'])
        return {
            "deid_message": deidentified_message,
            "hashed_message": hashed_message
        }
    except Exception as e:
        logging.error('Exception: %s. Unable to extract entities from message' % e)
        raise e


def deidentify_entities_in_message(message, entity_list, deidentify_Ent):
    entity_map = dict()
    for entity in entity_list:
        check = any(item in entity['Type'] for item in deidentify_Ent)
        if check is True:
            salted_entity = entity['Text'] + str(uuid.uuid4())
            hashkey = hashlib.sha3_256(salted_entity.encode()).hexdigest()
            entity_map[hashkey] = entity['Text']
            message = message.replace(entity['Text'], hashkey)
    return message, entity_map


def store_deidentified_message(message, entity_map, ddb_table):
    hashed_message = hashlib.sha3_256(message.encode()).hexdigest()
    for entity_hash in entity_map:
        ddb.put_item(
            TableName=ddb_table,
            Item={
                'MessageHash': {
                    'S': hashed_message
                },
                'EntityHash': {
                    'S': entity_hash
                },
                'Entity': {
                    'S': entity_map[entity_hash]
                }
            }
        )
    return hashed_message


@router.get("/maskedandanonymized")
async def ananomize(s3_path: str, Mask_Entity: str, deidentify_Ent: str):
    s3 = boto3.resource(
        service_name='s3',
        region_name='us-east-2', aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY)
    if s3_path.startswith('s3'):
        s3_path = s3_path[5:]
    s3_path = s3_path.split('/')
    bucket = s3_path[0]
    filename = s3_path[2]
    s3_key = ""
    if len(s3_path) > 1:
        s3_key = '/'.join(s3_path[1:])

    obj = s3.Object(bucket, s3_key)
    body = obj.get()['Body'].read().decode('utf8')
    masked = []

    Mask_Entity = Mask_Entity.split(',')
    deidentify_Ent = deidentify_Ent.split(',')

    entities_response = extract_entities_from_message(body)
    entity_list = entities_response['Entities']
    masked.append(mask(body, entity_list, Mask_Entity))
    for message in masked:
        masked_entities_response = extract_entities_from_message(message)
        masked_entity_list = masked_entities_response['Entities']
        x = anonamizing(message, masked_entity_list, deidentify_Ent)
        deidentifiedmessage = (x['deid_message'])
    print(deidentifiedmessage)
    BUCKET_NAME = " "
    OUTPUT_BODY = deidentifiedmessage
    s3.Bucket(BUCKET_NAME).put_object(Key=f'maskoutput/anaonamized.txt', Body=OUTPUT_BODY)
    return {
        'body': json.dumps(deidentifiedmessage)
    }