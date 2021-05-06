
from . import api
from show_result.model import User
from flask import make_response

from show_result.utils.commons import login_required

@login_required
@api.route("/index")
def index():
    return make_response("index.html")