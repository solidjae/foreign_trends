from serpapi import GoogleSearch
from deep_translator import GoogleTranslator
import pandas as pd
import json


def plugin_params(country):

    translator = GoogleTranslator(from_lang="en", to_lang=country)

    keywords = ["desk", "Chair", "table", 'hanger', 'shelf']

    key_list = []

    for k in keywords:

        key_list.append(translator.translate(k))

    print(",".join(key_list))

    params = {

        "engine": "google_trends",
        "q": ",".join(key_list),
        "geo": "JP",
        "data_type": "TIMESERIES",
        "cat": "18",
        "date": "today 12-m",
        "api_key": "84b61d90d93854b23dd71ce39a74ec6b1a312e67820c8bf9cc6e8f38b96a282e",
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    with open('data.json', "w") as file:
        json.dump(results, file, indent=4)


    print(results)

    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    translator = GoogleTranslator(to_lang="en")
    # Extract the relevant data
    interest_data = data['interest_over_time']['timeline_data']

    # Convert data to DataFrame
    frames = []  # List to hold DataFrames for each entry

    for entry in interest_data:
        date = entry['date']
        values = {item['query']: item['value'] for item in entry['values']}
        values['Date'] = date
        frame = pd.DataFrame([values])  # Convert dict to DataFrame
        frames.append(frame)

    # Concatenate all DataFrames and set date as index
    structured_df = pd.concat(frames).set_index('Date')
    structured_df.columns = [translator.translate(col) for col in structured_df.columns]
    print(structured_df)


plugin_params('ja')