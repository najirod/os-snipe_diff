from flask import Flask, render_template, url_for, request, send_file, redirect, flash
import os
from operator import itemgetter
import diff
from pathlib import  Path
import sys
import os
from dotenv import load_dotenv
import snipe_sofa_framework

app = Flask(__name__)
app.secret_key = 'kljuc'


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/snipe_changes", methods=["POST", "GET"])
def snipe_changes():
    root_path = (sys.path[1] + "/")  # /Users/dpustahija1/PycharmProjects/os-snipe_diff/
    dotenv_path = (root_path + ".env")
    print(dotenv_path)
    load_dotenv(dotenv_path=dotenv_path)
    file_name1 = ""
    file_name2 = ""
    save_file_name = "file"
    path = (root_path + ("results_cron/pretty/"))
    print(path)
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
            print(diff.Diff(file_name1, file_name2, save_name=save_file_name,
                      save_path="results_cron/diff/excel/"))
            if diff.Diff(file_name1, file_name2, save_name=save_file_name,
                      save_path="results_cron/diff/excel/").check_if_changed() == "0":
                flash("Nema Promjena između zadanih datuma!")
            else:
                print(file_name1, file_name2)
                return redirect(url_for("download", filename=save_file_name+".xlsx"))


    return render_template('snipe_changes.html', data=temp)


@app.route("/reports", methods=["POST", "GET"])
def reports():
    if request.method == "POST":
        if request.form['submit_button'] == 'proba':
            #snipe_sofa_framework.Reports().matching_snipe_and_os_report()
            return redirect(url_for("download", filename=("matching_snipe_and_os_report"+".xlsx")))

        elif request.form['submit_button'] == 'proba2':
            #snipe_sofa_framework.Reports().matching_snipe_and_os_report()
            return redirect(url_for("download", filename=("non_matching_snipe_and_os_report"+".xlsx")))

        elif request.form['submit_button'] == 'proba3':
            #snipe_sofa_framework.Reports().matching_snipe_and_os_report()
            return redirect(url_for("download", filename=("rest_in_snipe_report"+".xlsx")))


    return render_template("reports.html")

@app.route("/test", methods=["POST", "GET"])
def test():
    if request.method == "POST":
        print(request.form.get("recordinput"))

    return render_template("test.html")


@app.route('/download/<filename>')
def download(filename):
    root_path = (sys.path[1] + "/")  # /Users/dpustahija1/PycharmProjects/os-snipe_diff/
    if filename == "file.xlsx":
        path = ((root_path + ('results_cron/diff/excel/')) + filename)
    elif filename == "matching_snipe_and_os_report.xlsx":
        path = ((root_path + ('results/matching/')) + filename)
    elif filename == "non_matching_snipe_and_os_report.xlsx":
        path = ((root_path + ('results/non_matching/')) + filename)
    elif filename == "rest_in_snipe_report.xlsx":
        path = ((root_path + ('results/rest/')) + filename)
    return send_file(path, as_attachment=True)

@app.route('/snipeit')
def snipeit():
    return redirect("http://10.10.1.54/")

if __name__ == "__main__":
    app.run(debug=True)
