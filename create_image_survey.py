import requests
from generate_team import *
from generate_image import *

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

# Function that creates two teams
def make_tables(size):
    table_list = []
    for _ in range(size):
        table = {
            'teamA': generate_team(5),
            'teamB': generate_team(5)
        }
        table_list.append(table)
    return table_list

def upload_image(file_path, prompt):
    generate_image(prompt, 'generated-image.jpg')
    cloud_name = "dmmulnblq"
    pi_key = "945771813558264"
    api_secret = "DgAx26TNCnM_qGeI4KapjaC55r8"

    # Cloudinary API endpoint
    url = f"https://api.cloudinary.com/v1_1/{cloud_name}/image/upload"

    # Upload settings
    data = {
        "upload_preset": "d2evzunt"  # Set this in Cloudinary Dashboard (Media Library > Upload Settings)
    }

    # Open the file and upload it
    with open(file_path, "rb") as image_file:
        response = requests.post(url, data=data, files={"file": image_file})

    # Parse and print the image URL
    if response.status_code == 200:
        image_url = response.json()["secure_url"]
        print('success')
        return image_url
    else:
        print("❌ Upload failed!", response.text)

# New function to create HTML containing 5 images
def generate_images_html(team_data, title):
    """
    This function generates HTML for a team of 5 images.
    Currently uses placeholder image references; you can replace these
    with actual image URLs as needed.
    """
    images_html = ""
    for i, member in enumerate(team_data, 1):
        # In a real scenario, you might map each member's attributes (Age, Gender, etc.)
        # to a specific image. For now, we'll use placeholder URLs.
        prompt = f"An image of a {member['Age']} year old {member['Race']} {member['Gender']} with a business background, wearing formal attire, in a modern office setting, realistic"
        images_html += f"""
            <div style="text-align: center;">
                <img src={upload_image('generated-image.jpg', prompt)} alt="Person {i}" style="display: block; margin: 0 auto; width: 150px; height: 150px;">
                <p>{member['Background']}</p>
            </div>
        """

    return f"""
    <div style="margin-right: 20px;">
        <h3>{title}</h3>
        <div style="display: flex; gap: 10px;">
            {images_html}
        </div>
    </div>
    """

for i, variation in enumerate(make_tables(10), start=1):
    # Build the question text with two groups of 5 images
    question_text = f"""
    <p>Question {i}: Please review the two teams below and choose which is more diverse:</p>
    <div style="display: flex; justify-content: space-around;">
        {generate_images_html(variation['teamA'], 'Team A')}
        {generate_images_html(variation['teamB'], 'Team B')}
    </div>
    """

    # Construct the payload to create a multiple-choice question
    payload = {
        "QuestionText": question_text,
        "QuestionType": "MC",
        "Selector": "SAVR",
        "SubSelector": "TX",
        "Choices": {
            "1": {"Display": "Team A"},
            "2": {"Display": "Team B"}
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
        "QuestionDescription": "Choose the more diverse team",
        "Validation": {
            "Settings": {
                "ForceResponse": "ON",
                "ForceResponseType": "ON"
            }
        }
    }

    # Add the new question to the Qualtrics survey
    url = f"{BASE_URL}/survey-definitions/{SURVEY_ID}/questions"
    print(f"POST to: {url}")

    response = requests.post(url, headers=headers, json=payload)
    print(f"Created Question {i}: Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    print("-" * 50)