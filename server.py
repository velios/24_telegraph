import json
import uuid
from os.path import isfile
from argparse import ArgumentParser

from flask import Flask, render_template, request, session, redirect


app = Flask(__name__)
app.secret_key = 'ei$tiq5(=k&q=6pzm(j0mk8otxvus1+u!y#g-iu1i7a+r7aqt^'


def make_cmd_arguments_parser():
    parser_description = 'Run flask server'
    parser = ArgumentParser(description=parser_description)
    parser.add_argument('-d', '--debug_mode',
                        help='Run in debug mode',
                        action='store_true')
    return parser


def load_from_articles_db(filepath='data.json'):
    articles_data = {}
    if not isfile(filepath):
        with open(filepath, mode='w') as file_handler:
            file_handler.write(json.dumps(articles_data, indent=2))
    else:
        with open(filepath) as file_handler:
            articles_data = json.load(file_handler)
    return articles_data


def write_to_articles_db(dict_data, filepath='data.json'):
    articles_data = load_from_articles_db()
    with open(filepath, mode='w') as file_handler:
        articles_data.update(dict_data)
        file_handler.write(json.dumps(articles_data, indent=2))


@app.before_request
def make_session():
    session.permanent = True
    unique_key = str(uuid.uuid4())
    if not session.get('key'):
        session['key'] = unique_key


@app.route('/', methods = ['POST', 'GET'])
def form():
    if request.method == 'POST':
        unique_key = str(uuid.uuid4())
        article_data = {unique_key: {
            'header': request.form['header'],
            'signature': request.form['signature'],
            'body': request.form['body'],
            'session': session.get('key')
        }}
        write_to_articles_db(article_data)
        return redirect(unique_key)
    return render_template('form.html')


@app.route('/<post_key>', methods = ['POST', 'GET'])
def show_post(post_key):
    session_key = session.get('key')
    data_from_json = load_from_articles_db()
    if request.method == 'POST':
        current_post_data = data_from_json.get(post_key)
        current_post_data['header'] = request.form['header']
        current_post_data['signature'] = request.form['signature']
        current_post_data['body'] = request.form['body']
        write_to_articles_db(data_from_json)

    article_data = data_from_json.get(post_key)
    template4render = 'form.html' if article_data.get('session') == session_key else 'article.html'
    return render_template(template4render, article=article_data)


if __name__ == "__main__":
    cmd_args_parser = make_cmd_arguments_parser()
    cmd_args = cmd_args_parser.parse_args()
    if cmd_args.debug_mode:
        app.config['DEBUG'] = True
    app.run()
