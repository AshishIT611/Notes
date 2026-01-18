from flask import Flask,render_template,request,redirect,url_for,flash
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from bson.objectid import ObjectId
load_dotenv("config/config.env")
app=Flask(__name__)
app.secret_key=os.getenv("SECRET_KEY")
MONGO_URI=os.getenv("MONGO_URI")
DB_NAME=os.getenv("DB_NAME")
COLLECTION_NAME=os.getenv("COLLECTION_NAME")
client=MongoClient(MONGO_URI)
db=client[DB_NAME]
collection=db[COLLECTION_NAME]
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/write",methods=["GET","POST"])
def write():
    if request.method=="POST":
        data={
            "name":request.form["name"],
            "email":request.form["email"],
            "phone":request.form["phone"],
            "message":request.form.get("message","")
        }
        collection.insert_one(data)
        flash("Data added successfully ✅")
        return redirect(url_for("home"))
    return render_template("write.html")
@app.route("/read")
def read():
    data=collection.find()
    return render_template("read.html",data=data)
@app.route("/delete/<id>")
def delete(id):
    collection.delete_one({"_id":ObjectId(id)})
    flash("Data deleted successfully ❌")
    return redirect(url_for("read"))
@app.route("/update/<id>")
def update(id):
    data=collection.find_one({"_id":ObjectId(id)})
    return render_template("update.html",data=data)
@app.route("/update_data/<id>", methods=["POST"])
def update_data(id):
    updated_data = {
        "name": request.form["name"],
        "email": request.form["email"],
        "phone": request.form["phone"],
        "message": request.form["message"]
    }
    collection.update_one({"_id": ObjectId(id)},{"$set": updated_data})
    flash("Data updated successfully ✏️")
    return redirect(url_for("read"))
if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000)