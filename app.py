from flask import Flask, render_template, request, redirect
import uuid
import datetime

app = Flask(__name__, static_folder='static')

data = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        unique_id = str(uuid.uuid4())[:8]
        expiration = datetime.datetime.now() + datetime.timedelta(hours=1)
        data[unique_id] = {'text': text, 'expiration': expiration}
        return redirect(f'/{unique_id}')
    return render_template('index.html')

@app.route('/<unique_id>')
def display_text(unique_id):
    if unique_id in data:
        if datetime.datetime.now() < data[unique_id]['expiration']:
            text = data[unique_id]['text']
            return render_template('display.html', text=text)
        else:
            del data[unique_id]
            return "Link has expired"
    return "Invalid URL"

if __name__ == '__main__':
    app.run()