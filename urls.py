from sanic import Sanic,Blueprint
from data_ins import data_collection

# urls for the file
login = Blueprint(name = "twad_insertation", url_prefix="/zogx_test")

#child url

#user details
login.add_route(data_collection.user_details,"/user-details",methods=["POST"])

#user login 
login.add_route(data_collection.user_login,"/user-login",methods=["POST"])

#particular user info
login.add_route(data_collection.user_info,"/user-info",methods=["POST"])

#user overall info
login.add_route(data_collection.overall_info,"/overall-info",methods=["POST"])

#password update
login.add_route(data_collection.password_reset,"/password-reset",methods=["POST"])

#user id delete
login.add_route(data_collection.delete_user,"/delete-user",methods=["POST"])

#forgot password
login.add_route(data_collection.forgot_password,"/forgot-password",methods=["POST"])

#generate_otp
login.add_route(data_collection.generate_otp,"/generate-otp",methods=["POST"])

#otp verfiy
login.add_route(data_collection.otp_verfiy,"/otp-verfiy",methods=["POST"])

#cooling pad status
login.add_route(data_collection.cooling_pad_status,"/cooling-pad-status",methods=["POST"])

#fan status
login.add_route(data_collection.fan_status,"/fan-status",methods=["POST"])

#checking 

login.add_route(data_collection.alaram1,"/alaram1",methods=["POST"])

