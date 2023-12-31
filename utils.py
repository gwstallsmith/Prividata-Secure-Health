from flask import Flask, render_template, request, make_response, redirect, url_for
import sqlite3
import random
import math
from crypto import *

app = Flask(__name__)


import random

# Lists of random data for generating tuples
first_names = ["Alice", "Bob", "Charlie", "David", "Emma", "Frank", "Grace", "Henry", "Ivy", "Jack", "Aarav", "Mei", "Sofia", "Malik", "Yuki", "Isabella","Lars","Emeka","Ainhoa","Hugo","Leila","Mateo","Freya","Amir","Zara","Elena","Thiago","Ananya","Khaled","Sienna","Taika","Ravi","Ingrid","Hiroshi","Laila","Nikolai","Elin","Aarushi","Rafael","Aoife","Dante","Amara","Ying","Larsa","Kiana","Ludmila","Karan","Isolde","Aisha","Akio","Malina","Cosima","Jovan","Anouk","Niamh","Bodhi","Esmeralda","Tariq", "Luka", "Anya"]
last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Smith","Johnson","Williams","Jones","Brown","Davis","Miller","Wilson","Moore","Taylor","Anderson","Thomas","Jackson","White","Harris","Martin","Thompson","Garcia","Martinez","Robinson","Clark","Rodriguez","Lewis","Lee","Walker","Hall","Allen","Young","Hernandez","King","Wright","Lopez","Hill","Scott","Green","Adams","Baker","Gonzalez","Nelson","Carter","Mitchell","Perez","Roberts","Turner","Phillips","Campbell","Parker","Evans","Edwards","Collins","Stewart","Sanchez","Morris","Rogers","Reed","Cook","Morgan","Bell","Murphy","Bailey","Rivera","Cooper","Richardson","Cox","Howard","Ward","Torres","Peterson","Gray","Ramirez",]
genders = ["Male", "Female"]
health_history = ["No significant health issues.","Has a history of allergies but otherwise healthy.","Regularly exercises and maintains good health.","Underwent surgery last year but recovered well.","Currently undergoing treatment for a minor condition.","Maintains excellent health through a routine of yoga and meditation.","Recovering from a recent injury sustained during a sports event.","Struggles with occasional allergies but maintains an active lifestyle.","Underwent successful surgery last year and has fully recovered.","Regularly visits the gym and follows a balanced diet for optimal health.","Manages stress effectively through regular exercise and mindfulness.","Dealing with a chronic condition but manages it well with medication.","Recently started a fitness regimen to improve overall well-being.","Maintains a healthy weight through mindful eating and regular walks.","Has a history of asthma but manages it with prescribed treatments.","Currently undergoing physical therapy after a minor accident.","Experiences occasional back pain but manages it with exercises.","Recovered from a bout of flu and focuses on boosting immunity.","Participates in marathons to maintain physical and mental fitness.","Recovered from a major surgery and is steadily regaining strength.","Practices healthy habits to keep cholesterol and blood pressure in check.","Dealing with a recent diagnosis and adjusting to a new treatment plan.","Follows a strict diet and exercise routine for weight management.","Recently adopted a healthier lifestyle to improve overall health.","Manages a chronic condition with a balance of medication and diet.","Struggling with chronic back pain due to a herniated disc.","Facing ongoing challenges with rheumatoid arthritis.","Enduring the effects of a recent stroke and undergoing rehabilitation.","Coping with the debilitating symptoms of fibromyalgia.","Managing a severe case of Crohn's disease with medication and dietary restrictions.","Dealing with the complications of Type 1 diabetes.","Struggling with the effects of chronic obstructive pulmonary disease (COPD).","Undergoing chemotherapy for an aggressive form of cancer.","Living with the challenges of multiple sclerosis (MS) on a daily basis.","Recovering from a major heart attack and adapting to a new lifestyle.","Enduring the difficulties of severe depression and seeking ongoing treatment.","Facing challenges of bipolar disorder and working on finding stability.","Living with the impact of a traumatic brain injury.","Managing the effects of severe asthma attacks.","Dealing with chronic kidney disease and undergoing dialysis regularly.","Struggling with the limitations of Parkinson's disease.","Recovering from a serious car accident and multiple surgeries.","Living with the effects of a spinal cord injury.","Enduring the challenges of severe chronic migraines.","Coping with the debilitating effects of severe anxiety disorder."]


