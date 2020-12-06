from flask import Flask, render_template, session, request
from courses import courses

app = Flask(__name__)

@app.route("/")
def main():
    if not "user-name" in request.args:
        return render_template("name.html")
    
    if not "curr-course" in request.args:
        return "Malformed url", 400
    

    user_name = request.args["user-name"]
    try:
        curr_course = int(request.args["curr-course"])
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

if __name__ == "__main__":
    app.run(debug=True)
