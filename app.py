#!/usr/bin/env python
# coding: utf-8


## Import Libraries

import streamlit as st
import urllib.request
import csv
import io
import json


# título
st.title("Diabetes Mellitus Diagnosis Analysis") 
# subtítulo
st.markdown("This is a Web App used to predict the chance of a positive diagnosis of diabetes. The app is based in a a model trained through Azure Machine Learning Studio https://studio.azureml.net")
# subtítulo
st.markdown("This app was developed by Wladimir B. G. de Araújo Neto (dev.wlad@gmail.com) and Patrick T. Pinto (patrick.tapajos@gmail.com)")


data_csv = st.text_input("Patient data", key="data_csv", value="")
reader = csv.DictReader(io.StringIO(data_csv))
json_data = json.dumps(list(reader))
json_data


# inserindo um botão na tela
btn_predict = st.button("Start Prediction")

if btn_predict:
    data = {
        "Inputs": {
            "input1":json_data,
        },
    "GlobalParameters": {
    }
}

    body = str.encode(json.dumps(data))

    url = 'https://ussouthcentral.services.azureml.net/workspaces/62be23b8fa1d4188bd6401cdb4527b4d/services/90b9756deb424549ac98867017467ee2/execute?api-version=2.0&format=swagger'
    api_key = '/zIK5JjZudsy8UAIfeqN+FBF2CLMnYcebLd4P1DuP0Rrtpm49BCW+sZseEcpyGvqwRfiGqHWXRi5/0bDDqdSjg==' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        
        parsed_json = (json.loads(result))
        y = json.loads(json.dumps(parsed_json, indent=4, sort_keys=True))
        x = y['Results']
        z = x['output1']
        m = z[0]
        #print(m['Scored Labels'])
 
        if m['Scored Labels'] == '1':
            st.markdown("The data shows that the patient have a positive diagnosis for Diabetes")
        else:
            st.markdown("The data shows that the patient have a negative diagnosis for Diabetes")
            

    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))