from flask import Blueprint, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from .models import Admin, Note, User
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/lounge', methods=['GET', 'POST'])
@login_required
def lounge():
    
    return render_template("lounge.html", user=current_user)


@views.route('/admin-dashboard', methods=['GET'])
@login_required
def admin_dashboard():
    if not isinstance(current_user, Admin):
        flash('You must be an admin to access this page.', category='error')
        #return redirect(url_for('auth.admin_login'))
        users = User.query.all()  # Query all users to display in the admin dashboard
        return render_template("admin-dashboard.html", user=current_user, users=users)
    users = User.query.all()  # Query all users to display in the admin dashboard
    return render_template("admin-dashboard.html", user=current_user, users=users)



@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})