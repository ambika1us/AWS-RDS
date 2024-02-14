from flask import Flask, jsonify, render_template, request
from flask_pymongo import PyMongo

app = Flask(__name__, static_url_path='')
app.config["MONGO_URI"] = "mongodb://localhost:27017/edureka"
mongo = PyMongo(app)

@app.route('/')
def home_page():
    return 'hiiii'

@app.route('/about/')
def about_page():
    online_users = mongo.db.zomato.find({})
    print (online_users)
    out = {"data": online_users}
    return out

@app.route("/data/")
def data_page():
    online_users = mongo.db.cars.find({})
    return render_template("data.html",
        online_users=online_users)

@app.route('/forms/')
def form_page():
    return render_template('form.html')

@app.route('/books/')
def hi_flask():
    users = [ "Frank", "Steve", "Alice", "Bruce" ]
    return render_template('books.html',users=users)

@app.route('/handle_data', methods=['POST'])
def handle_data():
    projectpath = request.form['projectFilepath']
    mongo.db.first.insert({"name":projectpath})
    return render_template('about.html')

@app.route('/update_data', methods=['POST'])
def update_data():
    oldData = request.form['hiddenData']
    newData = request.form['updateData']
    print(">>>>>"+ newData)
    mongo.db.first.update({"name":oldData},{"$set":{"name":newData}}, upsert=False)
    return render_template('about.html')


app.run(port=3300)
