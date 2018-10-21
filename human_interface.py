from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def a():
    if request.method == 'POST':
        name = request.form['app_name']
        print(name)
    return render_template("a.html")

@app.route('/wca')
def hello():
    return render_template("test.html")

if __name__ == "__main__":
    app.run(debug=True)