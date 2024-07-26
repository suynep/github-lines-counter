from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3
from glob import glob
from helpers.utils import (
    init,
    extract_zip,
    clear_uploads_dir,
    clone_repo,
    count_line_number,
    count_words,
)

if not os.path.exists("uploads"):
    os.makedirs("uploads")

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

con = sqlite3.connect("feedback.db", check_same_thread=False)
con_history = sqlite3.connect("history.db", check_same_thread=False)


clear = ""

@app.route("/", methods=["GET", "POST"])
def index():
    res = cur_history.execute("SELECT * FROM history")
    res = res.fetchall()
    return render_template("index.html", clear=clear, history=res)


@app.route("/clear_uploads", methods=["GET", "POST"])
def clear_uploads():
    clear = "Cleared Uploads"
    res = cur_history.execute("SELECT * FROM history")
    res = res.fetchall()
    clear_uploads_dir()
    return redirect(url_for("index", clear=clear, history=res))


def init_db():
    global cur
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS feedback(user, feedback)")
    global cur_history
    cur_history = con_history.cursor()
    cur_history.execute("CREATE TABLE IF NOT EXISTS history(id, url)")

    # res = cur.execute("SELECT name FROM sqlite_master")
    # print(res.fetchone())

init_db()


@app.route("/feedback", methods=["POST", "GET"])
def feedback():

    recent_feedback = request.form.get("feedback")
    username = request.form.get("username")

    if recent_feedback and username:
        cur.execute("INSERT INTO feedback VALUES (?, ?)", (username, recent_feedback))
        con.commit()
        res = cur.execute("SELECT * FROM feedback")
        res = res.fetchall()
        return render_template(
            "feedback.html", feedback=recent_feedback, all_feedback=res
        )
    else:
        res = cur.execute("SELECT * FROM feedback")
        res = res.fetchall()
        return render_template(
            "feedback.html", feedback="No Feedback", all_feedback=res
        )


@app.route("/word_count_req", methods=["POST", "GET"])
def word_count_req():
    init()
    url = request.form.get("url")
    db_count = cur_history.execute("SELECT COUNT(*) FROM history").fetchone()[0]
    cur_history.execute("INSERT INTO history VALUES (?, ?)", (db_count, url))
    con_history.commit()
    search_ext_list = [
        "1.ada",
        "2.ada",
        "ada",
        "adb",
        "ads",
        "asm",
        "bas",
        "bash",
        "bat",
        "c",
        "c++",
        "cbl",
        "cc",
        "class",
        "clj",
        "cob",
        "cpp",
        "cs",
        "csh",
        "cxx",
        "d",
        "diff",
        "e",
        "el",
        "f",
        "f77",
        "f90",
        "fish",
        "for",
        "fth",
        "ftn",
        "go",
        "groovy",
        "h",
        "hh",
        "hpp",
        "hs",
        "html",
        "htm",
        "hxx",
        "java",
        "js",
        "jsx",
        "jsp",
        "ksh",
        "kt",
        "lhs",
        "lisp",
        "lua",
        "m",
        "m4",
        "nim",
        "patch",
        "php",
        "pl",
        "po",
        "pp",
        "py",
        "r",
        "rb",
        "rs",
        "s",
        "scala",
        "sh",
        "swg",
        "swift",
        "ts",
        "tsx",
        "v",
        "vb",
        "vcxproj",
        "xcodeproj",
        "xml",
        "zsh",
    ]

    file_contents = []
    path = "uploads/"
    try:
        file_upload = request.files["optional-upload"]
    except:
        file_upload = None
    if file_upload != None:
        for uploaded_file in request.files.getlist("optional-upload"):
            if uploaded_file.filename != "":
                try:
                    uploaded_file.save(path + uploaded_file.filename)
                    path = path + uploaded_file.filename
                except:
                    print("File already exists / Error uploading file")
            file_contents = extract_zip(path)
        print(file_contents)

    if url:
        path = clone_repo(url)

    result_dict = {}
    max_used_ext = "py"
    for ext in search_ext_list:
        result_dict[ext] = [
            y for x in os.walk(path) for y in glob(os.path.join(x[0], "*." + ext))
        ]

    for key in result_dict:
        if len(result_dict[key]) > len(result_dict[max_used_ext]):
            max_used_ext = key

    print(result_dict, "\n", max_used_ext)

    word_count = 0
    line_count = 0
    rank = 0

    for key in result_dict:
        for file in result_dict[key]:
            line_count += count_line_number(file)
            word_count += count_words(file)

    ret_obj = {
        "max_used_ext": max_used_ext,
        "word_count": word_count,
        "line_count": line_count,
        "rank": rank,
    }

    return render_template("word_count_req.html", **ret_obj)
