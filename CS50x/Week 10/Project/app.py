from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)

notes = []

@app.route('/')
def index():
    return render_template('index.html', notes=notes)

@app.route('/history')
def history():
    return render_template('history.html', notes=notes)

@app.route('/index', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        note_name = request.form.get('name')
        note_text = request.form.get('note')
        if note_text:
            note = {
                'name': note_name,
                'note': note_text,
                'date': datetime.now()
            }
            notes.append(note)
        return redirect('/history')
    else:
        return redirect('/')
