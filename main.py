import flask
import numpy as np
import csv
import h5py
from scipy import sparse
import time

app = flask.Flask(__name__)


def load_feature_matrix():
    f = h5py.File('data/user_feature_matrix.h5', mode='r')
    dataset = f.create_dataset("feature_matrix")
    # dataset = user_feature_matrix['features']
    x = 1


def get_data():
    pass


def compute_similarity_score(user1_feature_vec, user2_feature_vec):
    numerator = np.dot(user1_feature_vec, user2_feature_vec)
    denominator = np.linalg.norm(user1_feature_vec) * np.linalg.norm(user2_feature_vec)
    cosine_similarity = 0.0
    if denominator != 0:
        cosine_similarity = numerator / denominator
    return round(cosine_similarity, 4)


def get_top_n_similar_users(user_handle, n=5):
    """
    TODO: Use dask to optimize data loading
    :param user_handle: unique user id
    :param n: number of similar users
    :return:
    """
    try:
        feature_matrix = np.loadtxt('data/user_feature_matrix.csv', skiprows=1, delimiter=',')  # expensive operation
    except Exception as e:
        print(f'ERROR: Unable to load feature matrix: {e}')
        raise Exception()
    user_feature_vec = feature_matrix[user_handle-1][1:]  # ignore first column which contains user handles
    user_handles = feature_matrix[:, 0]
    top_n_user_handles = []
    for user_handle_2 in user_handles:
        if user_handle != user_handle_2:
            user2_feature_vec = feature_matrix[int(user_handle_2)-1][1:]
            similarity_score = compute_similarity_score(user_feature_vec, user2_feature_vec)
            top_n_user_handles.append({'user_handle': int(user_handle_2), 'similarity_score': similarity_score})

    # sort the users by similarity scores from highest to lowest, and return the top n
    return sorted(top_n_user_handles, key=lambda k: k['similarity_score'], reverse=True)[:n]


def get_top_n_similar_users_csr_matrix(user_handle, n=5):
    try:
        feature_matrix = sparse.load_npz('sparse_user_features.npz')
        feature_matrix = np.array(feature_matrix.todense())  # convert csr matrix to dense representation
    except Exception as e:
        print(f'ERROR: Unable to load feature matrix: {e}')
        raise Exception()

    user_feature_vec = feature_matrix[user_handle-1][1:]
    user_handles = feature_matrix[:, 0]  # get 0th column
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
    # start_time = time.time()
    # top_n_users = get_top_n_similar_users(user_handle=1, n=5)
    # print(top_n_users)
    # print(f'Time taken by loading the feature matrix directly into memory: {round(time.time() - start_time, 2)} secs')

    start_time = time.time()
    top_n_users = get_top_n_similar_users_csr_matrix(user_handle=1, n=10)
    print(top_n_users)
    print(f'Time taken by using the CSR matrix representation: {round(time.time() - start_time, 2)}')
