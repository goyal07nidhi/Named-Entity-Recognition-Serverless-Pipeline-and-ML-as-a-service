import streamlit as st
import requests
import pandas as pd


def main():
    headers = {'authorization': ''}
    st.header("SENTIMENT ANALYSIS")
    st.image('./download.png')
    selection = st.selectbox('Select',('Access API', 'NER API', 'Anonymised and Masked API', 'Prediction'))
    if selection == 'Access API':
        filename = st.text_input("Enter the link")
        if st.button("Get API"):
            response = requests.get(filename,headers=headers)
            st.write(response.json())
    if selection == 'NER API':
        filename = st.text_input("Enter the link")
        if st.button("Get API"):
            response = requests.get(filename,headers=headers)
            st.write(response.json())
    if selection == 'Anonymised and Masked API':
        filename = st.text_input("Enter the link")
        if st.button("Get API"):
            response = requests.get(filename,headers=headers)
            st.write(response.json())

    if selection == 'Prediction':
        file = st.text_input("Enter the link")
        names = file.split("/")
        filename = names[len(names)-1]
        print(filename)
        if st.button("Predict"):
            response = requests.post(f"http://127.0.0.1:8001/SentimentAnalysis/{filename}")
            output = response.json()
            print(output)

            sentence = []
            predict = []
            for i in output['sentence']:
                sentence.append(i)
            for j in output['predict']:
                predict.append(j)
            #sentence.append(output['sentence'])
            #predict.append(output['predict'])
            df = pd.DataFrame()
            df['Sentence'] = sentence
            df['Score'] = predict
            st.table(df)


if __name__ == "__main__":
    main()
