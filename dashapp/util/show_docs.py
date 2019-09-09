from flask import Blueprint, send_from_directory
docs = Blueprint('docs', __name__)
@docs.route('/docs/<path:path>')
def show_docs(path):
    try:
        return send_from_directory('docs', path)
    except Exception as e:
        if path.endswith("/"):
            print(e)
            return send_from_directory('docs', "{}index.html".format(path))
        return send_from_directory('docs', "{}index.html".format(path))