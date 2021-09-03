#!/usr/bin/env python
# coding: utf-8


# Import Libraries

from os import replace
import streamlit as st
import urllib.request
import pandas as pd
import json


# título
st.title("Diabetes Mellitus Diagnosis Analysis")
# subtítulo
st.markdown("This is a Web App used to predict the chance of a positive diagnosis of diabetes. The app is based in a a model trained through Azure Machine Learning Studio https://studio.azureml.net")
# subtítulo
st.markdown("This app was developed by Wladimir B. G. de Araújo Neto (dev.wlad@gmail.com) and Patrick T. Pinto (patrick.tapajos@gmail.com)")

uploaded_file = st.file_uploader('Choose your .csv file', type="csv")
df_dict = ""
if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)
    df["diabetes_mellitus"] = None
    st.write(df)
    df_dict = df.to_dict(orient="records")
# inserindo um botão na tela
btn_predict = st.button("Start Prediction")

if btn_predict:
    data = {
        "Inputs": {
            "input1": [df_dict[0]],
        },
        "GlobalParameters": {
        }
    }

    body = str.encode(json.dumps(data).replace('NaN','null'))

    url = 'https://ussouthcentral.services.azureml.net/workspaces/62be23b8fa1d4188bd6401cdb4527b4d/services/90b9756deb424549ac98867017467ee2/execute?api-version=2.0&format=swagger'
    api_key = '/zIK5JjZudsy8UAIfeqN+FBF2CLMnYcebLd4P1DuP0Rrtpm49BCW+sZseEcpyGvqwRfiGqHWXRi5/0bDDqdSjg=='
    headers = {'Content-Type': 'application/json',
               'Authorization': ('Bearer ' + api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        parsed_json = (json.loads(result))
        y = json.loads(json.dumps(parsed_json, indent=4, sort_keys=True))
        m = y['Results']['output1'][0]
        if m['Scored Labels'] and m['Scored Probabilities']:
            if m['Scored Labels'] == '1':
                st.markdown(
                    "The data shows that the patient have a positive diagnosis for Diabetes ({:.2f})".format(float(m['Scored Probabilities'])))
            else:
                st.markdown(
                    "The data shows that the patient have a negative diagnosis for Diabetes ({:.2f})".format(float(m['Scored Probabilities'])))
        else:
            st.write("No response received from server")

    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))
