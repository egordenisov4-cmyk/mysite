from flask import Flask, render_template, request, redirect, url_for, session

app = flask(__name__)
app.secret_key = "secret123"  # обязательно для сессий


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/reviews")
def reviews():
    return render_template("reviews.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # для учебы просто перекидываем на логин
        return redirect("/login")
    return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        session["user"] = email
        return redirect("/profile")
    return render_template("login.html")



@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user" not in session:
        return redirect("/login")

    # если бронирований ещё нет — создаём
    if "bookings" not in session:
        session["bookings"] = []

    if request.method == "POST":
        booking = {
            "date": request.form.get("date"),
            "time": request.form.get("time"),
            "guests": request.form.get("guests")
        }

        session["bookings"].append(booking)
        session.modified = True  # ВАЖНО

    return render_template(
        "profile.html",
        user=session["user"],
        bookings=session["bookings"]
    )




@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)




