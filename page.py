from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

app.config['SECRET_KEY'] = "a67c6cc35e60b993eed3ec744bbc84da"

@app.route("/", methods = ["GET", "POST"])
def home():
    #if request.method == "POST":
    print(request.form.get("selection1"))
    if request.form.get("selection1") == "AddNew":
        return redirect(url_for("addData"))
    return render_template("home.html")
    
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/addData", methods = ['GET','POST'])
def addData():
    print(request.form.get("input_button"))

    return render_template("adddata.html")

if __name__ == "__main__":
    app.run(debug = True)

