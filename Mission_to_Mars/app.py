
# Import Libraries

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Flask App
app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_DB")


# Route that renders index.html
@app.route("/")
def index():
    scraped_data = mongo.db.scraped_data.find_one()
    return render_template("index.html", scraped_data = scraped_data)

@app.route("/scrape")
def scrape():
    scraped_data = mongo.db.scraped_data
    scraped_data_list = scrape_to_mars.scrape()
    scraped_data.update({}, scraped_data_list, upsert=True)
    return redirect("/", code=302)

@app.route("/img")
def img():
        img_data = scrape_mars.featured_image()
        return render_template("index.html", img_data = hemisphere)

if __name__ == "__main__":
    app.run(debug=True)
