import random

ages = [i for i in range(20, 66)]
races = ["Caucasion", "African American", "Hispanic", "East Asian", "South Asian", "Middle Eastern", "Other"]
genders = ['Male', 'Female']
backgrounds = ['Business/Finance', 'Software', 'Healthcare Provider', 'Designer (Product, Graphic, etc.)', 
    'Engineering (Mechanical, Electrical, etc.)', 'Data Science', 'Scientist', 'Media', 'Law/Policy'
]

def generate_person():
    return {
        'Age': random.choice(ages),
        'Race': random.choice(races),
        'Gender': random.choice(genders),
        'Background': random.choice(backgrounds)
    }

def generate_team(size):
    team = [generate_person() for _ in range(size)]

    # Sort by age
    team.sort(key=lambda person: person['Age'])
    return team 
