from flask import Flask, render_template, session, request, redirect, url_for
from google.cloud import firestore
from courses import courses
import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "GET":
        if not "user_email" in request.args:
            return render_template("email.html")
        
        if not "curr_course" in request.args:
            return "Malformed url", 400
        

        user_email = request.args["user_email"]
        try:
            curr_course = int(request.args["curr_course"])
        except ValueError:
            return "Malformed url", 400

        if curr_course == len(courses):
            return "You've completed the survey, you'll now recieve the ultimate reward I, Aditya Shankar, can give..., I hereby admit python is not greater than Java"

        if not (curr_course >= 0 and curr_course < len(courses)):
            return "invalid curr course index", 400

        next_course = curr_course + 1
        curr_course_email = courses[curr_course]

        return render_template("q.html", 
                               next_course=next_course,
                               curr_course=curr_course,
                               curr_course_email=curr_course_email,
                               user_email=user_email)

    else:
        curr_course = int(request.form["curr_course"])
        user_email   = request.form["user_email"]
        session_rec = request.form["session_recommend"]
        rating = request.form["rating"]

        db = firestore.Client()
        collection = db.collection("survey-data")
        prev_ref = collection.where("user", "==", user_email).where("course", "==", courses[curr_course]).get()

        if len(prev_ref) > 0:
            prev_ref[0].reference.delete()

        collection.add({
            "user":user_email,
            "course_num":curr_course,
            "course":courses[curr_course],
            "session-recommendation" : session_rec,
            "difficulty rating": rating,
            "insertion time": datetime.datetime.now()
        })


        # some processing for storing information over here
        return redirect(url_for(f"main", user_email=user_email, curr_course=curr_course + 1))


if __name__ == "__main__":
    app.run(debug=True)
