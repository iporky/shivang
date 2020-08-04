import spacy
import pandas as pd
from spacy.matcher import Matcher
from spacy.tokens import Doc
#import slate3k as slate
import dbInteraction

if __name__ == "__main__":
    df = pd.read_excel('Helpdesk_Report_part_cleaned_final.xlsx')
    nan_value = float("NaN")
    df.replace("", nan_value, inplace=True)
    df.dropna(subset=["Ticket Closure notes"], inplace=True)
    unprocessDocs = []
    categoryList = ['access', 'error', 'general', 'logs', 'report', 'usage']

    appMap = {
        "data distribution": "dd",
        "nonconfirmance management system": "nms",
        "significant process substantiation": "sps",
        "high performance archive system": "hpas",
        "quality escape management": "qem",
        "engineering program execution tool": "epex",
        "design reviews": "dr",
        "design review": "dr",
        "design practice": "dp",
        "drawing signature record": "dsr",
        "design record book": "drb",
        "repairbuilder": "reb",
        "repair builder": "reb",
        "export tagging": "dax",
        "nginxutil": "nginx",
        "openresty": "nginx",
        "fai": "cav",
        "cnf": "cav",
        "cid": "ecid",
        "aeip": "afrt",
        "tc": "teamcenter",
        "digital thread engineer": "dte",
        "oneidm": "idm",
        "data lake": "datalake",
        "general": "general",
        "Digital thread intelligence": 'dti',
        'Aviation Additive Product Industrialization': 'aapi',
        'Quality Escape Manual': 'qem'
    }
    docIndex = {'id': 1}
    sampleDocs = []
    for index in df.index:
        text = str(df["Ticket Description"][index])
        context = {"closure_note": str(df["Ticket Closure notes"][index]),
                   "desc": str(df["Ticket Description"][index])}  # , "note": finalNotes, "noteArray": cleanedArray}
        unprocessDocs.append((text, context))

    nlp = spacy.load('en_vectors_web_lg')
    category_list = [nlp('error'), nlp('access'), nlp('usage'), nlp('report'), nlp('logs')]
    matcher = Matcher(nlp.vocab)
    matcher.add("Application", None,
                [{"LOWER": "sps"}], [{"LOWER": "drb"}], [{"LOWER": "nms"}], [{"LOWER": "cert"}], [{"LOWER": "dwb"}],
                [{"LOWER": "dd"}], [{"LOWER": "dp"}], [{"LOWER": "dr"}], [{"LOWER": "dsr"}],
                [{"LOWER": "epex"}], [{"LOWER": "hpas"}], [{"LOWER": "qem"}], [{"LOWER": "dti"}],
                [{"LOWER": "dte"}, {"LOWER": "discover"}], [{"LOWER": "departure"}, {"LOWER": "record"}],
                [{"LOWER": "dp"}, {"LOWER": "systems"}], [{"LOWER": "dr"}, {"LOWER": "systems"}],
                [{"LOWER": "drb"}, {"LOWER": "systems"}], [{"LOWER": "laws"}, {"LOWER": "fa"}],
                [{"LOWER": "repair"}, {"LOWER": "docs"}], [{"LOWER": "aapi"}], [{"LOWER": "dax"}],
                [{"LOWER": "significant"}, {"LOWER": "process"}, {"LOWER": "substantiation"}],
                [{"LOWER": "design"}, {"LOWER": "record"}, {"LOWER": "book"}],
                [{"LOWER": "nonconfirmance "}, {"LOWER": "management"}, {"LOWER": "system"}],
                [{"LOWER": "data"}, {"LOWER": "distribution"}], [{"LOWER": "design"}, {"LOWER": "practice"}],
                [{"LOWER": "design"}, {"LOWER": "reviews"}],
                [{"LOWER": "drawing"}, {"LOWER": "signature"}, {"LOWER": "record"}],
                [{"LOWER": "engineering"}, {"LOWER": "program"}, {"LOWER": "execution"}, {"LOWER": "tool"}],
                [{"LOWER": "high"}, {"LOWER": "performance"}, {"LOWER": "archive"}, {"LOWER": "system"}],
                [{"LOWER": "quality"}, {"LOWER": "escape"}, {"LOWER": "management"}], [{"LOWER": "teamcenter"}],
                [{"LOWER": "tc"}],
                [{"LOWER": "reb"}], [{"LOWER": "repair"}, {"LOWER": "builder"}], [{"LOWER": "repairbuilder"}],
                [{"LOWER": "export"}, {"LOWER": "tagging"}], [{"LOWER": "cav"}], [{"LOWER": "cnf"}], [{"LOWER": "fai"}],
                [{"LOWER": "nginx"}], [{"LOWER": "nginxutil"}], [{"LOWER": "kibana"}], [{"LOWER": "jenkins"}],
                [{"LOWER": "ecid"}],
                [{"LOWER": "cid"}], [{"LOWER": "dte"}],
                [{"LOWER": "digital"}, {"LOWER": "thread"}, {"LOWER": "engineer"}], [{"LOWER": "openresty"}],
                [{"LOWER": "idm"}], [{"LOWER": "oneidm"}], [{"LOWER": "datalake"}], [{"LOWER": "afrt"}],
                [{"LOWER": "aeip"}], [{"LOWER": "data lake"}])

    Doc.set_extension('closure_note', default=None)
    Doc.set_extension('desc', default=None)
    Doc.set_extension('id', default=None)
    Doc.set_extension('app', default=['unknown'])
    Doc.set_extension('category', default=['general'])
    Doc.set_extension('notes', default=[])
    Doc.set_extension('attachments', default=[])
    Doc.set_extension('highlight', default=None)


    def custom_category_component(doc):
        scores = []
        for i in category_list:
            s = doc.similarity(i[0])
            scores.append((i, s))
            orderedScores = sorted(scores, key=lambda tup: tup[1], reverse=True)
            catlist = []
            for j in orderedScores:
                if float(j[1]) > 0.50:
                    catlist.append(j[0].text)
            if len(catlist) != 0:
                doc._.category = catlist
        return doc


    def application_component(doc):
        matches = matcher(doc)
        appNames = [doc[start:end].text for match_id, start, end in matches]
        for i in range(len(appNames)):
            appNames[i] = appNames[i].lower()
            if appMap.get(appNames[i]) != None:
                appNames[i] = appMap.get(appNames[i])
        if len(appNames) > 0:
            doc._.app = list(set(appNames))
        return doc

    nlp.add_pipe(application_component)
    nlp.add_pipe(custom_category_component)
    # WORK HERE
    connection = dbInteraction.connect_db()
    cursor = connection.cursor()

    # dbInteraction.insertAppAndCatTables(connection, cursor, categoryList, appMap)
    print("starting row addition")
    rowsInserted = 0
    for doc, context in nlp.pipe(unprocessDocs, as_tuples=True):
        doc._.desc = context['desc']
        doc._.closure_note = context['closure_note']
        sampleDocs.append(doc)
        # DB INTERACTION STATEMENTS
        if rowsInserted < 2581:
            rowsInserted += 1
            continue
        print("skipping completed")
        dbInteraction.pushData(cursor, doc._.category[0], doc._.app[0], doc._.desc, doc._.closure_note)
        rowsInserted += 1
        print("curr row: ", rowsInserted)
        print("------------")
        if rowsInserted % 100 == 0:
            dbInteraction.disconnect_db(connection, cursor)
            connection = dbInteraction.connect_db()
            cursor = connection.cursor()
    print("$$$$$$$$$$$$$$$$$$")
    # FOR FILE DATA
    print("SENDING DOCS DATA TO DB")
    # files = ['DTE_DRB_General_Concepts.pdf', 'DTE_DRB_Getting_Started.pdf']
    files = []
    for fileName in files:
        with open(fileName, 'rb') as f:
            #doc = slate.PDF(f)
            for i, p in enumerate(doc):
                doc = nlp(p)
                doc._.desc = p
                docIndex['id'] = docIndex['id'] + 1
                doc._.id = docIndex['id']
                doc._.closure_note = "Page " + str(i + 1) + " of " + fileName + " has more details on this"
                # doc._.highlight = para
                sampleDocs.append(doc)
                # DB RELATED QUERIES
                dbInteraction.pushData(cursor, doc._.category[0], doc._.app[0], doc._.desc, doc._.closure_note)
                rowsInserted += 1
                print("curr row: ", rowsInserted)
                if rowsInserted % 50 == 0:
                    dbInteraction.disconnect_db(connection, cursor)
                    connection = dbInteraction.connect_db()
                    cursor = connection.cursor()
    dbInteraction.disconnect_db(connection, cursor)
    print("data insertion complete")
    exit(0)









