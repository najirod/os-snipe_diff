import json
from crypt import methods

from flask import Flask, render_template, url_for, request, send_file, redirect, flash, jsonify
import os
from operator import itemgetter
import diff
from pathlib import Path
import sys
import os
from dotenv import load_dotenv
import snipe_sofa_framework
import receipt_statments
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_admin.contrib.sqla import *
from flask_admin.menu import MenuLink
import urllib.parse
from functools import wraps

if "venv" in sys.path[0]:
    root_path = (sys.path[1] + "/")
else:
    root_path = (sys.path[0] + "/")

app = Flask(__name__)
app.secret_key = 'kljuc'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + root_path + 'database/database.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

admin = Admin(app, template_mode='bootstrap3')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    user_level = db.Column(db.Integer, nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.username


class Rights(db.Model):
    id = db.Column(db.Integer, primary_key=True)


admin.add_view(ModelView(User, db.session))


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    email = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "email"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            # flash("User Already Exists", "warning")
            pass
            # raise ValidationError("user postoji")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("login")


class UpdateUserForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    # email = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "email"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("UpdatePass")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            pass
        else:
            raise ValidationError("veror")


def level_5_admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_level < 5:
            flash("no access", "warning")
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return decorated_view


def level_4_admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_level < 4:
            flash("no access", "warning")
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return decorated_view


def level_3_admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_level < 3:
            flash("no access", "warning")
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return decorated_view


def level_2_admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_level < 2:
            flash("no access", "warning")
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return decorated_view


def level_1_admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_level < 1:
            flash("no access", "warning")
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return decorated_view


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/snipe_changes", methods=["POST", "GET"])
@login_required
@level_2_admin_required
def snipe_changes():
    # root_path = (sys.path[0] + "/")  # /Users/dpustahija1/PycharmProjects/os-snipe_diff/
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
    # temp = sorted(temp, key=itemgetter('date'), reverse=True) # OLD sort
    temp.sort(key=lambda x: datetime.strptime(x['date'], '%d.%m.%Y'), reverse=True)  # NEW sort

    if request.method == "POST":
        file_name1 = (request.form.get("date1"))[:-5]
        file_name2 = (request.form.get("date2"))[:-5]

        if file_name1 == file_name2:
            flash("Nije moguće izabrati dva ista datuma!", "warning")
        else:
            print(os.getpid())
            diff.Diff(file_name1, file_name2, save_name=save_file_name,
                      save_path="results_cron/diff/excel/").pretty_diffs_xlsx()
            print(diff.Diff(file_name1, file_name2, save_name=save_file_name,
                            save_path="results_cron/diff/excel/"))
            if diff.Diff(file_name1, file_name2, save_name=save_file_name,
                         save_path="results_cron/diff/excel/").check_if_changed() == "0":
                flash("Nema Promjena između zadanih datuma!", "success")
            else:
                print(file_name1, file_name2)
                return redirect(url_for("download", filename=save_file_name + ".xlsx"))

    return render_template('snipe_changes.html', data=temp)


@app.route("/reports", methods=["POST", "GET"])
@login_required
@level_2_admin_required
def reports():
    if request.method == "POST":
        if request.form['submit_button'] == 'in_snipe':
            snipe_sofa_framework.Reports().matching_snipe_and_os_report()
            return redirect(url_for("download", filename=("matching_snipe_and_os_report" + ".xlsx")))

        elif request.form['submit_button'] == 'not_in_snipe':
            snipe_sofa_framework.Reports().non_matching_snipe_and_os_report()
            return redirect(url_for("download", filename=("non_matching_snipe_and_os_report" + ".xlsx")))

        elif request.form['submit_button'] == 'not_in_os':
            snipe_sofa_framework.Reports().rest_in_snipe_report()
            return redirect(url_for("download", filename=("rest_in_snipe_report" + ".xlsx")))

    return render_template("reports.html")


@app.route("/rtd_check", methods=["POST", "GET"])
@login_required
@level_2_admin_required
def rtd_check():
    if request.method == "POST":
        data = json.loads(request.data)  # Parse the JSON data
        print(f"{data:}")
        if data["os_numbers"] != [""]:
            os_numbers = data.get('os_numbers')
            print(os_numbers)
            my_report = snipe_sofa_framework.Reports()
            my_report.non_rtd_assets(os_numbers=os_numbers)
            # return redirect(url_for("download", filename=("non_rtd_assets"+".xlsx")))
            return redirect(url_for("download_report", filename="non_rtd_assets.xlsx"))
        else:
            flash("Nema unosa", "warning")
    return render_template("rtd_check.html")


@app.route("/test", methods=["POST", "GET"])
@login_required
@level_5_admin_required
def test():
    flash("user" + current_user.username, "warning")
    if request.method == "POST":
        print(request.form.get("recordinput"))

    return render_template("test.html")


@app.route('/download/<filename>')
@login_required
def download(filename):
    if filename == "file.xlsx":
        print(os.getpid())
        path = ((root_path + ('results_cron/diff/excel/')) + filename)
    elif filename == "matching_snipe_and_os_report.xlsx":
        path = ((root_path + ('results/matching/')) + filename)
    elif filename == "non_matching_snipe_and_os_report.xlsx":
        path = ((root_path + ('results/non_matching/')) + filename)
    elif filename == "rest_in_snipe_report.xlsx":
        path = ((root_path + ('results/rest/')) + filename)
    return send_file(path, as_attachment=True)


@app.route('/download/report/<filename>')
@login_required
def download_report(filename):
    non_rtd_save_location = os.getenv("export_report_path_rest")
    path = f"{root_path}{non_rtd_save_location}{urllib.parse.unquote(filename)}"
    print(path)
    return send_file(path, as_attachment=True)


@app.route('/download/statement/<filename>')
@login_required
def download_statement(filename):
    save_location = os.getenv("statement_save_location")
    path = root_path + save_location + (urllib.parse.unquote(filename))
    print("path:  ", path)

    return send_file(path, as_attachment=True, mimetype='application/pdf')


@app.route('/snipeit')
def snipeit():
    return redirect("http://10.10.1.54/")


@app.route('/docs')
def docs():
    return redirect("https://snipeit-framework.gitbook.io/snipeit-framework/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("uspješno ulogiran " + user.username, "success")
                return redirect(url_for("index"))
            else:
                flash("kriva lozinka", "warning")
                return redirect(url_for("login"))
        else:
            flash("Korisnik ne postoji", "warning")
            # return redirect(url_for(""))

    return render_template("login.html", form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route('/edit-user', methods=['GET', 'POST'])
@login_required
@level_5_admin_required
def edit_user():
    form = UpdateUserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            user_to_update = User.query.get_or_404(user.id)
            user_to_update.password = hashed_password
            # print(f"{user.id=}")
            try:
                db.session.commit()
                flash("Successfully updated password", "success")
            except:
                flash("Error on updating password", "warning")
        else:
            return None

    return render_template("user_edit.html", form=form)


@app.route('/register', methods=['GET', 'POST'])
@login_required
@level_5_admin_required
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # user = User.query.filter_by(username=form.username.data).first()
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, password=hashed_password, email=form.email.data, user_level=0)
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None:
                db.session.add(new_user)
                db.session.commit()
                flash("User added successfully", "success")
            else:
                flash(f"User {new_user.username} Already Exists", "warning")
                return redirect(url_for("register"))
        else:
            flash("ecdws", "warning")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route('/delete/<int:id>')
@login_required
@level_5_admin_required
def delete(id):
    user_to_delete = User.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("user " + user_to_delete.username + " deleted")
        return redirect(url_for("login"))
    except:
        flash("PROMLEM!")


@app.route('/create-document', methods=['POST'])
def asset_list():
    selected_user_full_name = json.loads(request.form.get("selected_user"))["name"]
    selected_assets = request.form.getlist("selected_assets[]")
    statement_type_option = request.form.getlist("statement_type_option")
    date_of_statement = request.form.get("date_of_statement")
    print(f"{date_of_statement=}")
    print(type(statement_type_option))
    list_of_dicts_of_assets = []
    for item in selected_assets:
        my_dict = {'item': item}
        list_of_dicts_of_assets.append(my_dict)

    if statement_type_option[0] == "zaduzenje":
        name = receipt_statments.Create().zaduzenje(user=selected_user_full_name, items=list_of_dicts_of_assets,
                                                    date=date_of_statement)
        print("name: ", name)
        return redirect(url_for("download_statement", filename=name))

    if statement_type_option[0] == "razduzenje":
        name = receipt_statments.Create().razduzenje(user=selected_user_full_name, items=list_of_dicts_of_assets)
        return redirect(url_for("download_statement", filename=name))

    if statement_type_option[0] == "mob":
        pass
    return {'message': selected_assets}


@app.route('/submit-user', methods=['POST'])
def handle_form_submission():
    if request.form["selected_user"] and request.form.get("for_cards") == "True":
        user_id = json.loads(request.form.get("selected_user"))["id"]
        print(request.form.get("for_cards"))
        assets = snipe_sofa_framework.Snipe().get_checked_out_assets_by_id(user_id)
        for asset_tag in assets:
            if assets[asset_tag]["model"] == "Kartica za ulazak u firmu":
                print(assets[asset_tag])
                temp2 = dict.fromkeys("0")
                temp2["0"] = assets[asset_tag]
        return render_template("card_list.html", data2=temp2)
    if request.form["selected_user"] and request.form.get("for_cards") == "False":
        user_id = json.loads(request.form.get("selected_user"))["id"]

        temp2 = snipe_sofa_framework.Snipe().get_checked_out_assets_by_id(user_id)
        return render_template("assets_list.html", data2=temp2)
    else:
        pass


@app.route('/statements', methods=["POST", "GET"])
@login_required
@level_3_admin_required
def statements():
    temp = snipe_sofa_framework.Snipe().statement_user_data()
    temp2 = {}
    statement_type = [{'type': "mob", 'name': "Izjava o zaduženju mobitela"},
                      {'type': "zaduzenje", 'name': "Izjava o zaduženju opreme"},
                      {'type': "razduzenje", 'name': "Izjava o razduženju opreme"}]
    temp = dict(sorted(temp.items(), key=lambda x: x[1]['name']))
    # temp = {245: {'id': 245, 'username': 'ihrzina', 'name': 'Ivana Hržina', 'assets_count': 4}, 244: {'id': 244, 'username': 'edabo', 'name': 'Elizabeta Dabo', 'assets_count': 4}, 243: {'id': 243, 'username': 'nmehes', 'name': 'Nikola Meheš', 'assets_count': 5}, 242: {'id': 242, 'username': 'mgerm', 'name': 'Mario Germ', 'assets_count': 5}, 241: {'id': 241, 'username': 'tharamustek', 'name': 'Tomislav Haramustek', 'assets_count': 4}}
    # if request.method == "POST":

    return render_template("statements.html", data=temp, data2=temp2, statment_type=statement_type)


@app.route('/update-card', methods=['POST', "GET"])
@login_required
@level_3_admin_required
def update_card():
    temp = snipe_sofa_framework.Snipe().statement_user_data()
    temp = dict(sorted(temp.items(), key=lambda x: x[1]['name']))
    if request.is_json:
        card_data = request.json.get("card_data")
        if card_data:
            card_asset_tag = card_data.get("asset_tag")
            card_hex = card_data.get("hex")
            card_dec = card_data.get("dec")
            if card_asset_tag and card_hex and card_dec:
                print(f"{card_asset_tag=}{card_dec=}{card_hex=}")
                snipe_sofa_framework.Update(asset_tag=card_asset_tag).set_card_dec(card_dec=card_dec)
                snipe_sofa_framework.Update(asset_tag=card_asset_tag).set_card_hex(card_hex=card_hex)
                # Process the card data as needed
                return jsonify({"message": "Card data received successfully and updated Snipe-IT"})
            else:
                return jsonify({"message": "ERROR: MISSING DATA "})
    return render_template("update_card.html", data=temp)


@app.route('/update-assets', methods=["POST", "GET"])
@login_required
@level_5_admin_required
def update_assets():
    if request.method == "POST":
        data = request.json
        print(f"{data=}")
        for item in data:
            for key, value in item.items():
                if value == '':
                    return f"Empty string found in {key} of {item}"
            if snipe_sofa_framework.Check().is_asset_tag_valid(item['asset_tag']):
                snipe_sofa_framework.Update(asset_tag=item['asset_tag']).set_os_number(os_number=item['os_number'])
            else:
                snipe_sofa_framework.Update(asset_tag=f"0{item['asset_tag']}").set_os_number(
                    os_number=item['os_number'])
            if item["ZOPU"]:
                snipe_sofa_framework.Update(asset_tag=item['asset_tag']).set_zopu()
            else:
                print("nije true")
            # return "1"

        return "Data received."

    return render_template("update_assets.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
