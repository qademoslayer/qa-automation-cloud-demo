from flask import Flask, request, redirect, make_response, render_template_string

app = Flask(__name__)

LOGIN_HTML = """
<!doctype html>
<html>
  <head><title>Login</title></head>
  <body>
    <h1>Login</h1>
    {% if error %}<p style="color:red">{{ error }}</p>{% endif %}
    <form method="post">
      <label>Username</label>
      <input name="username" />
      <br/>
      <label>Password</label>
      <input name="password" type="password" />
      <br/>
      <button type="submit">Sign in</button>
    </form>
  </body>
</html>
"""

DASHBOARD_HTML = """
<!doctype html>
<html>
  <head><title>Dashboard</title></head>
  <body>
    <h1>Dashboard</h1>
    <p id="welcome">Welcome, {{ user }}</p>
    <a href="/logout">Logout</a>
  </body>
</html>
"""

@app.get("/")
def home():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template_string(LOGIN_HTML, error=None)

    username = (request.form.get("username") or "").strip()
    password = (request.form.get("password") or "").strip()

    # demo credentials
    if username == "demo" and password == "demo":
        resp = make_response(redirect("/dashboard"))
        resp.set_cookie("session", "ok", httponly=True)
        resp.set_cookie("user", username)
        return resp

    return render_template_string(LOGIN_HTML, error="Invalid credentials"), 401

@app.get("/dashboard")
def dashboard():
    if request.cookies.get("session") != "ok":
        return redirect("/login")

    user = request.cookies.get("user") or "unknown"
    return render_template_string(DASHBOARD_HTML, user=user)

@app.get("/logout")
def logout():
    resp = make_response(redirect("/login"))
    resp.delete_cookie("session")
    resp.delete_cookie("user")
    return resp

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
