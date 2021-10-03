import os
from zipfile import ZipFile
from os.path import basename
import shutil
from evaluation_server import *

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_file
)

bp = Blueprint('/', __name__, url_prefix='/')

input_dir = "static/input/"
output_dir = "static/output/"
os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

input_path = input_dir + 'input.pickle'
output_path = output_dir + 'output.csv'

example_input_path = 'static/example/final_mcpas_neg_mhc_2206_train_samples.pickle'


@bp.route('/Home', methods=('GET', 'POST'))
def home_page():
    error = None

    if request.method == 'POST':

        input_file = request.files['input_file']

        if not input_file:
            error = 'Missing input file.'

        input_file.save(input_path)
        df = run(input_path)
        df.to_csv(output_path)

        flash(error)

        if not error:
            return render_template('home.html', active='Home', output_flag=1, input_file=input_file)

    return render_template('home.html', active='Home')


@bp.route('/Help')
def help_page():
    return render_template('help.html', active='Help')


@bp.route('/Example')
def example_page():
    return render_template('example.html', active='Example')


@bp.route('/About')
def about_page():
    return render_template('about.html', active='About')


@bp.route('/download-outputs')
def download():
    return send_file(output_path, mimetype='csv', as_attachment=True, )


@bp.route('/download-example-files')
def download_example():
    return send_file(example_input_path, mimetype='pickle', as_attachment=True, )
