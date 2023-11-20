# copied from video 114
import os

# 01.python.exe -m pip install --upgrade pip
# 02.pip install flask
# 03.flask --app app_01.py --debug run
# request is for request.method
from flask import Flask, render_template, request

# importing datatime module
import datetime

# You can install, pymongo on its own, but with the srv in square
# brackets there, it'll also install some extra package that we need in
# order to connect to MongoDB Atlas.
# And that package is called dnspython.
# So it installs pymongo and dnspython.
# 04.pip install pymongo[srv]
# to check what has been installed
#  pip freeze
# >
# blinker==1.7.0
# click==8.1.7
# colorama==0.4.6
# dnspython==2.4.2  # installed
# Flask==3.0.0
# itsdangerous==2.1.2
# Jinja2==3.1.2
# MarkupSafe==2.1.3
# pymongo==4.6.0
# Werkzeug==3.0.1
# 05. pip install -r requirements.txt
from pymongo import MongoClient

# adding env
import os
from dotenv import load_dotenv
# this variable - just for storing info, later we are going to usr MongoDb
# entries = [] # we're using DB
# 06 pip install python-dotenv
# 07 pip install gunicorn
# we need to create create_app() function to use factory

# gunicorn "app:create_app()"   doesn't work inWindows

load_dotenv()
# load_dotenv() goes into the .env file, and populates environment variables based on the lines in that file.

def create_app():
    app = Flask(__name__)

    # We have a client, but we haven't connected to any database yet.
    # client = MongoClient("mongodb+srv://andrey:FMn0hud4rHUrAl3f@microblog-application.qfnk0rz.mongodb.net/")
    # replacing with a env. variable
    client = MongoClient(os.getenv("MONGODB_URI"))
    # So what we're going to do now is we're going to connect to the database.
    # db = client.microblog
    # better is next
    app.db = client.microblog

    @app.route("/", methods=["GET", "POST"])
    def home():
        # And we can do something like .find and put in an empty dictionary., "ENTRIES IS A COLLECTION IN DB"
        # print([e for e in app.db.entries.find({})])  # Andrey -- remember syntax !!!
        # works
        # 127.0.0.1 - - [19/Nov/2023 11:53:48] "GET /static/logo.svg HTTP/1.1" 304 -
        # [{'_id': ObjectId('6559f7af2f90163befd983ae'), 'name': 'test'}]

        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            # removing this as we're saving in DB entries.append((entry_content, formatted_date))
            # adds the list of tuples
            app.db.entries.insert_one({"content": entry_content, "data": formatted_date})
            # according video 113, we use {} as we are inserting the dictionary
        entries_with_date = [
            (
                # entry[0],
                entry["content"],
                entry["data"],
                datetime.datetime.strptime(entry["data"], "%Y-%m-%d").strftime("%b %d")
            )
            # for entry in entries
            for entry in app.db.entries.find({})
        ]
        # return render_template("home.html", entries=entries)
        return render_template("home.html", entries=entries_with_date)

    return app
