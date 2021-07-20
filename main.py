from flask import Flask
from top_n_users import TopNUsersAPI


if __name__ == '__main__':
    app = Flask(__name__)
    top_n_users_view = TopNUsersAPI.as_view('top_n_users')
    app.add_url_rule('/topNUsers', view_func=top_n_users_view, methods=['GET', ])
    app.run(debug=True, host='0.0.0.0', port=9007)
