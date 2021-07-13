from flask import Flask, flash, render_template, request, redirect
import csv
from incomlete_form_exception import IncompleteFormException

app = Flask(__name__)
app.secret_key = 'Some key to work with sessions'


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/<string:page>')
def single_page(page=None):
    if not page:
        return render_template('index.html')
    return render_template(page)


def write_form_submittion(data):
    with open('database.csv', mode='a') as database:
        email = data['email']
        subject = data['subject']
        message = data['message']
        if not (email and (subject or message)):
            raise IncompleteFormException('empty-form')
        csv_writer = csv.writer(database, delimiter=',', quoting=csv.QUOTE_MINIMAL, quotechar='"')
        csv_writer.writerow([email, subject, message])


@app.route('/submit_contact_form', methods=['POST'])
def submit_contact_form():
    try:
        data = request.form.to_dict()
        write_form_submittion(data)
        flash('Thanks for your message, I`ll answer it as soon as possible!', 'contact_submit_success')
    except IncompleteFormException:
        flash('Please fill email and subject or message :)', 'contact_submit_error')
    except:
        flash('Oops, something went wrong :( Please try to contact me on social networks.', 'contact_submit_error')
    finally:
        return redirect('/contact.html')
