from flask import Flask, render_template

app = Flask(__name__)


def get_films():
    return [
        {
            'id': 1,
            'title': 'Film name!!',
            'release_date': '12.31'
        },
        {
            'id': 2,
            'title': 'Film name TWO',
            'release_date': '1999'
        },
    ]


@app.route("/")
@app.route("/hello")
def index():
    films = get_films()
    return render_template('hello.html', films=films)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/<string:name>")
def greeting(name: str):
    return f'<h1>Привет, {name.capitalize()}!</h1>'


if __name__ == '__main__':
    app.run()
