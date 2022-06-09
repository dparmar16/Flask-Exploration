from flask import Flask, render_template, url_for
#from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Table, Column, String, Integer, Float, MetaData
#from datetime import datetime
import csv
import numpy as np

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# db = SQLAlchemy(app)
#
# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable=False)
#     completed = db.Column(db.Integer, default=0)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)
#
#     def __repr__(self):
#         return 'Task %r' % self.id


# @app.route('/')
# def index():
#     return render_template('index.html')

engine = create_engine('sqlite:///life-expectancy.db', echo=True)
metadata_object = MetaData()
life_expectancy_table = Table('life_expectancy_table', metadata_object,
                              Column('Entity', String),
                              Column('Code', String),
                              Column('Year', Integer),
                              Column('Estimate', Float),
                              Column('Interpolation', Float))

metadata_object.create_all(engine)
insert_query = life_expectancy_table.insert()

with open('life-expectancy-at-birth-including-the-un-projections.csv',
          'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader, None) # Use iterator to skip header line
    engine.execute(insert_query,
                   [{'Entity': row[0],
                     'Code': row[1],
                     'Year': row[2],
                     'Estimate': np.where(row[3] == '', np.NaN, row[3]),
                     'Interpolation': np.where(row[4] == '', np.NaN, row[4])} for row in csv_reader])


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///life-expectancy.db'

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)