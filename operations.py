import spacy
import pandas as pd
import numpy as np
from spacy.matcher import Matcher
from spacy.tokens import Doc
from PyPDF2 import PdfFileReader
# import slate3k as slate
import dbInteraction
import cx_Oracle


def OutputTypeHandler(cursor, name, defaultType, size, precision, scale):
    if defaultType == cx_Oracle.CLOB:
        return cursor.var(cx_Oracle.LONG_STRING, arraysize=cursor.arraysize)


pool = dbInteraction.connect_db()
connection= pool.acquire()
connection.outputtypehandler = OutputTypeHandler
cursor = connection.cursor()

df = dbInteraction.select_doc_all(cursor)
category_df = dbInteraction.select_cat_all(cursor)
app_df = dbInteraction.select_app_all(cursor)
note_df = dbInteraction.select_note_all(cursor)
atc_df = dbInteraction.select_atc_all(cursor)

df.columns = ['DOC_ID', 'Ticket Description', 'Ticket Closure notes']
category_df.columns = ["category"]
app_df.columns = ['name', 'fullname']
if len(note_df) != 0:
    note_df.columns = ['NOTE_ID', 'NOTE_TEXT', 'DOC_ID']
    groupByNote = note_df.groupby('DOC_ID')
if len(atc_df) != 0:
    atc_df.columns = ['ATC_ID', 'ATC_NAME', 'DOC_ID', 'UUID']
    groupByAtc = atc_df.groupby('DOC_ID')

unprocessed_docs = []
sampleDocs = []

for index in df.index:
    if (len(note_df) > 0 and df["DOC_ID"][index] in list(note_df.DOC_ID)) and (len(atc_df) > 0 and df["DOC_ID"][index] in list(atc_df.DOC_ID)):
        note_dict = groupByNote.get_group(df["DOC_ID"][index]).to_dict("list")
        text = df["Ticket Description"][index] + ' '.join(note_dict['NOTE_TEXT'])
        atc_dict = groupByAtc.get_group(df["DOC_ID"][index]).to_dict("list")
        context = {"id": int(df["DOC_ID"][index]), "closure_note": df["Ticket Closure notes"][index],
                   "desc": df["Ticket Description"][index], "notes": note_dict, "attachments": atc_dict}
    elif len(atc_df) > 0 and df["DOC_ID"][index] in list(atc_df.DOC_ID):
        atc_dict = groupByAtc.get_group(df["DOC_ID"][index]).to_dict("list")
        context = {"id": int(df["DOC_ID"][index]), "closure_note": df["Ticket Closure notes"][index],
                   "desc": df["Ticket Description"][index], "notes": {}, "attachments": atc_dict}
    elif len(note_df) > 0 and df["DOC_ID"][index] in list(note_df.DOC_ID):
        note_dict = groupByNote.get_group(df["DOC_ID"][index]).to_dict("list")
        text = df["Ticket Description"][index] + ' '.join(note_dict['NOTE_TEXT'])
        context = {"id": int(df["DOC_ID"][index]), "closure_note": df["Ticket Closure notes"][index],
                   "desc": df["Ticket Description"][index], "notes": note_dict, "attachments": {}}
    else:
        text = df["Ticket Description"][index]
        context = {"id": int(df["DOC_ID"][index]), "closure_note": df["Ticket Closure notes"][index],
                   "desc": df["Ticket Description"][index], "notes": {}, "attachments": {}}
    unprocessed_docs.append((text, context))

nlp = spacy.load('en_vectors_web_lg')

category_list = []
for i in range(0, len(category_df)):
    category_list.append(nlp(str(category_df['category'][i])))

matcher = Matcher(nlp.vocab)

appMap = {}
for i in range(0, len(app_df)):
    appMap[str(app_df['fullname'][i])] = str(app_df['name'][i])

