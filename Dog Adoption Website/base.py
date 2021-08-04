import os
from flask import Flask,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from form import AddForm,DelForm,AddOwner

app=Flask(__name__)
app.config['SECRET_KEY']='mykey'


basedir=os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
Migrate(app,db)

class Puppy(db.Model):
    __tablename__='puppies'
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)
    owner=db.relationship('Owner',backref='Puppy',uselist=False)
    def __init__(self,name):
        self.name=name
    def __repr__(self):
        if self.owner:
            return f"The puppy name is {self.name} and its owner name is {self.owner.item_name}"
        else:
            return f"The puppy name is {self.name} and it has no owner"
class Owner(db.Model):
    __tablename__='owner'
    id=db.Column(db.Integer,primary_key=True)
    item_name=db.Column(db.Text)
    puppy_id=db.Column(db.Integer,db.ForeignKey('puppies.id'))
    def __init__(self,item_name,puppy_id):
        self.item_name=item_name
        self.puppy_id=puppy_id
    def __repr__(self):
        return f"The Name of the owner is: {self.item_name}"

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add', methods=['GET','POST'])
def add():
    form= AddForm()
    if form.validate_on_submit():
        pup=form.name.data
        puppy=Puppy(pup)
        db.session.add(puppy)
        db.session.commit()
        return redirect(url_for('list'))
    return render_template('add.html',form=form)

@app.route('/list')
def list():
    pups=Puppy.query.all()
    return render_template('list.html',pups=pups)

@app.route('/delete',methods=['GET','POST'])
def delete():
    form=DelForm()
    if form.validate_on_submit():
        id=form.id.data
        pup=Puppy.query.get(id)
        db.session.delete(pup)
        db.session.commit()
        return redirect(url_for('list'))
    return render_template('delete.html',form=form)

@app.route('/addowner',methods=['GET','POST'])
def addowner():
    form=AddOwner()
    if form.validate_on_submit():
        oname=form.item_name.data
        oid=form.puppy_id.data
        new_owner=Owner(oname,oid)
        db.session.add(new_owner)
        db.session.commit()
        return redirect(url_for('list'))
    return render_template('addowner.html',form=form)

if __name__=='__main__':
    app.run(debug=True)
