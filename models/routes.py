from flask import request, redirect, url_for, session, render_template
from models.database_handling import insert_user, find_user_by_email, authenticate_user

# Other routes and their implementations remain the same...


# app/routes.py

from flask import request, redirect, url_for, session, render_template

def register_routes(app):
    from models.database_handling import insert_user, find_user_by_email, authenticate_user

    # Login route
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            user = find_user_by_email(email)

            if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
                session["user_id"] = str(user["_id"])
                return redirect(url_for("dashboard"))
            else:
                return render_template("login.html", error="Invalid credentials")

        return render_template("login.html")

    # Logout route
    @app.route("/logout")
    def logout():
        session.pop("user_id", None)
        return redirect(url_for("login"))

    # Registration route
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            firstname = request.form["Firstname"]
            lastname = request.form["Lastname"]
            email = request.form["Email"]
            password = request.form["Password"]

            existing_user = find_user_by_email(email)
            if existing_user:
                return render_template("register.html", error="Email already exists")
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            insert_user(firstname, lastname, email, hashed_password)

            return redirect(url_for("login"))

        return render_template("register.html")

    # Dashboard route
    @app.route("/dashboard")
    def dashboard():
        if "user_id" in session:
            user_id = session["user_id"]
            user = find_user_by_id(user_id)
            return render_template("dashboard.html", user=user)
        else:
            flash("Please log in first", "warning")
            return redirect(url_for("login"))

# Services route
@app.route("/services", methods=["GET", "POST"])
def services():
    return render_template("services.html")

# Contact route
@app.route("/contact", methods=["GET", "POST"])
def contact():
    return render_template("contactus.html")

# About route
@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html")

# Index route
@app.route("/index", methods=["GET", "POST"])
def index():
    return render_template("index.html")

# Blog routes
@app.route("/blog1", methods=["GET", "POST"])
def blog1():
    return render_template("blog1.html")

@app.route("/blog2", methods=["GET", "POST"])
def blog2():
    return render_template("blog2.html")

@app.route("/blog3", methods=["GET", "POST"])
def blog3():
    return render_template("blog3.html")

# Content routes
@app.route("/content1", methods=["GET", "POST"])
def content1():
    return render_template("content1.html")

@app.route("/content2", methods=["GET", "POST"])
def content2():
    return render_template("content2.html")

@app.route("/content3", methods=["GET", "POST"])
def content3():
    return render_template("content3.html")

@app.route("/content4", methods=["GET", "POST"])
def content4():
    return render_template("content4.html")

# Feature routes
@app.route("/feature1", methods=["GET", "POST"])
def feature1():
    return render_template("feature1.html")

@app.route("/feature2", methods=["GET", "POST"])
def feature2():
    return render_template("feature2.html")

@app.route("/feature3", methods=["GET", "POST"])
def feature3():
    return render_template("feature3.html")
