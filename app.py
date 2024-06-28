from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

os.makedirs('files', exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        filename = request.form['filename']
        text = request.form['textbox']
        with open(f'files/{filename}', 'w') as file:
            file.write(text)
        return redirect(url_for('index'))

    files = os.listdir('files')

    return render_template('index.html', files=files)

@app.route('/edit/<filename>', methods=['GET', 'POST'])
def edit(filename):
    filepath = f'files/{filename}'
    if request.method == 'POST':
        text = request.form['textbox']
        with open(filepath, 'w') as file:
            file.write(text)
        return redirect(url_for('index'))

    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            saved_text = file.read()
    else:
        saved_text = ""

    return render_template('edit.html', filename=filename, saved_text=saved_text)

if __name__ == '__main__':
    app.run(debug=True)
