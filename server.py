from flask import Flask, escape, render_template, request, redirect, url_for
import data_manager
import util

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def list_route():
    questions = data_manager.get_all_questions()
    sorted_titles = util.sort_by_time_submission(questions)
    return render_template('list-questions.html', questions=sorted_titles)


@app.route('/question', defaults={'question_id': None})
@app.route('/question/<int:question_id>')
def question_route(question_id):
    if question_id is None:
        return redirect('/')
    post = data_manager.get_question_by_id(question_id)
    post['submission_time'] = util.convert_timestamp_to_date(post['submission_time'])
    answers = data_manager.get_all_answers()
    return render_template('question-page.html', post=post, answers=answers)


@app.route('/add-question', methods=['POST', 'GET'])
def add_question_route():
    if request.method == 'GET':
        return render_template('question-edit-page.html')
    else:
        title = escape(request.form['title'])
        msg = escape(request.form['message'])
        question_id = data_manager.add_new_question(title, msg)
        print(msg)
        return redirect(url_for('question_route', question_id=question_id))


if __name__ == '__main__':
    app.run(
        debug=True,
        port=8000
    )

