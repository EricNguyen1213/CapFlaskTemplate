from app import app
from flask import render_template

# This is for rendering the home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aboutus')
<<<<<<< HEAD
def test():
=======
def aboutus():
>>>>>>> a08386a94239d8d234ae0d5a1ef66aa9d43ea93c
    return render_template('aboutus.html')