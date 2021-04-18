import tensorflow_text as text
import boto3
import tensorflow as tf
from fastapi import Security, Depends, FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
import re

app = FastAPI()


class Item(BaseModel):
    filename: str


# Update you credentials
ACCESS_KEY = ''
SECRET_KEY = ''
BUCKET = ""
loc = ""

s3 = boto3.client("s3", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
checkpoint = tf.saved_model.load('./albert')


@app.get("/")
def read_root(tags=["Welcome"]):
    return {"message": "Welcome from the API"}


@app.post("/SentimentAnalysis/{filename}", tags=["Sentiment Analysis"])
async def predict(filename: str):
    key = loc + filename
    try:
        file = s3.get_object(Bucket=BUCKET, Key=key)
        text = str(file['Body'].read().decode('utf-8'))
        text = text.replace('\n\n', '\n')
        # Removing the following words from file
        text = text.replace('Operator', '')
        text = text.replace('[Operator Instructions]', '')
        text = text.replace('Company Participants', '')
        text = text.replace('[ Instructions]', '')
        text = text.replace('Unidentified Analyst', '')
        text = text.replace('Company Participants', '')
        text = text.replace('Conference Call Participants', '')

        # Keeping only Alphabets, numbers and space
        text = re.sub('[^a-zA-Z0-9., \n]', '', text)

        # Splitting the line
        sentences = (text.splitlines())

        # Removing the spaces
        sentences = [x for x in sentences if x != '']
        line = []
        score = []
        for i in sentences:
            paragraph = 'b"'+i+'"'
            f = checkpoint.signatures["serving_default"]
            predict = f(tf.constant([paragraph]))
            line.append(i)
            score.append(float(predict['outputs']))
            if len(line)==15:
                break
        return {"sentence": line, "predict": score}

    except:
        raise HTTPException(status_code=404, detail="Filename not found")

if __name__ == '__main__':
    uvicorn.run(app, port=8000, host="0.0.0.0")