matcher.add("Application", None,
            [{"LOWER": "sps"}],
            [{"LOWER": "drb"}],
            [{"LOWER": "nms"}],
            [{"LOWER": "cert"}],
            [{"LOWER": "dwb"}],
            [{"LOWER": "dd"}],
            [{"LOWER": "dp"}],
            [{"LOWER": "dr"}],
            [{"LOWER": "dsr"}],
            [{"LOWER": "epex"}],
            [{"LOWER": "hpas"}],
            [{"LOWER": "qem"}],
            [{"LOWER": "dti"}],
            [{"LOWER": "dte"}, {"LOWER": "discover"}],
            [{"LOWER": "departure"}, {"LOWER": "record"}],
            [{"LOWER": "dp"}, {"LOWER": "systems"}],
            [{"LOWER": "dr"}, {"LOWER": "systems"}],
            [{"LOWER": "drb"}, {"LOWER": "systems"}],
            [{"LOWER": "laws"}, {"LOWER": "fa"}],
            [{"LOWER": "repair"}, {"LOWER": "docs"}],
            [{"LOWER": "aapi"}],
            [{"LOWER": "dax"}],
            [{"LOWER": "significant"}, {"LOWER": "process"}, {"LOWER": "substantiation"}],
            [{"LOWER": "design"}, {"LOWER": "record"}, {"LOWER": "book"}],
            [{"LOWER": "nonconfirmance "}, {"LOWER": "management"}, {"LOWER": "system"}],
            [{"LOWER": "data"}, {"LOWER": "distribution"}],
            [{"LOWER": "design"}, {"LOWER": "practice"}],
            [{"LOWER": "design"}, {"LOWER": "reviews"}],
            [{"LOWER": "drawing"}, {"LOWER": "signature"}, {"LOWER": "record"}],
            [{"LOWER": "engineering"}, {"LOWER": "program"}, {"LOWER": "execution"}, {"LOWER": "tool"}],
            [{"LOWER": "high"}, {"LOWER": "performance"}, {"LOWER": "archive"}, {"LOWER": "system"}],
            [{"LOWER": "quality"}, {"LOWER": "escape"}, {"LOWER": "management"}],
            [{"LOWER": "teamcenter"}],
            [{"LOWER": "tc"}],
            [{"LOWER": "reb"}],
            [{"LOWER": "repair"}, {"LOWER": "builder"}],
            [{"LOWER": "repairbuilder"}],
            [{"LOWER": "export"}, {"LOWER": "tagging"}],
            [{"LOWER": "cav"}],
            [{"LOWER": "cnf"}],
            [{"LOWER": "fai"}],
            [{"LOWER": "nginx"}],
            [{"LOWER": "nginxutil"}],
            [{"LOWER": "kibana"}],
            [{"LOWER": "jenkins"}],
            [{"LOWER": "ecid"}],
            [{"LOWER": "cid"}],
            [{"LOWER": "dte"}],
            [{"LOWER": "digital"}, {"LOWER": "thread"}, {"LOWER": "engineer"}],
            [{"LOWER": "openresty"}],
            [{"LOWER": "idm"}],
            [{"LOWER": "oneidm"}],
            [{"LOWER": "datalake"}],
            [{"LOWER": "afrt"}],
            [{"LOWER": "aeip"}],
            [{"LOWER": "data lake"}])

Doc.set_extension('closure_note', default=None)
Doc.set_extension('desc', default=None)
Doc.set_extension('id', default=None)
Doc.set_extension('app', default=['unknown'])
Doc.set_extension('category', default=['general'])
Doc.set_extension('notes', default={})
Doc.set_extension('attachments', default={})
Doc.set_extension('highlight', default=None)


def custom_category_component(doc):
    scores = []
    for cats in category_list:
        s = doc.similarity(cats[0])
        scores.append((cats, s))
        orderedScores = sorted(scores, key=lambda tup: tup[1], reverse=True)
        cat_list = []
        for j in orderedScores:
            if float(j[1]) > 0.50:
                cat_list.append(j[0].text)
        if len(cat_list) != 0:
            doc._.category = cat_list
    return doc


def application_component(doc):
    matches = matcher(doc)
    appNames = [doc[start:end].text for match_id, start, end in matches]
    for name in range(len(appNames)):
        appNames[name] = appNames[name].lower()
        if appMap.get(appNames[name]) is not None:
            appNames[name] = appMap.get(appNames[name])
    if len(appNames) > 0:
        doc._.app = list(set(appNames))
    return doc


nlp.add_pipe(application_component)
nlp.add_pipe(custom_category_component)

rowsInserted = 0
for doc, context in nlp.pipe(unprocessed_docs, as_tuples=True):
    doc._.id = context['id']
    doc._.desc = context['desc']
    doc._.closure_note = context['closure_note']
    doc._.notes = context['notes']
    doc._.attachments = context['attachments']
    sampleDocs.append(doc)

# Get all attachments from FMS and run below code
# # FOR FILE DATA
# files = ['DTE_DRB_General_Concepts.pdf','DTE_DRB_Getting_Started.pdf']
# for fileName in files:
#     with open(fileName, 'rb') as f:
#         doc = slate.PDF(f)
#         for i, p in enumerate(doc):
#             doc = nlp(p)
#             doc._.desc = p
#             docIndex['id'] = docIndex['id'] + 1
#             doc._.id = docIndex['id']
#             doc._.closure_note = "Page "+ str(i+1) +" of "+ fileName + " has more details on this"
#             sampleDocs.append(doc)


def getSuggestions(desc):
    print(desc)
    scores = []
    newDoc = nlp(desc)
    for doc in sampleDocs:
        is_intersect = 0
        if ('unknown' not in doc._.app) and (len(list(set(doc._.app).intersection(newDoc._.app))) > 0):
            is_intersect = 1
        scores.append({"intent": doc.text, "desc": doc._.desc, "app": doc._.app, "notes": doc._.notes,
                       "attachments": doc._.attachments, "category": doc._.category, "score": doc.similarity(newDoc),
                       "id": doc._.id, "closure_note": doc._.closure_note, "is_intersect": is_intersect})
    orderedScores = sorted(scores, key=lambda tup: tup["score"], reverse=True)
    return sorted(orderedScores[0:10], key=lambda tup: tup["is_intersect"], reverse=True)


