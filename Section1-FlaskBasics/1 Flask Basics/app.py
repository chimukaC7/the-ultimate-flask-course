from flask import Flask, request, redirect, url_for

app = Flask(__name__) # this is the Flask application object, it is used to define routes and run the app

@app.route("/")
def index():
    return "<h1>Hello</h1>"

@app.route("/home", methods=["GET"])# explicit stating that this route only accepts GET requests, this is the default behavior for routes
def home():
    return "<h1>Home</h1>"

@app.route("/json")
def json():
    return {"mykey": "JSON Value!", "mylist": [1, 2, 3, 4, 5]}

@app.post("/json")
def json():
    return {"mykey": "JSON Value!", "mylist": [1, 2, 3, 4, 5]}

@app.route("/dynamic", defaults={"user_input": "default"})
@app.route("/dynamic/<user_input>") # use angle brackets to declare route variables
def dynamic(user_input):
    return f"<h1>The user entered: {user_input}</h1>"

@app.route("/query")
def query():
    # retrieving query string arguments
    first = request.args.get("first")
    second = request.args.get("second")
    return f"<h1>The query string contains: {first} and {second}</h1>"

@app.route("/form", methods=["GET", "POST"]) # use the list method to state the request methods
def form():
    if request.method == "POST":
        #user_input = request.form.get("user_input") # use the get method two avoid a KeyError if the key is not present in the form data
        user_input = request.form["user_input"] # use the form method to retrieve form data, this will raise a KeyError if the key is not present in the form data
        print(user_input)

        # return f"<h1>The user entered: {user_input}</h1>"
        return redirect(url_for("home")) # use the redirect function to redirect the user to a different route, use the url_for function to generate the URL for the route, this is better than hardcoding the URL because it will automatically update if the route changes
        
    return ('<form method="POST">'
            '<input type="text" name="user_input" />'
            '<input type="submit" />'
            '</form>')

@app.route("/acceptjson")
def acceptjson():
    json_data = request.get_json() # use the get_json method to retrieve JSON data from the request body, this will return None if the request does not contain valid JSON data

    api_input = json_data["mylist"]
    hello = json_data["hello"]

    return {"api_input": api_input, "hello": hello}

@app.route("/error")
def error():
    a = 1 / 0
    return "Error"