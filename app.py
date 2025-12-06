from flask import Flask, render_template, request, session, redirect, url_for
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Change this to a secure random key in production
GIPHY_API_KEY = os.getenv('GIPHY_API_KEY')

def get_random_gif(tag):
    if not GIPHY_API_KEY:
        return "https://placekitten.com/500/300"  # Fallback if no API key
    url = f"https://api.giphy.com/v1/gifs/random?api_key={GIPHY_API_KEY}&tag={tag}&rating=g"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['data']['images']['original']['url']
    else:
        return "https://placekitten.com/500/300"  # Fallback on error

@app.route('/', methods=['GET'])
def index():
    session.clear()  # Reset session for a fresh start
    return render_template('index.html')

@app.route('/page1', methods=['GET', 'POST'])
def page1():
    if request.method == 'POST':
        mood = request.form.get('mood')
        if mood:
            session['mood'] = mood
        else:
            return redirect(url_for('index'))
    elif 'mood' in session:
        mood = session['mood']
    else:
        return redirect(url_for('index'))
    
    gif_url = get_random_gif(mood)
    return render_template('page1.html', mood=mood, gif_url=gif_url)

@app.route('/page2', methods=['POST'])
def page2():
    wish_mood = request.form.get('wish_mood')
    if not wish_mood:
        return redirect(url_for('page1'))
    
    gif_url = get_random_gif(wish_mood)
    return render_template('page2.html', wish_mood=wish_mood, gif_url=gif_url)

if __name__ == '__main__':
    app.run(debug=True)