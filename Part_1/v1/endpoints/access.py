from fastapi import APIRouter
import boto3
from urllib.parse import urlparse

router = APIRouter()


@router.get("/access")
async def getdata(url:str):

    start = urlparse(url, allow_fragments = False)
    s3 = boto3.client('s3', aws_access_key_id="",
                      aws_secret_access_key="",
                      region_name='us-east-1')
    obj = s3.get_object(Bucket=start.netloc, Key=start.path.lstrip('/'))
    body = obj['Body']
    return body.read()
