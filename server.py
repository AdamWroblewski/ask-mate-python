from flask import Flask, render_template, request, redirect
import data_manager

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def list_route():
    titles = data_manager.get_post_title()
    return render_template('list-questions.html', titles=titles)


if __name__ == '__main__':
    app.run(
        debug=True,
        port=8000
    )
