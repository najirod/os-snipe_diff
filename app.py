from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/snipe_changes")
def snipe_changes():
    return render_template('snipe_changes.html')

if __name__ == "__main__":
    app.run(debug=True)
