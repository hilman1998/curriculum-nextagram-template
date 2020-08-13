from flask import Blueprint,render_template,redirect,url_for,flash, request
from werkzeug import secure_filename
from instagram_web.util.helpers import upload_file_to_s3
from models.image import Image
from flask_login import current_user,login_required

images_blueprint = Blueprint("images",
                            __name__,
                            template_folder="templates")

@images_blueprint.route("/new", methods=["GET"])
@login_required
def new():
    return render_template("images/new.html")

@images_blueprint.route("/<id>/show", methods=["GET"])
@login_required
def show(id):
    image = Image.get_or_none(Image.id == id)
    return render_template("images/show.html", image=image)

@images_blueprint.route("/", methods=["POST"])
@login_required 
def create():
    if "user_image" not in request.files:
        flash("No file provided!", "danger")
        return redirect(url_for("images.new"))
    
    file = request.files['user_image']

    file.filename = secure_filename(file.filename)
    # get path from S3
    image_path = upload_file_to_s3(file, current_user.name)
    
    # save path into image table
    image = Image(image_url=image_path, user=current_user.id)
    if image.save():
        flash("Image uploaded!" , "primary")
        return redirect(url_for('users.show',username=current_user.name))
    else:
        flash("Try again.","danger")
        return render_template("images/new.html")