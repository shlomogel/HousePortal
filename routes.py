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
from bs4 import BeautifulSoup
from werkzeug.utils import secure_filename

routes = Blueprint("routes", __name__)
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@routes.route("/")
def hello():
    # Get the latest important post
    important_post = (
        Post.query.filter_by(important=True).order_by(Post.date.desc()).first()
    )

    # Get all non-important posts (including those with null important field)
    posts = (
        Post.query.filter((Post.important.is_(False)) | (Post.important.is_(None)))
        .order_by(Post.date.desc())
        .all()
    )

    # Process image URLs
    for post in posts:
        if post.image:
            post.image_url = url_for("static", filename=f"uploads/{post.image}")
        else:
            post.image_url = None

    # Process image URL for important post if it exists
    if important_post and important_post.image:
        important_post.image_url = url_for(
            "static", filename=f"uploads/{important_post.image}"
        )

    return render_template("index.html", posts=posts, important_post=important_post)


@routes.route("/debug_posts")
def debug_posts():
    all_posts = Post.query.all()
    posts_info = []
    for post in all_posts:
        posts_info.append(
            {
                "id": post.id,
                "title": post.title,
                "important": post.important,
                "date": post.date.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
    return jsonify(posts_info)


@routes.route("/fix_posts/<int:post_id>")
def fix_posts(post_id):
    post = Post.query.get_or_404(post_id)
    post.important = False
    db.session.commit()
    return jsonify(
        {
            "message": f'Post "{post.title}" updated, important set to False',
            "post_id": post_id,
        }
    )


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

    # Get all posts (including important ones) for the management page
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
        post.important = "important" in request.form

        # Handle image update
        if "image" in request.files:
            file = request.files["image"]
            if file and file.filename != "":
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
                file.save(file_path)
                post.image = filename

        db.session.commit()
        flash("הפוסט עודכן בהצלחה", "success")
        return redirect(url_for("routes.show_posts"))
    return render_template("edit_post.html", post=post)


@routes.route("/add_post", methods=["GET", "POST"])
def add_post():
    if request.method == "POST":
        title = request.form["title"]
        text = request.form["text"]
        icon = request.form["icon"]
        important = request.form.get("important", "") == "on"

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
            important=important,
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
        feed = feedparser.parse("https://rss.walla.co.il/feed/1")
        news_items = []

        for entry in feed.entries[:]:
            # Parse HTML content
            soup = BeautifulSoup(entry.description, "html.parser")

            # Remove all img tags and their parent a tags if they exist
            for img in soup.find_all("img"):
                if img.parent.name == "a":
                    img.parent.decompose()
                else:
                    img.decompose()

            # Remove any remaining a tags that might have contained images
            for a in soup.find_all("a"):
                a.decompose()

            # Get the cleaned text
            clean_description = soup.get_text(strip=True)

            news_items.append(
                {
                    "title": entry.title,
                    "pubDate": entry.published,
                    "description": clean_description,
                }
            )

        return jsonify(news_items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
