from flask import Flask, escape, render_template, request, redirect, url_for
import data_manager
import util

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def list_route():
    title = 'Ask mate'
    questions = data_manager.get_all_questions()
    return render_template('list_question.html', questions=questions, title=title)


@app.route('/question', defaults={'question_id': None})
@app.route('/question/<int:question_id>')
def question_route(question_id):
    exsiting_ids = data_manager.get_question_ids()
    if question_id not in exsiting_ids:
        return redirect('/')

    post = data_manager.get_question_by_id(question_id)
    post_data = 0

    answers_dict = data_manager.get_all_sorted_answers(question_id)
    id_tuple = data_manager.get_answers_ids(question_id)

    if len(id_tuple) < 1:
        id_tuple = (-1,)

    question_comments_dict = data_manager.get_question_comments(question_id)
    answer_commnets_dict = data_manager.get_answer_coments(id_tuple)

    return render_template('question_page.html', post=post[post_data],
                           answers=answers_dict, question_id=question_id,
                           question_comments=question_comments_dict,
                           answer_comments=answer_commnets_dict)


@app.route('/add-question', methods=['POST', 'GET'])
def add_question_route():
    if request.method == 'GET':
        return render_template('ask_question.html')
    else:
        title = escape(request.form['title'])
        msg = escape(request.form['message'])
        data_manager.add_new_question(title, msg)
        question_id = data_manager.find_max_id()
        return redirect(url_for('question_route', question_id=question_id))


@app.route('/question/<int:question_id>/new-answer', methods=['POST', 'GET'])
def answer_route(question_id=None):
    if request.method == 'GET':
        title = 'Add answer - Ask mate'
        return render_template('add_answer.html', question_id=question_id, title=title)
    else:
        msg = escape(request.form['answer-msg'])
        quest_id = escape(request.form['id'])
        data_manager.add_new_answer(msg, quest_id)
        return redirect(url_for('question_route', question_id=question_id))


@app.route('/question/<question_id>/new-comment', methods=['POST', 'GET'])
def question_comment_route(question_id=None):
    if request.method == 'GET':
        title = 'Add coment to question - Ask mate'
        return render_template('question_comment.html', question_id=question_id, title=title)
    else:
        comment_message = request.form['comment-msg']
        data_manager.insert_question_comment(question_id, comment_message)
        return redirect(url_for('question_route', question_id=question_id))


@app.route('/answer/<question_id>/<answer_id>/new-comment', methods=['POST', 'GET'])
def answer_comment_route(answer_id=None, question_id=None):
    if request.method == 'GET':
        title = 'Add coment to answer - Ask mate'
        return render_template('answer_comment.html', answer_id=answer_id,
                               question_id=question_id, title=title)
    else:
        question_id = request.form['question_id']
        comment_message = request.form['comment-msg']
        data_manager.insert_answer_comment(answer_id, comment_message)
        return redirect(url_for('question_route', question_id=question_id))


@app.errorhandler(404)
def page_404(e):
    return render_template('error_404_page.html'), 404
#


if __name__ == '__main__':
    app.run(
        debug=True,
        port=8000
    )
