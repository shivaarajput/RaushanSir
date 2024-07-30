import os
import json
import requests
from flask import Flask, render_template, request, redirect, url_for
from io import BytesIO

app = Flask(__name__)


def load_content():
    with open("static/data/content.json") as content_file:
        content = json.load(content_file)
    with open("static/data/sayari.json") as sayari_file:
        sayari_data = json.load(sayari_file)
    with open("static/data/urls.json") as urls_file:
        links = json.load(urls_file)
    url = "https://lw7e6p1qbekb9ev7.public.blob.vercel-storage.com/feedback/feedbacks.json"
    response = requests.get(url)
    if response.status_code == 200:
        feedbacks = response.json()
    else:
        with open("static/data/feedbacks.json") as feed_file:
            feedbacks = json.load(feed_file)

    return content, links, sayari_data, feedbacks


# Route for the home page
@app.route("/")
def home():
    image_folder = os.path.join("static", "gallary")
    image_names = os.listdir(image_folder)
    content, links, sayari_data, feedbacks = load_content()
    return render_template(
        "index.html",
        links=links,
        my=content,
        sayari=sayari_data,
        images=image_names,
        feedbacks=feedbacks,
    )


"""
@app.route('/<path:page>')
def render_page(page):
    content, links, sayari_data,feedbacks = load_content()
    return render_template(page, links=links, my=content, sayari=sayari_data)
"""


# Route to handle form submission
@app.route("/submit_form", methods=["POST"])
def submit_form():
    if request.method == "POST":
        # Handle form submission
        name = request.form["name"]
        phone = request.form["phone"]
        subject = request.form["subject"]
        message = request.form["message"]

        send_to_telegram(name, phone, subject, message)

    return "OK", 200


# This is photo upload page
@app.route("/upload_image")
def upload_page():
    content, links, sayari_data, feedbacks = load_content()
    return render_template("upload.html", links=links)


def send_to_telegram(name, email, subject, message):
    bot_token = os.environ.get("BOT_TOKEN")
    chat_id = os.environ.get("CHAT_ID")

    text = f"New message from {name}\nPhone: {email}\nSubject: {subject}\n\nMessage: {message}"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={text}"
    url_sir = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id=6573678761&text={text}"
    requests.get(url_sir)
    response = requests.get(url)
    return response.json()


# Added for photo upload logic
def send_photo_to_telegram(file_stream, filename, description):
    bot_token = os.environ.get("TOKEN")
    chat_id = os.environ.get("CHAT_ID")

    files = {"photo": (filename, file_stream, "image/jpeg")}
    data = {"chat_id": chat_id, "caption": description}
    response = requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendPhoto", data=data, files=files
    )
    return response.json()


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["photo"]
    name = request.form["name"]
    phone = request.form["phone"]
    description = request.form["message"]
    caption = f"Name: {name}\nPhone: {phone}\nDescription: {description}"
    if file and description:
        file_stream = BytesIO(file.read())
        response = send_photo_to_telegram(file_stream, file.filename, caption)
        return "OK", 200
    return "No file uploaded or description is missing."


if __name__ == "__main__":
    app.run()
