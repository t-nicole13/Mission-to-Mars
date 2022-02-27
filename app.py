from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# Set Up Flask
app = Flask(__name__)

# Use flask_pymong to set up mongo connection
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_app'
mongo = PyMongo(app)

# # Set Up App Routes
# Route for our html page
@app.route('/')
def index():
    mars = mongo.db.mars.find_one() # uses PyMongo to find the 'mars' collection in our db
    return render_template('index_challenge.html', mars = mars) # return html template using index.html and use the 'mars' collection


# Route for scraping
@app.route('/scrape')
def scrape():
    mars = mongo.db.mars # accessing the db
    mars_data = scraping.scrape_all() # scrape new data
    mars.update_one({}, {'$set': mars_data}, upsert = True) # update the db
    return redirect('/', code = 302) # return a message when successful




# # Tell Flask to Run

if __name__ == '__main__':
    app.run()