def getDocById(doc_id):
    for doc in sampleDocs:
        if doc._.id == doc_id:
            return doc
    return None


def addNote(doc_id, note):
    # pool = dbInteraction.connect_db()
    connection = pool.acquire()
    cursor = connection.cursor()
    dbInteraction.insert_dts_note(cursor, note, doc_id)
    note_id = dbInteraction.select_note_id(cursor)
    dbInteraction.disconnect_pool(connection, pool)
    doc = getDocById(doc_id)
    if doc is not None:
        text = doc.text + ' ' + note
        newDoc = nlp(text)
        newDoc._.app = doc._.app
        newDoc._.desc = doc._.desc
        newDoc._.category = doc._.category
        newDoc._.id = doc._.id
        newDoc._.closure_note = doc._.closure_note
        newDoc._.attachments = doc._.attachments
        if doc._.notes == {}:
            newDoc._.attachments = {
                'NOTE_ID': [note_id],
                'NOTE_TEXT': [note],
                'DOC_ID': [doc_id]
            }
        else:
            newDoc._.notes = doc._.notes
            newDoc._.notes['NOTE_ID'].append(note_id)
            newDoc._.notes['NOTE_TEXT'].append(note)
            newDoc._.notes['DOC_ID'].append(doc_id)
        sampleDocs.remove(doc)
        sampleDocs.insert(newDoc._.id-2, newDoc)
        return note_id


def updateClosureNote(doc_id, closure_note):
    doc = getDocById(doc_id)
    if doc is not None:
        doc._.closure_note = closure_note
        # pool = dbInteraction.connect_db()
        connection = pool.acquire()
        cursor = connection.cursor()
        dbInteraction.update_doc_closure_note(cursor, doc_id, closure_note)
        dbInteraction.disconnect_pool(connection, pool)


def addVotedResult(description, closure_note):
    doc = nlp(description)
    doc._.desc = description
    doc._.closure_note = closure_note
    # pool = dbInteraction.connect_db()
    connection = pool.acquire()
    cursor = connection.cursor()
    doc._.id = dbInteraction.pushData(cursor, doc._.category[0], doc._.app[0], doc._.desc, doc._.closure_note)
    dbInteraction.disconnect_pool(connection, pool)
    sampleDocs.append(doc)


def addfile(doc_id, file_name, uuid):
    # pool = dbInteraction.connect_db()
    connection = pool.acquire()
    cursor = connection.cursor()
    dbInteraction.insert_dts_attachment(cursor, file_name, uuid, doc_id)
    atc_id = dbInteraction.select_atc_id(cursor, uuid)
    dbInteraction.disconnect_pool(connection, pool)
    doc = getDocById(doc_id)
    if doc is not None:
        text = doc.text
        newDoc = nlp(text)
        newDoc._.app = doc._.app
        newDoc._.desc = doc._.desc
        newDoc._.category = doc._.category
        newDoc._.id = doc._.id
        newDoc._.closure_note = doc._.closure_note
        newDoc._.notes = doc._.notes
        if doc._.attachments == {}:
            newDoc._.attachments = {
                'ATC_ID': [atc_id],
                'ATC_NAME': [file_name],
                'DOC_ID': [doc_id],
                'UUID': [uuid]
            }
        else:
            newDoc._.attachments = doc._.attachments
            newDoc._.attachments['ATC_ID'].append(atc_id)
            newDoc._.attachments['ATC_NAME'].append(file_name)
            newDoc._.attachments['DOC_ID'].append(doc_id)
            newDoc._.attachments['UUID'].append(uuid)
        sampleDocs.remove(doc)
        sampleDocs.insert(newDoc._.id - 2, newDoc)
    return atc_id

def addTicket(issue, note):
    doc = nlp(issue)
    doc._.desc = issue
    doc._.closure_note = note
    # pool = dbInteraction.connect_db()
    connection = pool.acquire()
    cursor = connection.cursor()
    doc._.id = dbInteraction.pushData(cursor, doc._.category[0], doc._.app[0], doc._.desc, doc._.closure_note)
    dbInteraction.disconnect_pool(connection, pool)
    sampleDocs.append(doc)


def removeTicket(doc_id):
    doc = getDocById(doc_id)
    if doc is not None:
        # pool = dbInteraction.connect_db()
        connection = pool.acquire()
        cursor = connection.cursor()
        dbInteraction.delete_doc_by_id(cursor, doc_id)
        dbInteraction.disconnect_pool(connection, pool)
        sampleDocs.remove(doc)
