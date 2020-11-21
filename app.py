import mariadb
from flask import Flask, request, Response
import json
import dbcreds
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/posts', methods = ["GET", "POST", "PATCH", "DELETE"])
def posts():
    if request.method == "GET":
        conn = None
        cursor = None
        posts = None
        try:
            conn = mariadb.connect(host = dbcreds.host, password = dbcreds.password, user = dbcreds.user, port = dbcreds.port, database = dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM posts")
            posts = cursor.fetchall()
        except Exception as error:
            print("SOMETHING WENT WRONG (THIS IS LAZY)")
            print(error)
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.rollback()
                conn.close()
            if posts != None:
                return Response(json.dumps(posts, default=str), mimetype="application/json", status=200)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == "POST":
        conn = None
        cursor = None
        post_title = request.json.get("title")
        post_content = request.json.get("content")
        rows = None
        try:
            conn = mariadb.connect(host = dbcreds.host, password = dbcreds.password, user = dbcreds.user, port = dbcreds.port, database = dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO posts(title, content) VALUES(?, ?)", [post_title, post_content])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("SOMETHING WENT WRONG (THIS IS LAZY)")
            print(error)
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.rollback()
                conn.close()
            if rows == 1:
                return Response("Successfully made a post!", mimetype="text/html", status=201)
            else:
                return Response("Something went wrong", mimetype="text/html", status=500)
    elif request.method == "PATCH":
        conn = None
        cursor = None
        post_title = request.json.get("title")
        post_content = request.json.get("content")
        post_id = request.json.get("id")
        rows = None
        try:
            conn = mariadb.connect(host = dbcreds.host, password = dbcreds.password, user = dbcreds.user, port = dbcreds.port, database = dbcreds.database)
            cursor = conn.cursor()
            if post_title != "" and post_title != None:
                cursor.execute("UPDATE posts SET title=? WHERE id=?", [post_title, post_id])
            if post_content != "" and post_content != None:
                cursor.execute("UPDATE posts SET content=? WHERE id=?", [post_content, post_id])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("Something went wrong (THIS IS LAZY)")
            print(error)
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.rollback()
                conn.close()
            if rows == 1:
                return Response("Updated successfully", mimetype="text/html", status=204)
            else:
                return Response("Update failed", mimetype="text/html", status=500)
    elif request.method == "DELETE":
        conn = None
        cursor = None
        post_id = request.json.get("id")
        rows = None
        try:
            conn = mariadb.connect(host = dbcreds.host, password = dbcreds.password, user = dbcreds.user, port = dbcreds.port, database = dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM posts WHERE id=?", [post_id])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("Something went wrong (THIS IS LAZY)")
            print(error)
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.rollback()
                conn.close()
            if rows == 1:
                return Response("Delted successfully", mimetype="text/html", status=204)
            else:
                return Response("Delete failed", mimetype="text/html", status=500)