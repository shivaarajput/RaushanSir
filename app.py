import os
import json
import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def load_content():
    with open('static/data/content.json') as content_file:
        content = json.load(content_file)
    with open('static/data/sayari.json') as sayari_file:
        sayari_data = json.load(sayari_file)
    with open('static/data/urls.json') as urls_file:
        links = json.load(urls_file)

    return content, links, sayari_data

# Route for the home page
@app.route('/')
def home():
    image_folder = os.path.join('static', 'gallary')
    image_names = os.listdir(image_folder)
    content, links, sayari_data = load_content()
    return render_template('index.html', links=links, my=content, sayari=sayari_data, images=image_names)

@app.route('/<path:page>')
def render_page(page):
    content, links, sayari_data = load_content()
    return render_template(page, links=links, my=content, sayari=sayari_data)

# Route to handle form submission
@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        # Handle form submission
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject'] 
        message = request.form['message']
        
        # Send data to Telegram bot
        send_to_telegram(name, email, subject, message)
        
        # Optionally, you can redirect somewhere after submission
  #      return redirect(url_for('thank_you'))
    
    # Handle other methods if needed
    return  "OK", 200

# Route for the thank you page
#@app.route('/thank_you')
#def thank_you():
 #   return "Thank you for your message!"

def send_to_telegram(name, email, subject, message):
    bot_token = os.environ.get('BOT_TOKEN')
    chat_id = os.environ.get('CHAT_ID')
    text = f'New message from {name}\nEmail: {email}\nSubject: {subject}\n\nMessage: {message}'
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={text}'

    response = requests.get(url)
    return response.json()

if __name__ == '__main__':
    app.run()
