# CSYE7245 - Assignment_4: Named-Entity-Recognition Serverless Pipeline and ML-as-a-service

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)


#### Quick Links

- [CLAAT document](https://codelabs-preview.appspot.com/?file_id=1_QhZStOwgZQnpsi08ABSlJUKF0_pKWXRfX2RDbhYHcc#0)


---
## Getting Started
This project has two parts. 

Part 1: Goal of the first part of the project is to create API that Anonymizes the data through:

- Masking
- Anonymization

Then, building upon the Infrastructure for login and server less functions using Cognito and integrating the APIs so that only authenticated users can call these APIs. 

Part 2: In this part of the project, we are building upon the pre-processed (anonymized/masked data) and build a sentiment analysis model that could take the location of the anonymized file as an input and generate sentiments for each sentence.

We are using the IMDB datasets as a proxy and building a sentiment analyzer.

![image](https://user-images.githubusercontent.com/33648410/115083382-3d623100-9ed5-11eb-8a9a-f43c8efb7394.png)

## Task performed

- Task 1: Three APIs Creation
- Task 2: Model as a service for anonymized data 
  - Step 1: TensorFlow Model
  - Step 2: FastAPI to serve the model
  - Step 3: Dockerize the API service
  - Step 4: Streamlit to test the API
  - Step 5: Unit Testing and Load Testing for API

## Project Structure

![Screen Shot 2021-04-16 at 2 19 37 AM](https://user-images.githubusercontent.com/56357740/114980302-4235cf00-9e5a-11eb-8218-dfec92866434.png)

## Task 1: Three APIs
- We have created authorized apis which could be used by our users who have signed up and can get access and id tokens generated using Amazon Cognito which we are stored in dynamo db

### API 1: Access
This API should retrieve the EDGAR filings data from the S3 bucket

### API 2: Named entity recognition
This API should take a link to a file on S3 and
- Call Amazon Comprehend to find entities.
- Store these on S3
  
### API 3: Implement masking, and anonymization functions.
We define the API in a way that indicate which entities need to be masked, which needs to be anonymized. We are getting the location of the file/files as input and output the files back to S3.

## Task 2: Model as a service for anonymized data 
To deploy a sentiment analysis model or to create a Model-as-a-service for anonymized data
### Step 1:Train TensorFlow models using TensorFlow Extended(TFX)
Replicated the architecture to train the model for the anonymized data using ALBERT and this architecture that leveragesTensorFlow Hub,TensorflowTransform,TensorFlow Data Validation and Tensorflow Text and Tensorflow Serving.

![Screen Shot 2021-04-15 at 6 54 28 PM](https://user-images.githubusercontent.com/56357740/114947955-0da32280-9e1c-11eb-89ee-8d75368c6c4e.png)

The pipeline takes advantage of the broad TensorFlowEcosystem, including:
- Loading the IMDB dataset via TensorFlow Datasets
- Loading a pre-trained model via tf.hub
- Manipulating the raw input data with tf.text
- Building a simple model architecture with Keras
- Composing the model pipeline with TensorFlow Extended,e.g. TensorFlowTransform, TensorFlow Data Validation and then consumingthe tf.Kerasmodel with the latest Trainer component from TFX

### Step 2: FastAPI to serve the model
#### setup:
Install FastAPI framework, high performance, easy to learn, fast to code, ready for production

`
pip install fastapi
`
Install the lightning-fast ASGI server Uvicorn
`
pip install uvicorn
`

API:
We have a POST method where we give the URL of the S3 file and get the predicts using Albert model

### Step 3: Dockerize the API service

### Prerequisites
Your development and production environments are constructed by Docker. Install Docker for Desktop for your OS.
To verify that Docker is installed, run `docker --version`.

### Simple Case: One Container
In this directory, we have `Dockerfile`, a blueprint for our development environment, and `requirements.txt` that lists the python dependencies.

We made use of the following command to create our docker image:

```
# Tensforlow 2 official image with Python 3.6 as base
FROM tensorflow/tensorflow:2.0.0-py3

# Make working directories
RUN  mkdir -p /home/project-api
WORKDIR /home/project-api/

# Upgrade pip with no cache
RUN pip install --no-cache-dir -U pip

# Copy application requirements file to the created working directory
COPY requirements.txt .

# Install application dependencies from the requirements file
RUN pip install -r requirements.txt

# Copy every file in the source folder to the created working directory
COPY  . .

# Run the python application
CMD ["python", "main.py"]
```
#### Build:
##### Local
To serve the provided pre-trained model, follow these steps:
1. `git clone` this repo
2. `cd Assignment_4/app/`
3. `docker build -t nidhi2019/edgar-sentiment-analyzer-api:latest .`

##### Dockerhub
`docker pull nidhi2019/edgar-sentiment-analyzer-api`

#### Run
`docker run -it --rm -p 8000:8000 nidhi2019/edgar-sentiment-analyzer-api`

If everything worked properly, you should now have a container running at server `http://0.0.0.0:8000/`

### Step 4: Streamlit App
#### Setup:
`
pip install fastapi
`
To run the application, run 
`
streamlit run app.py
`

Application:

If we give the s3 link of the anonymised file, we should be able to see the prediction score of the transcript

### Step 5: Test API
#### Test Unit Cases
#### Setup: 
Install PyTest by running this:
```
 % pip install pytest
```
#### Using TestClient

Import ```TestClient```
Create a ```TestClient``` passing to it your ```FastAPI```.

Create functions with a name that starts with ```test.``` (this is standard pytest conventions).

Use the ```TestClient``` object the same way as you do with requests.

Write simple assert statements with the standard Python expressions that you need to check (again, standard pytest).
###### Run the command to test all use cases in test_main.py,
```
pytest or pytest -v
```
#### Locust Load Test
##### Setup:
1.Install the libraries
```
pip install locustio==0.14.6
pip install greenlet==0.4.16
```
##### Processs

1. Make a .py file similar to locust_load_test.py to test the load test 

2. To run the file 
```
locust -f query_locust.py
```
3. Open the browser and enter the following url
```
http://localhost:8089/
```
4. Fill up the Number of users to simulate, Hatch rate, Host and click Start swarming 

## Team Members:

- Nidhi Goyal
- Kanika Damodarsingh Negi
- Rishvita Reddy Bhumireddy

## Citation:
- https://aws.amazon.com/blogs/machine-learning/identifying-and-working-with-sensitive-healthcare-data-with-amazon-comprehend-medical/
- https://aws.amazon.com/blogs/machine-learning/detecting-and-redacting-pii-using-amazon-comprehend/
- https://docs.aws.amazon.com/apigateway/latest/developerguide/integrating-api-with-aws-services-s3.html
- https://testdriven.io/blog/fastapi-streamlit/
- https://github.com/google-research/albert
- https://github.com/google-research/ALBERT/blob/master/run_classifier.py
