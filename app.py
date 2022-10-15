from flask import Flask, render_template, url_for, request, send_file, redirect, flash
import os
from operator import itemgetter
import diff

app = Flask(__name__)
app.secret_key = 'kljuc'


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/snipe_changes", methods=["POST", "GET"])
def snipe_changes():
    file_name1 = ""
    file_name2 = ""
    save_file_name = "file"
    path = (os.path.abspath("results_cron/pretty")+"/")
    dirs = os.listdir(path)
    temp = []

    for file in dirs:
        if ".json" in file:
            file_date = file[:-5]
            file_date = file_date[-10:]
            temp.append({'date': file_date, 'name': file})
    temp = sorted(temp, key=itemgetter('date'), reverse=True)

    if request.method == "POST":
        file_name1 = (request.form.get("date1"))[:-5]
        file_name2 = (request.form.get("date2"))[:-5]

        if file_name1 == file_name2:
            flash("Nije moguće izabrati dva ista datuma!")
        else:
            diff.Diff(file_name1, file_name2, save_name=save_file_name,
                      save_path="results_cron/diff/excel/").pretty_diffs_xlsx()

            print(file_name1, file_name2)
            return redirect(url_for("download", filename=save_file_name+".xlsx"))


    return render_template('snipe_changes.html', data=temp)


@app.route("/test", methods=["POST", "GET"])
def test():
    if request.method == "POST":
        print(request.form.get("recordinput"))

    return render_template("test.html")


@app.route('/download/<filename>')
def download(filename):
    path = ((os.path.abspath(('results_cron/diff/excel/'))+"/") + filename)
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
