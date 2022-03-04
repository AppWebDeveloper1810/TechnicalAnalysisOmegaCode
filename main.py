import pprint
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import *

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#TABLE
class User(UserMixin, db.Model):  # Creates Table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250))
    password = db.Column(db.String(250), nullable=False)
    plan = db.Column(db.String(250), nullable=False)


db.create_all()


@app.route('/')
def home_page():
    return render_template("home.html")


@app.route('/log_up', methods=["GET", "POST"])
def log_up_page():
    form = SignUp()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first() != None:  # Checks if there is an email in the database which is same as the email entered by the user
            return render_template("wrong_sign_up.html")
        else:  # If user input email does not match the email of an email in the database
            hashed_and_salted_password = generate_password_hash(
                password=form.password.data,
                method='pbkdf2:sha256',
                salt_length=10
            )
            print(f"Sign Up Password: {hashed_and_salted_password}")
            new_user = User(name=form.name.data,
                               email=form.email.data,
                               password=hashed_and_salted_password,
                               plan="NONE")
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)  #  # Log in and authenticate user after adding details to database.
            return redirect(url_for("log_in_page"))
    return render_template("sign_up.html", form=form)


@app.route('/log_in', methods=["GET", "POST"])
def log_in_page():
    form = SignIn()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first() != None:  # Checks if email in the database if true continues
            user = User.query.filter_by(email=form.email.data).first()
            print(user.password)
            print(f"Sign In Password: {form.password.data}")
            if check_password_hash(user.password, form.password.data):  # Checks if password in the database if true continues
                login_user(user)
                print("ooh")
                return redirect(url_for("personal_page", user_email=user.email))  # Could also pass form.email.data in user_email parameter
            else:
                return render_template("wrong_sign_in.html")
        else:
            return render_template("wrong_sign_in.html")

    return render_template("sign_in.html", form=form)


@app.route('/personal_page/<user_email>', methods=["GET", "POST"])
@login_required
def personal_page(user_email):
    user = User.query.filter_by(email=user_email).first()
    color = [[]]
    if user.plan == "NONE":
        color[0] = ["white", "white", "white"]
    elif user.plan == "BASIC":
        color[0] = ["#28f7bc", "white", "white"]
    elif user.plan == "HACKER":
        color[0] = ["white", "white", "#28f7bc"]
    elif user.plan == "PRO":
        color[0] = ["white", "#28f7bc", "white"]
    return render_template("personal_page.html", a=color[0], user=user)


@app.route('/upgrade/<email>', methods=["GET", "POST"])
@login_required
def upgrade_page(email):
    upgrade_form = UpgradeForm()
    user = User.query.filter_by(email=email).first()
    plan_data = str(upgrade_form.plan.data)
    color = [[]]
    if user.plan == "BASIC":
        color[0] = ["#28f7bc", "white", "white"]
    elif user.plan == "HACKER":
        color[0] = ["white", "white", "#28f7bc"]
    elif user.plan == "PRO":
        color[0] = ["white", "#28f7bc", "white"]
    if upgrade_form.validate_on_submit():
        if plan_data.upper() == user.plan:
            return render_template("return_upgrades_or_password.html", message="Seems like you selected the plan you already have.")
        else:
            if plan_data.upper() == "BASIC":
                user.plan = "BASIC"
                db.session.commit()
                return render_template("return_upgrades_or_password.html", message="Upgraded to BASIC plan")
            elif plan_data.upper() == "PRO":
                user.plan = "PRO"
                db.session.commit()
                return render_template("return_upgrades_or_password.html", message="Upgraded to PRO plan")
            elif plan_data.upper() == "HACKER":
                user.plan = "HACKER"
                db.session.commit()
                return render_template("return_upgrades_or_password.html", message="Upgraded to HACKER plan")
            else:
                return render_template("return_upgrades_or_password.html", message="Looks like there is a spelling mistake in your input.")
    return render_template("upgrade.html", user=user, form=upgrade_form)


@app.route('/change_password/<email>', methods=["GET", "POST"])
@login_required
def change_password(email):
    change_password_form = ChangePasswordForm()
    if change_password_form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        if change_password_form.current_password.data == user.password:
            user.password = change_password_form.new_password.data
            db.session.commit()
            return render_template("return_upgrades_or_password.html", message="Successfully changed the password")
        else:
            return render_template("return_upgrades_or_password.html", message="Looks likes your password was wrong.")
    return render_template('change_password.html', form=change_password_form)


@app.route('/logout')
@login_required
def log_out():
    logout_user()
    return redirect(url_for('home_page'))


@app.route('/database/<secret_key>')
def database(secret_key):
    if secret_key == "1":
        a = db.session.query(User).all()
        database = []
        for i in a:
            database.append([i.id, i.name, i.email, i.password, i.plan])
        return jsonify(data=database)
    else:
        return jsonify(error="Sorry, you did not give the right secret key")


@app.route('/clear-database/<secret_key>')
def clear_database(secret_key):
    if secret_key == "1":
        a = db.session.query(User).all()
        for i in a:
            db.session.delete(i)
            db.session.commit()
        return "Successfully Cleared The Database"


@app.route('/screen', methods=["GET", "POST"])
@login_required
def screen_page():
    from analyse import run_analyzation
    screening_message = run_analyzation()
    return render_template("screen_page.html", message=screening_message)

if __name__ == "__main__":
    app.run(debug=True)
