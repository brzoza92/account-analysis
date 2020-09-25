from flask import Flask, render_template, request


app = Flask(__name__)

app.config['SECRET_KEY'] = "a67c6cc35e60b993eed3ec744bbc84da"

@app.route("/")
def home():
    return render_template("home.html", title = "Home")
    
@app.route("/about")
def about():
    return render_template("about.html", title = "About")


@app.route("/selection", methods = ['POST'])
def selection():
    text_in = request.form.get('text_in')
    return render_template("selection.html", title = "Selection", text_input = text_in)

if __name__ == "__main__":
    app.run(debug = True)

