import flask
import numpy as np
import csv

app = flask.Flask(__name__)


def load_feature_matrix():
    pass


def compute_similarity_score(user1_feature_vec, user2_feature_vec):
    """
    1. Fetch all the courses the user1 and user2 have taken. Count no. of matching courses taken
        1.a: What about course tags?
    2. Fetch their interests. Count no. of matching interests
    3. Fetch all author handles of the course. (Add more weight to this?)
    4. How to use user assessment scores?
    5. How to use viewing time?
    The time of day when users watch a course. Users who are consistent
    I don't have a class to work with.
      |__c1___|__c2___|__c3___|
    u1|_______|_______|_______|
    u2|_______|_______|_______|
    Logic:
    1. Fetch feature_matrix
    2. Compute cosine distance
    3.
    """
    cosine_similarity = np.dot(user1_feature_vec, user2_feature_vec)/(np.linalg.norm(user1_feature_vec) * np.linalg.norm(user2_feature_vec))
    return round(cosine_similarity, 4)


def get_top_n_similar_users(user_handle, n=5):
    try:
        feature_matrix = np.loadtxt('data/user_feature_matrix.csv', skiprows=1, delimiter=',')  # expensive operation
    except Exception as e:
        print('ERROR: Unable to load feature matrix')
        raise Exception()
    user_feature_vec = feature_matrix[user_handle-1][1:]  # ignore first column which contains user handles
    user_feature_vec = user_feature_vec
    user_handles = feature_matrix[:, 0]
    top_n_user_handles = []
    for user_handle_2 in user_handles:
        if user_handle != user_handle_2:
            user2_feature_vec = feature_matrix[int(user_handle_2)-1][1:]
            similarity_score = compute_similarity_score(user_feature_vec, user2_feature_vec)
            top_n_user_handles.append({'user_handle': int(user_handle_2), 'similarity_score': similarity_score})

    # sort the users by similarity scores from highest to lowest, and return the top n
    return sorted(top_n_user_handles, key=lambda k: k['similarity_score'], reverse=True)[:n]


@app.route('/', methods=['GET'])
def home(user_handle, n=5):
    # top_n_users = get_top_n_similar_users(user_handle, n)
    # print(top_n_users)
    return "<h1> Hello 123 </h1>"


if __name__ == '__main__':
    # app.run(debug=True)
    top_n_users = get_top_n_similar_users(user_handle=1, n=5)
    print(top_n_users)