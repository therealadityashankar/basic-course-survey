from flask import Flask, render_template, session, request, redirect, url_for
from google.cloud import firestore
from courses import courses

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "GET":
        if not "user_name" in request.args:
            return render_template("name.html")
        
        if not "curr_course" in request.args:
            return "Malformed url", 400
        

        user_name = request.args["user_name"]
        try:
            curr_course = int(request.args["curr_course"])
        except ValueError:
            return "Malformed url", 400

        if not (curr_course >= 0 and curr_course < len(courses)):
            return "invalid curr course index", 400

        next_course = curr_course + 1
        curr_course_name = courses[curr_course]

        return render_template("q.html", 
                               next_course=next_course,
                               curr_course=curr_course,
                               curr_course_name=curr_course_name,
                               user_name=user_name)

    else:
        curr_course = int(request.form["curr_course"])
        user_name   = request.form["user_name"]
        session_rec = request.form["session_recommend"]
        rating = request.form["rating"]

        db = firestore.Client()
        doc_ref = db.collection("survey-data").document(user_name)
        doc_ref.set({
            "session-recommendation" : session_rec,
            "difficulty rating": rating
        })

        if curr_course == len(courses) - 1:
            return "You've completed the survey, you'll now recieve the ultimare reward I, Aditya Shankar, can give..., I hereby admit python is not greater than Java"

        # some processing for storing information over here
        return redirect(url_for(f"main", user_name=user_name, curr_course=curr_course + 1))


if __name__ == "__main__":
    app.run(debug=True)
