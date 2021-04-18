from fastapi import APIRouter
import boto3
import json
from urllib.parse import urlparse

router = APIRouter()


@router.get("/ner")
async def nerdata(url:str):

    start = urlparse(url, allow_fragments = False)
    s3 = boto3.client('s3', aws_access_key_id="",aws_secret_access_key="",region_name='us-east-1')

    obj = s3.get_object(Bucket=start.netloc, Key=start.path.lstrip('/'))
    paragraph = str(obj['Body'].read().decode('utf-8'))

    comprehend = boto3.client("comprehend", region_name='us-east-1',aws_access_key_id="",aws_secret_access_key="")

    entities = comprehend.detect_entities(Text=paragraph, LanguageCode="en")
    keyphrase = comprehend.detect_key_phrases(Text=paragraph, LanguageCode="en")
    print(entities)
    s3 = boto3.resource('s3', aws_access_key_id="",aws_secret_access_key="",region_name='us-east-1')

    BUCKET_NAME = ""

    OUTPUT_NAME = f"dataKeyTest.json"
    OUTPUT_BODY = json.dumps(entities)
    s3.Bucket(BUCKET_NAME).put_object(Key=OUTPUT_NAME, Body=OUTPUT_BODY)
    print(entities)
    return json.dumps(entities)

