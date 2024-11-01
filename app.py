from flask import Flask, abort, render_template, jsonify, request, redirect, url_for
#render_template renderiza un template(pagina html), para
#eso busca una carpeta q se llame template

import sqlite3


def get_db_connection():
    conn = sqlite3.connect("database1.db")
    #como queremos q nos devuelva las filas
    conn.row_factory = sqlite3.Row
    return conn


#creando instancia
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    context = {'name':'base', "project": "Api dfdf"}
    return render_template(template_name_or_list="base.html", **context)

@app.route("/home", methods=["GET"])
def home():
    context = {'name':'home', "my_name" : "ghj", "lista": ['l1','l2','l3']}
    return render_template(template_name_or_list="home.html", **context)
    #return render_template("home.html")


@app.route("/post", methods=["GET"])
def get_all_post():
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts").fetchall()
    conn.close()
    # for post in posts:
    #     print("======>", post["id"])
    #     print("======>", post["title"])
    #     print("======>", post["content"])
    #     print("======>", post["created"])
    #     print("====================================")
    return render_template(template_name_or_list="post/posts.html", posts=posts)


@app.route("/post/<int:post_id>", methods=["GET"])
def get_one_post(post_id):
    if request.method == "GET":
        conn = get_db_connection()
        post = conn.execute("SELECT * FROM posts where id = ?", (post_id, )).fetchone()
        conn.close()
        if post is None:
            abort(404)

    print("====================================", post)
    # for post in posts:
    #     print("======>", post["id"])
    #     print("======>", post["title"])
    #     print("======>", post["content"])
    #     print("======>", post["created"])
    #     print("====================================")
    return render_template(template_name_or_list="post/post.html", post=post)


@app.route("/post/create", methods=["GET", "POST"])
def create_one_post():
    if request.method == "POST":
       title = request.form["title"]
       content = request.form["content"]
       conn = get_db_connection()
       conn.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title.upper(), content.capitalize()))
       conn.commit()
       conn.close()
       print(title)
       print(content)
       return redirect(url_for("get_all_post"))
    elif request.method == "GET":
       return render_template("post/create.html")
    

@app.route("/post/edit/<int:post_id>", methods=["GET", "POST"])
def edit_one_post(post_id):
    conn = get_db_connection()
    post = conn.execute("SELECT * FROM posts where id = ?", (post_id, )).fetchone()
    conn.close()
   


    if request.method == "POST":
       title = request.form["title"]
       content = request.form["content"]
       conn = get_db_connection()
       conn.execute("UPDATE posts SET title = ?, content = ? where id = ?", (title.upper(), content.capitalize(),post_id ))
       conn.commit()
       conn.close()
       print(title)
       print(content)
       return redirect(url_for("get_all_post"))
    elif request.method == "GET":
       return render_template(template_name_or_list="post/edit.html", post=post)
   

@app.route("/post/delete/<int:post_id>", methods=["POST"])
def delete_one_post(post_id):
    conn = get_db_connection()
   
    if request.method == "POST":
       conn.execute("DELETE FROM posts where id = ?", (post_id, ))
       conn.commit()
       conn.close()

       return redirect(url_for("get_all_post"))
    
    

#iniciando el servidor, debug true hace q el codigo 
# se modifique solo en el navegador
if __name__ == '__main__':
    app.run(debug=True)