import pickle
import uuid
from os.path import isfile

from flask import Flask, render_template, request, session, redirect, url_for


app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'ei$tiq5(=k&q=6pzm(j0mk8otxvus1+u!y#g-iu1i7a+r7aqt^'



def write_to_articles_db(dict_data):
    pickle_filepath = 'data.pickle'
    if not isfile(pickle_filepath):
        data_from_pickle = dict_data
    else:
        data_from_pickle = load_from_articles_db()
        data_from_pickle.update(dict_data)
    with open(pickle_filepath, 'wb+') as file_handler:
        pickle.dump(data_from_pickle, file_handler, pickle.HIGHEST_PROTOCOL)


def load_from_articles_db():
    pickle_filepath = 'data.pickle'
    with open(pickle_filepath, 'rb') as file_handler:
        return pickle.load(file_handler)


@app.route('/', methods = ['POST', 'GET'])
def form():
    if request.method == 'POST':
        unique_key = str(uuid.uuid4())
        article_data = {unique_key : {
            'header': request.form['header'],
            'signature': request.form['signature'],
            'body': request.form['body'],
        }}
        write_to_articles_db(article_data)
        return redirect(
            '{article_key}'.format(article_key=unique_key)
        )

    return render_template('form.html')


@app.route('/<post_key>', methods = ['POST', 'GET'])
def show_post(post_key):
    if request.method == 'POST':
        article_data = {post_key : {
            'header': request.form['header'],
            'signature': request.form['signature'],
            'body': request.form['body'],
        }}
        write_to_articles_db(article_data)

    data_from_pickle = load_from_articles_db()
    return render_template('form.html', article=data_from_pickle.get(post_key))


@app.route('/hello')
def hello():
    return 'hello'

if __name__ == "__main__":
    # a = load_from_articles_db()
    # print(a.get('09e550e4-5d57-4b94-9036-3ea6af84da52'))
    app.run()
