import json
import uuid
from os.path import isfile
from argparse import ArgumentParser

from flask import Flask, render_template, request, session, redirect


app = Flask(__name__)
app.secret_key = 'ei$tiq5(=k&q=6pzm(j0mk8otxvus1+u!y#g-iu1i7a+r7aqt^'


def fetch_cmd_arguments():
    parser_description = 'Run flask server'
    parser = ArgumentParser(description=parser_description)
    parser.add_argument('-d', '--debug_mode',
                        help='Run in debug mode',
                        action='store_true')
    return parser.parse_args()


def load_data_from_articles_json(filepath='data.json'):
    with open(filepath) as file_handler:
        return json.load(file_handler)


def update_articles_json(dict_data, filepath='data.json'):
    articles_data = load_data_from_articles_json()
    with open(filepath, mode='w') as file_handler:
        articles_data.update(dict_data)
        file_handler.write(json.dumps(articles_data, indent=2))


@app.before_request
def make_session():
    session.permanent = True
    if 'key' not in session:
        unique_key = str(uuid.uuid4())
        session['key'] = unique_key


@app.route('/', methods = ['POST', 'GET'])
def form():
    if request.method == 'POST':
        article_id = str(uuid.uuid4())
        article_data = {article_id: {
            'header': request.form['header'],
            'signature': request.form['signature'],
            'body': request.form['body'],
            'session': session['key']
        }}
        update_articles_json(article_data)
        return redirect(article_id)
    return render_template('form.html')


@app.route('/<post_key>', methods = ['POST', 'GET'])
def show_post(post_key):
    data_from_json = load_data_from_articles_json()
    article_data = data_from_json.get(post_key)
    if not article_data:
        return render_template('not_found.html')
    if request.method == 'POST':
        current_post_data = data_from_json.get(post_key)
        current_post_data['header'] = request.form['header']
        current_post_data['signature'] = request.form['signature']
        current_post_data['body'] = request.form['body']
        update_articles_json(data_from_json)
    template4render = 'form.html' if article_data['session'] == session['key'] else 'article.html'
    return render_template(template4render, article=article_data)


def initialize_article_json(filepath='data.json'):
    if not isfile(filepath):
        with open(filepath, 'w') as file_handler:
            empty_dict = {}
            json.dump(empty_dict, file_handler)


if __name__ == "__main__":
    cmd_args = fetch_cmd_arguments()
    initialize_article_json()
    if cmd_args.debug_mode:
        app.config['DEBUG'] = True
    app.run()