def delete_all():
    with sqlite3.connect("db.sqlite3") as connection:
        cursor = connection.cursor()

        cursor.execute('DELETE FROM PatientInformation')
        cursor.execute('DROP TABLE IF EXISTS PatientInformation')
        cursor.execute('CREATE TABLE IF NOT EXISTS PatientInformation (ID INTEGER PRIMARY KEY, First_Name TEXT, Last_Name TEXT, Gender TEXT, Age INTEGER, Weight INTEGER, Height INTEGER, Health_History TEXT, MAC TEXT)')
        
        cursor.execute('DELETE FROM Credentials')
        cursor.execute('DROP TABLE IF EXISTS Credentials')
        cursor.execute('CREATE TABLE IF NOT EXISTS Credentials (ID INTEGER PRIMARY KEY, Username TEXT, Password TEXT, IsAdmin INTEGER, FOREIGN KEY (ID) REFERENCES PatientInformation(ID))')


        generate_shared_secret("adpass")
        history = "Living an alternative lifestyle with Golem."


        cursor.execute("INSERT INTO Credentials (ID, Username, Password, IsAdmin) VALUES (?, ?, ?, ?)", (1, "admin", hash_password("adpass"), 2))
        cursor.execute("INSERT INTO PatientInformation (ID, First_Name, Last_Name, Gender, Age, Weight, Height, Health_History, MAC) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (1, encrypt("Bilbo"), encrypt("Baggins"), encrypt("Male"), 50, 30, 120, encrypt(history), encrypt(generate_mac(history))))


        generate_shared_secret("adfail")
        history = "Died of cringe."

        cursor.execute("INSERT INTO Credentials (ID, Username, Password, IsAdmin) VALUES (?, ?, ?, ?)", (2, "notadmin", hash_password("adfail"), 1))
        cursor.execute("INSERT INTO PatientInformation (ID, First_Name, Last_Name, Gender, Age, Weight, Height, Health_History, MAC) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (2, encrypt("Frodo"), encrypt("Baggins"), encrypt("Male"), 50, 30, 120, encrypt(history), encrypt(generate_mac(history))))

    return

@app.route('/more', methods=['GET', 'POST'])
def generate_more_users():
    delete_all()

    with sqlite3.connect("db.sqlite3") as connection:
        cursor = connection.cursor()

        for _ in range(100):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            gender = random.choice(genders)


            age = random.randint(4, 16) * 5
            weight = random.randint(2, 10) * 10
            height = random.randint(15, 20) * 10


            history = random.choice(health_history)

            generate_shared_secret(first_name + last_name)

            cursor.execute("SELECT MAX(ID) FROM Credentials")
            new_ID = cursor.fetchone()[0] + 1
            
            cursor.execute("INSERT INTO Credentials (ID, Username, Password, IsAdmin) VALUES (?, ?, ?, ?)", (new_ID, first_name + last_name + str(new_ID), hash_password(first_name + last_name), 0))
            cursor.execute("INSERT INTO PatientInformation (ID, First_Name, Last_Name, Gender, Age, Weight, Height, Health_History, MAC) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (new_ID, encrypt(first_name), encrypt(last_name), encrypt(gender), age, weight, height, encrypt(history), encrypt(generate_mac(history))))


def remove_user(id):
    with sqlite3.connect("db.sqlite3") as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Credentials WHERE ID = ?", (id,))


def remove_history(id):
    with sqlite3.connect("db.sqlite3") as connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE PatientInformation SET Health_History = NULL WHERE ID = ?", (id,))

def round_down_ten(hw):
    return math.floor(hw / 10) * 10
