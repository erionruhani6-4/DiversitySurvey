import requests
from generate_team import *

# Counts times script has been run
# Used to create unique survey names
try:
    with open('counter.txt', 'r') as f:
        count = int(f.read())
except FileNotFoundError:
    count = 0

with open('counter.txt', 'w') as f:
    f.write(str(count + 1))

API_TOKEN = 'myhJ4dGBGOJMoWNP5dSRibf7Jbep70cCxn7E8m8M'
BASE_URL = 'https://iad1.qualtrics.com/API/v3'

headers_s = {
    'Content-Type': 'application/json',
    'X-API-TOKEN': API_TOKEN,
    'Accept': 'application/json'
}

payload_s = {
    "SurveyName": f"Diversity Survey {count}",
    "Language": "EN",
    "ProjectCategory": "CORE"
}

response = requests.post(f"{BASE_URL}/survey-definitions", headers=headers_s, json=payload_s)
survey_id = response.json()['result']['SurveyID']

SURVEY_ID = survey_id

headers = {
    'Content-Type': 'application/json',
    'X-API-TOKEN': API_TOKEN,
    'Accept': 'application/json'
}

# Table content variations

def make_tables(size):
    table_list = []
    for _ in range(size):
        table = {
            'tableA': generate_team(5),
            'tableB': generate_team(5)
        }
        table_list.append(table)
    return table_list


# Function to create table HTML
def generate_table_html(table_data, title):
    rows = "".join(
        f"<tr><td>{row['Age']}</td><td>{row['Race']}</td><td>{row['Gender']}</td><td>{row['Background']}</td></tr>" 
        for row in table_data
    )
    return f"""
    <table border='1' style='border-collapse: collapse; margin-right: 20px;'>
        <thead>
            <tr><th colspan='2'>{title}</th></tr>
            <tr><th>Age</th><th>Race</th><th>Gender</th><th>Professional Background</th></tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
    """

for i, variation in enumerate(make_tables(10), start=1):
    # Build the question text with two HTML tables
    question_text = f"""
    <p>Question {i}: Please review the two teams below and choose which is more diverse:</p>
    <div style="display: flex; justify-content: space-around;">
        {generate_table_html(variation['tableA'], 'Team A')}
        {generate_table_html(variation['tableB'], 'Team B')}
    </div>
    """

    # The new survey-definitions API requires a "questionDefinition" object
    payload = {
        "QuestionText": question_text,
        "QuestionType": "MC",
        "Selector": "SAVR",
        "SubSelector": "TX",
        "Choices": {
            "1": {
                "Display": "Table A"
            },
            "2": {
                "Display": "Table B"
            }
        },
        "ChoiceOrder": ["1", "2"],
        "Configuration": {
            "QuestionDescriptionOption": "UseText",
            "TextPosition": "inline",
            "ChoiceColumnWidth": 100,
            "RepeatHeaders": "none",
            "WhiteSpace": "ON",
            "LabelPosition": "BELOW",
            "NumColumns": 2,
            "MobileFirst": False
        },
        "Language": [],
        'QuestionDescription': 'Choose the more diverse team',
        "Validation": {
            "Settings": {
                "ForceResponse": "ON",
                "ForceResponseType": "ON"
            }
        }
    }

    # Important: Use the survey-definitions endpoint
    url = f"{BASE_URL}/survey-definitions/{SURVEY_ID}/questions"
    print(f"POST to: {url}")

    response = requests.post(url, headers=headers, json=payload)
    print(f"Created Question {i}: Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    print("-" * 50)

