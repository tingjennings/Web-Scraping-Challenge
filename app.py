# Import Dependencies 
from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrape_mars
import pymongo

# Create an instance of Flask app
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)


@app.route("/")
def home(): 
    print(mongo.db)
    mars_info = mongo.db.mars_db.find_one()
    return render_template("index.html", mars_info=mars_info)

@app.route("/scrape")
def scrape(): 

    mars_info = mongo.db.mars_db
    print('start scrape')
    mars_data = scrape_mars.scrape_all()
    mars_info.update({}, mars_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)