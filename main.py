import flask

app = flask.Flask(__name__)


def compute_similarity_score(user_handle_1, user_handle_2):
    pass


def get_top_n_similar_users(user_handle, n=5):
    # fetch the user record
    # compute similarity score between passed user and every other user in the db
    # sort the results by most similar to least similar
    # return user handles of top 5 most similar users
    top_n_user_handles = []
    user_handles = get_all_user_handles()
    user_similarity_score_mappings = {}
    top_n_user_handles = []
    for user_handle_2 in user_handles:
        similarity_score = compute_similarity_score(user_handle, user_handle_2)
        user_similarity_score_mappings[user_handle_2] = similarity_score

    return top_n_user_handles


@app.route('/', methods=['GET'])
def home(user_handle, n=5):
    top_n_users = get_top_n_similar_users(user_handle, n)
    return "<h1> Hello 123 </h1>"


if __name__ == '__main__':
    app.run(debug=True)