import os
from os import path

from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

import check_domain_expiration
import config


app = Flask(__name__)
# app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + config.db_username + ":" + config.db_password + "@localhost/" + config.db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class Domain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    expire_status = db.Column(db.Boolean)
    expire_date = db.Column(db.Date)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Domain %r>' % self.name

def save_domain(data):
    row = Domain.query.filter_by(name=data.get('name')).first()

    if row:
        row.expire_status = data.get('expire_status')
        row.expire_date = data.get('expire_date')
        row.email = data.get('email')

        db.session.commit()
    else:
        domain = Domain(data.get('name'))
        domain.expire_status = data.get('expire_status')
        domain.expire_date = data.get('expire_date')
        domain.email = data.get('email')

        db.session.add(domain)
        db.session.commit()


@app.route("/")
def index():
    domains = Domain.query.all()

    return render_template('index.html', domains=domains)

@app.route("/_domain_check")
def domain_check():
    domains = request.args.get('domains').split("\n")

    data = []
    for domain in domains:
        expire_date = check_domain_expiration.check(domain)
        if expire_date != "Wrong Format":
            save_domain({'name': domain, 'expire_date': expire_date})

        data.append({'name': domain, 'expire_date': expire_date})

    return jsonify(data)


if __name__ == "__main__":
    extra_dirs = [os.path.join(os.getcwd(), 'templates')]
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in os.walk(extra_dir):
            for filename in files:
                filename = path.join(dirname, filename)
                if path.isfile(filename):
                    extra_files.append(filename)

    db.create_all()
    app.run(host='0.0.0.0', extra_files=extra_files)