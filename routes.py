import logging
import os
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    jsonify,
    url_for,
)
from models import db, Post
from datetime import datetime
import feedparser
from werkzeug.utils import secure_filename

routes = Blueprint("routes", __name__)
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@routes.route("/")
def hello():
    posts = Post.query.order_by(Post.date.desc()).all()
    for post in posts:
        if post.image:
            post.image_url = url_for("static", filename=f"uploads/{post.image}")
        else:
            post.image_url = None
    return render_template("index.html", posts=posts)


@routes.route("/posts", methods=["GET", "POST"])
def show_posts():
    if request.method == "POST":
        if "delete" in request.form:
            post_id = request.form["delete"]
            post = Post.query.get_or_404(post_id)
            db.session.delete(post)
            db.session.commit()
            flash("Post deleted successfully", "success")
        return redirect(url_for("routes.show_posts"))

    posts = Post.query.order_by(Post.date.desc()).all()
    for post in posts:
        if post.image:
            post.image_url = url_for("static", filename=f"uploads/{post.image}")
        else:
            post.image_url = None
    return render_template("posts.html", posts=posts)


@routes.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == "POST":
        post.title = request.form["title"]
        post.text = request.form["text"]
        post.icon = request.form.get("icon")
        post.image = request.form.get("image")
        db.session.commit()
        flash("Post updated successfully", "success")
        return redirect(url_for("routes.show_posts"))
    return render_template("edit_post.html", post=post)


@routes.route("/add_post", methods=["GET", "POST"])
def add_post():
    if request.method == "POST":
        title = request.form["title"]
        text = request.form["text"]
        icon = request.form["icon"]

        logging.info(f"Received post data: title={title}, text={text}, icon={icon}")

        # Handle image upload
        image_filename = None
        if "image" in request.files:
            file = request.files["image"]
            logging.info(f"Received file: {file.filename}")
            if file and file.filename != "" and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_folder = current_app.config["UPLOAD_FOLDER"]
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                    logging.info(f"Created upload folder: {upload_folder}")
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
                image_filename = filename
                logging.info(f"Saved file to: {file_path}")
            else:
                logging.warning("Invalid file or no file uploaded")
        else:
            logging.warning("No image file in request")

        new_post = Post(
            title=title,
            text=text,
            icon=icon,
            image=image_filename,
            date=datetime.utcnow(),
        )
        db.session.add(new_post)
        db.session.commit()
        logging.info(f"Added new post to database: id={new_post.id}")
        flash("Post added successfully", "success")
        return redirect(url_for("routes.show_posts"))
    return render_template("add_post.html")


@routes.route("/get_news")
def get_news():
    try:
        feed = feedparser.parse("https://rss.walla.co.il/feed/1?type=main")
        news_items = []
        for entry in feed.entries[:]:
            news_items.append({"title": entry.title, "pubDate": entry.published})
        return jsonify(news_items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
