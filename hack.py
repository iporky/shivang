from flask import Flask, request, jsonify
# from flask import redirect, url_for, render_template
# import spacy
# import nltkGenismCleanModel
# import nltkGenism
import operations
from flask import send_file
# import pandas as pd


app = Flask(__name__)
# nlp = spacy.load('en_core_web_md')
# nltkGenismCleanModel.buildModel()
# df = pd.read_excel('Helpdesk_Report_part_cleaned_final.xlsx')
# dataoutput = df["Close notes"].tolist()

# @app.route('/')
# def index():
#   return render_template('text.html')


@app.route('/suggestions/get', methods=['post'])
def getSuggestions():
    data = request.get_json()
    return jsonify(operations.getSuggestions(data["desc"]))


@app.route('/upsuggestions', methods=["post"])
def putSuggestions():
    data = request.get_json()
    operations.addVotedResult(data["desc"], data["close_note"])
    return jsonify("success")


@app.route('/upsuggestions/addnote', methods=["post"])
def putNotes():
    data = request.get_json()
    note_id = operations.addNote(data["id"], data["note"])
    return jsonify(note_id)


@app.route('/upsuggestions/removeticket', methods=["post"])
def removeTicket():
    data = request.get_json()
    operations.removeTicket(data["id"])
    return jsonify("success")


@app.route('/upsuggestions/updateclousurenote', methods=["post"])
def putCloseNotes():
    data = request.get_json()
    operations.updateClosureNote(data["id"], data["close_note"])
    return jsonify("success")


@app.route('/upsuggestions/addticket', methods=["post"])
def putTicket():
    data = request.get_json()
    operations.addTicket(data["issue"], data["closureNote"])
    return jsonify("success")


@app.route('/upsuggestions/addfile', methods=["post"])
def putFileName():
    data = request.get_json()
    atc_id = operations.addfile(data["id"], data["fileName"], data["uuid"])
    return jsonify(atc_id)


if __name__ == '__main__':
    app.run(debug=True)
