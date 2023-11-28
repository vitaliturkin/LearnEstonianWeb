from flask import Flask, render_template, request, redirect, url_for, g, session, flash
import sqlite3
import secrets
import string
app = Flask(__name__)

def generate_secret_key(length=24):
    characters = string.ascii_letters + string.digits + string.punctuation
    secret_key = ''.join(secrets.choice(characters) for _ in range(length))
    return secret_key

# Generate a random secret key
generated_key = generate_secret_key()
print("Randomly generated secret key:", generated_key)

app.secret_key = generated_key
db_location = 'users.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_location)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        db.close()  # Close the database connection after initialization

# Initialize the database
init_db()

# Homepage 
@app.route('/')
def home():
    return render_template('home.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        if user:
            session['user_id'] = user[0]
            return redirect(url_for('path'))

        flash("Invalid username or password. Please try again.", "error")

    return render_template('login.html')


# Choose path page after successful login

@app.route('/path')
def path():
    return render_template('path.html')

# Signup route

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            db.commit()
            return redirect(url_for('login'))  # Redirect to login after successful signup
        except sqlite3.IntegrityError:
            # IntegrityError means the username might already exist
            flash("Username already exists. Try a different username.", "error")
            return redirect(url_for('signup'))  # Redirect back to signup page
        finally:
            db.close()

    return render_template('signup.html')


@app.route('/guest', methods=['POST'])
def guest():
    # Guest mode functionality
    return redirect(url_for('path'))  # Redirect to the path page in guest mode

# Define routes for language levels

@app.route('/beginner')
def beginner():
    return render_template('beginner.html')

@app.route('/intermediate')
def intermediate():
    return render_template('intermediate.html')

@app.route('/advanced')
def advanced():
    return render_template('advanced.html')

# Define route for quiz level

@app.route("/quiz/", methods=['GET', 'POST'])
def quiz():
    easy_questions = {
        "1": {"text": "What is 'hello' in Estonian?", "correct_answer": 0, "answers": ["Tere", "Hei", "Tervist", "Tere hommikust"]},
        "2": {"text": "What is 'thank you' in Estonian?", "correct_answer": 2, "answers": ["Palun", "Jah", "Aitäh", "Head aega"]}
    }

    moderate_questions = {
        "3": {"text": "What is 'good morning' in Estonian?", "correct_answer": 2, "answers": ["Tere päevast", "Head õhtut", "Tere hommikust", "Tere"]},
        "4": {"text": "What is 'water' in Estonian?", "correct_answer": 0, "answers": ["Vesi", "Õlu", "Kohv", "Piim"]}
    }

    hard_questions = {
        "5": {"text": "What is 'please' in Estonian?", "correct_answer": 0, "answers": ["Palun", "Vabandage", "Aitäh", "Tere"]},
        "6": {"text": "What is 'beautiful' in Estonian?", "correct_answer": 2, "answers": ["Kiire", "Tubli", "Kaunis", "Kurb"]}
    }

    qa = {**easy_questions, **moderate_questions, **hard_questions}

    if request.method == 'POST':
        score = 0  
        for i in range(1, 7):  
            given_answer = request.form.get(f'question_{i}')  
            correct_answer = qa[str(i)]['correct_answer']
            
            if given_answer is not None:  
                if int(given_answer) == correct_answer:
                    score += 1  

        session['score'] = score  

        score = session.get('score', 0)
        level = None
        if 0 <= score <= 1:
            level = "beginner"
        elif 2 <= score <= 3:
            level = "intermediate"
        elif 4 <= score <= 6:
            level = "advanced"

        return render_template('result.html', score=score, level=level)
    
    # Pre-calculate enumerations for answers
    enumerated_qa = {
        q_num: {
            'text': question['text'],
            'enumerated_answers': list(enumerate(question['answers'])),
            'correct_answer_index': question['correct_answer']  # Include correct answer index
        } for q_num, question in qa.items()
    }

    return render_template('quiz.html', qa=enumerated_qa)

@app.route('/result')
def result():
    return render_template('result.html')

# Define routes for flashcard pages for each theme 

@app.route('/months')
def months():
    flashcard_images = [
        {"image_path": url_for('static', filename='images/flashcards/months/April.jpg'), "word": "April"},
        {"image_path": url_for('static', filename='images/flashcards/months/May.jpg'), "word": "May"},
        {"image_path": url_for('static', filename='images/flashcards/months/June.jpg'), "word": "June"},
        {"image_path": url_for('static', filename='images/flashcards/months/July.jpg'), "word": "July"},
        {"image_path": url_for('static', filename='images/flashcards/months/August.jpg'), "word": "August"},
        {"image_path": url_for('static', filename='images/flashcards/months/September.jpg'), "word": "September"},
        {"image_path": url_for('static', filename='images/flashcards/months/October.jpg'), "word": "October"},
        {"image_path": url_for('static', filename='images/flashcards/months/November.jpg'), "word": "November"},
        {"image_path": url_for('static', filename='images/flashcards/months/December.jpg'), "word": "December"},
        {"image_path": url_for('static', filename='images/flashcards/months/January.jpg'), "word": "January"},
        {"image_path": url_for('static', filename='images/flashcards/months/February.jpg'), "word": "February"},
        {"image_path": url_for('static', filename='images/flashcards/months/March.jpg'), "word": "March"},
    ]
    return render_template('months.html', flashcard_images=flashcard_images)

@app.route('/numbers')
def numbers():
        flashcard_images = [
        {"image_path": url_for('static', filename='images/flashcards/counting/One.jpg'), "word": "One"},
        {"image_path": url_for('static', filename='images/flashcards/counting/Two.jpg'), "word": "Two"},
        {"image_path": url_for('static', filename='images/flashcards/counting/Three.jpg'), "word": "Three"},
        {"image_path": url_for('static', filename='images/flashcards/counting/Four.jpg'), "word": "Four"},
        {"image_path": url_for('static', filename='images/flashcards/counting/Five.jpg'), "word": "Five"},
        {"image_path": url_for('static', filename='images/flashcards/counting/Six.jpg'), "word": "Six"},
        {"image_path": url_for('static', filename='images/flashcards/counting/Seven.jpg'), "word": "Seven"},
        {"image_path": url_for('static', filename='images/flashcards/counting/Eight.jpg'), "word": "Eight"},
        {"image_path": url_for('static', filename='images/flashcards/counting/Nine.jpg'), "word": "Nine"},
        {"image_path": url_for('static', filename='images/flashcards/counting/Ten.jpg'), "word": "Ten"},
    ]
        return render_template('numbers.html',flashcard_images=flashcard_images)

@app.route('/berries')
def berries():     
     flashcard_images = [   
        {"image_path": url_for('static', filename='images/flashcards/berries/Blackberry.jpg'), "word": "Blackberry"},
        {"image_path": url_for('static', filename='images/flashcards/berries/BlackCurrant.jpg'), "word": "Black Currant"},
        {"image_path": url_for('static', filename='images/flashcards/berries/Blueberry.jpg'), "word": "Blueberry"},
        {"image_path": url_for('static', filename='images/flashcards/berries/Cherry.jpg'), "word": "Cherry"},
        {"image_path": url_for('static', filename='images/flashcards/berries/Cranberry.jpg'), "word": "Cranberry"},
        {"image_path": url_for('static', filename='images/flashcards/berries/Gooseberry.jpg'), "word": "Gooseberry"},
        {"image_path": url_for('static', filename='images/flashcards/berries/Melon.jpg'), "word": "Melon"},
        {"image_path": url_for('static', filename='images/flashcards/berries/Raspberry.jpg'), "word": "Raspberry"},
        {"image_path": url_for('static', filename='images/flashcards/berries/RedCurrant.jpg'), "word": "Red Currant"},
        {"image_path": url_for('static', filename='images/flashcards/berries/Strawberry.jpg'), "word": "Strawberry"},
        {"image_path": url_for('static', filename='images/flashcards/berries/Watermelon.jpg'), "word": "Watermelon"},
        ]
     return render_template('berries.html',flashcard_images=flashcard_images)

@app.route('/animals')
def animals():
         flashcard_images = [   
        {"image_path": url_for('static', filename='images/flashcards/animals/Cat.jpg'), "word": "Cat"},
        {"image_path": url_for('static', filename='images/flashcards/animals/Cow.jpg'), "word": "Cow"},
        {"image_path": url_for('static', filename='images/flashcards/animals/Dog.jpg'), "word": "Dog"},
        {"image_path": url_for('static', filename='images/flashcards/animals/Elephant.jpg'), "word": "Elephant"},
        {"image_path": url_for('static', filename='images/flashcards/animals/Fish.jpg'), "word": "Fish"},
        {"image_path": url_for('static', filename='images/flashcards/animals/Horse.jpg'), "word": "Horse"},
        {"image_path": url_for('static', filename='images/flashcards/animals/Lion.jpg'), "word": "Lion"},
        {"image_path": url_for('static', filename='images/flashcards/animals/Monkey.jpg'), "word": "Monkey"},
        {"image_path": url_for('static', filename='images/flashcards/animals/Pig.jpg'), "word": "Pig"},
        {"image_path": url_for('static', filename='images/flashcards/animals/Rabbit.jpg'), "word": "Rabbit"},
        {"image_path": url_for('static', filename='images/flashcards/animals/Tiger.jpg'), "word": "Tiger"},
        {"image_path": url_for('static', filename='images/flashcards/animals/Turtle.jpg'), "word": "Turtle"},
        ] 
         return render_template('animals.html',flashcard_images=flashcard_images)

@app.route('/produce')
def produce():
         flashcard_images = [   
        {"image_path": url_for('static', filename='images/flashcards/produce/Apple.jpg'), "word": "Apple"},
        {"image_path": url_for('static', filename='images/flashcards/produce/Beetroot.jpg'), "word": "Beetroot"},
        {"image_path": url_for('static', filename='images/flashcards/produce/Cabbage.jpg'), "word": "Cabbage"},
        {"image_path": url_for('static', filename='images/flashcards/produce/Corn.jpg'), "word": "Corn"},
        {"image_path": url_for('static', filename='images/flashcards/produce/Cucumber.jpg'), "word": "Cucumber"},
        {"image_path": url_for('static', filename='images/flashcards/produce/Lemon.jpg'), "word": "Lemon"},
        {"image_path": url_for('static', filename='images/flashcards/produce/Onion.jpg'), "word": "Onion"},
        {"image_path": url_for('static', filename='images/flashcards/produce/Peach.jpg'), "word": "Peach"},
        {"image_path": url_for('static', filename='images/flashcards/produce/Pear.jpg'), "word": "Pear"},
        {"image_path": url_for('static', filename='images/flashcards/produce/Pineapple.jpg'), "word": "Pineapple"},
        {"image_path": url_for('static', filename='images/flashcards/produce/Plum.jpg'), "word": "Plum"},
        {"image_path": url_for('static', filename='images/flashcards/produce/Tomato.jpg'), "word": "Tomato"},
        ]
         return render_template('produce.html',flashcard_images=flashcard_images)

@app.route('/colours')
def colours():
         flashcard_images = [   
        {"image_path": url_for('static', filename='images/flashcards/colours/Black.jpg'), "word": "Black"},
        {"image_path": url_for('static', filename='images/flashcards/colours/Blue.jpg'), "word": "Blue"},
        {"image_path": url_for('static', filename='images/flashcards/colours/Brown.jpg'), "word": "Brown"},
        {"image_path": url_for('static', filename='images/flashcards/colours/Gold.jpg'), "word": "Gold"},
        {"image_path": url_for('static', filename='images/flashcards/colours/Green.jpg'), "word": "Green"},
        {"image_path": url_for('static', filename='images/flashcards/colours/Grey.jpg'), "word": "Grey"},
        {"image_path": url_for('static', filename='images/flashcards/colours/Orange.jpg'), "word": "Orange"},
        {"image_path": url_for('static', filename='images/flashcards/colours/Purple.jpg'), "word": "Purple"},
        {"image_path": url_for('static', filename='images/flashcards/colours/Red.jpg'), "word": "Red"},
        {"image_path": url_for('static', filename='images/flashcards/colours/Silver.jpg'), "word": "Silver"},
        {"image_path": url_for('static', filename='images/flashcards/colours/White.jpg'), "word": "White"},
        {"image_path": url_for('static', filename='images/flashcards/colours/Yellow.jpg'), "word": "Yellow"},
        ]
         return render_template('colours.html',flashcard_images=flashcard_images)

@app.route('/transport')
def transport():   
     flashcard_images = [   
        {"image_path": url_for('static', filename='images/flashcards/transport/AirBalloon.jpg'), "word": "Air Ballon"},
        {"image_path": url_for('static', filename='images/flashcards/transport/Boat.jpg'), "word": "Boat"},
        {"image_path": url_for('static', filename='images/flashcards/transport/Bus.jpg'), "word": "Bus"},
        {"image_path": url_for('static', filename='images/flashcards/transport/Car.jpg'), "word": "Car"},
        {"image_path": url_for('static', filename='images/flashcards/transport/Ferry.jpg'), "word": "Ferry"},
        {"image_path": url_for('static', filename='images/flashcards/transport/Plane.jpg'), "word": "Plane"},
        {"image_path": url_for('static', filename='images/flashcards/transport/Satellite.jpg'), "word": "Satellite"},
        {"image_path": url_for('static', filename='images/flashcards/transport/Taxi.jpg'), "word": "Taxi"},
        {"image_path": url_for('static', filename='images/flashcards/transport/Truck.jpg'), "word": "Truck"},
        ]
     return render_template('months.html',flashcard_images=flashcard_images)

@app.route('/furniture')
def furniture():
         flashcard_images = [   
        {"image_path": url_for('static', filename='images/flashcards/furniture/Bench.jpg'), "word": "Bench"},
        {"image_path": url_for('static', filename='images/flashcards/furniture/Chair.jpg'), "word": "Chair"},
        {"image_path": url_for('static', filename='images/flashcards/furniture/Door.jpg'), "word": "Door"},
        {"image_path": url_for('static', filename='images/flashcards/furniture/Hanger.jpg'), "word": "Hanger"},
        {"image_path": url_for('static', filename='images/flashcards/furniture/Sofa.jpg'), "word": "Sofa"},
        {"image_path": url_for('static', filename='images/flashcards/furniture/Steps.jpg'), "word": "Steps"},
        {"image_path": url_for('static', filename='images/flashcards/furniture/Stool.jpg'), "word": "Stool"},
        {"image_path": url_for('static', filename='images/flashcards/furniture/Table.jpg'), "word": "Table"},
        {"image_path": url_for('static', filename='images/flashcards/furniture/Wardrobe.jpg'), "word": "Wardrobe"},
        ] 
         return render_template('numbers.html',flashcard_images=flashcard_images)

@app.route('/weather')
def weather():
         flashcard_images = [   
        {"image_path": url_for('static', filename='images/flashcards/weather/Cloud.jpg'), "word": "Cloud"},
        {"image_path": url_for('static', filename='images/flashcards/weather/Cold.jpg'), "word": "Cold"},
        {"image_path": url_for('static', filename='images/flashcards/weather/Fog.jpg'), "word": "Fog"},
        {"image_path": url_for('static', filename='images/flashcards/weather/Ice.jpg'), "word": "Ice"},
        {"image_path": url_for('static', filename='images/flashcards/weather/Lightning.jpg'), "word": "Lightning"},
        {"image_path": url_for('static', filename='images/flashcards/weather/Rain.jpg'), "word": "Rain"},
        {"image_path": url_for('static', filename='images/flashcards/weather/Snow.jpg'), "word": "Snow"},
        {"image_path": url_for('static', filename='images/flashcards/weather/Snowfall.jpg'), "word": "Snowfall"},
        {"image_path": url_for('static', filename='images/flashcards/weather/Storm.jpg'), "word": "Storm"},
        {"image_path": url_for('static', filename='images/flashcards/weather/Sunny.jpg'), "word": "Sunny"},
        {"image_path": url_for('static', filename='images/flashcards/weather/Warm.jpg'), "word": "Warm"},
        {"image_path": url_for('static', filename='images/flashcards/weather/Wind.jpg'), "word": "Wind"},
        ] 
         return render_template('berries.html',flashcard_images=flashcard_images)


# Define routes for test pages for each level

@app.route('/beginnertest')
def beginnertest():
    return render_template('beginnertest.html')

@app.route('/intermediatetest')
def intermediatetest():
    return render_template('intermediatetest.html')

@app.route('/advancedtest')
def advancedtest():
    return render_template('advancedtest.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

