from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        data = request.json

        if data and data.get('lottoNumbers') == data.get('numbers'):
            with open("flag", 'r') as file:
                flag = file.read().strip()

            return flag
        else:
            return "Wrong numbers."

if __name__ == '__main__':
    app.run()
