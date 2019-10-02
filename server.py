from flask import Flask, render_template, request, redirect
import data_manager
import util

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def list_route():
    questions = data_manager.get_all_questions()
    sorted_titles = util.sort_by_time_submission(questions)
    return render_template('list-questions.html', questions=sorted_titles)


@app.route('/question/<question_id>')
def question_route(question_id=None):
    return render_template('question-page.html')


if __name__ == '__main__':
    app.run(
        debug=True,
        port=8000
    )
