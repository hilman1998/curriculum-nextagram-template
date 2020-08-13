from flask import Flask,Blueprint,render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from models.user import User
from models.payment import Payment
from instagram_web.util.helpers import gateway
from flask_login import login_user, logout_user, login_required, current_user

payments_blueprint = Blueprint("payments",
                            __name__,
                            template_folder="templates")

@payments_blueprint.route("/<image_id>/new", methods=["GET"])
@login_required
def new(image_id):
    client_token=gateway.client_token.generate()
    return render_template("payments/new.html", client_token=client_token,image_id=image_id ) 

@payments_blueprint.route("/<image_id>/checkout", methods=["POST"])
def create_purchase(image_id):
    nonce_from_the_client = request.form["payment_nonce"]
    amount = request.form["amount"]
    print(nonce_from_the_client)
    print("0000000000000000000000000")
    print(amount)
    result = gateway.transaction.sale({
    "amount": amount,
    "payment_method_nonce": nonce_from_the_client,
    "options": {
      "submit_for_settlement": True
    }
    })
        
    if result.is_success:
      payment = Payment(sender=User.get_by_id(current_user.id), image_id=image_id, amount=amount)
      payment.save()
      return redirect(url_for("images.show",id= image_id))
    else:
      flash("Failed to donate! Please try again!")
      return redirect(url_for("payments.new", image_id=image_id))
