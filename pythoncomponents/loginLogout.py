from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from bson.objectid import ObjectId
import bcrypt

# Define blueprints
login_bp = Blueprint('login', __name__)
logout_bp = Blueprint('logout', __name__)
register_bp = Blueprint('register', __name__)

# Login route and view
@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = collection.find_one({"email": email})

        if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
            session["user_id"] = str(user["_id"])
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

# Logout route and view
@logout_bp.route('/logout')
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))

# Register route and view
@register_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        firstname = request.form["Firstname"]
        lastname = request.form["Lastname"]
        email = request.form["Email"]
        password = request.form["Password"]

        existing_user = collection.find_one({"email": email})
        if existing_user:
            return render_template("register.html", error="Email already exists")

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user_data = {
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "password": hashed_password,
        }
        collection.insert_one(user_data)

        return redirect(url_for("login"))

    return render_template("register.html")

# Dashboard route and view
@app.route("/dashboard")
def dashboard():
    if "user_id" in session:
        user_id = session["user_id"]
        user = collection.find_one({"_id": ObjectId(user_id)})
        return render_template("dashboard.html")
    else:
        flash("Please log in first", "warning")
        return redirect(url_for("login"))

# Register blueprints
app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(register_bp)

if __name__ == "__main__":
    app.run(debug=True)
