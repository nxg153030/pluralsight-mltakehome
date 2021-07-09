from flask import make_response, jsonify, request
from flask.views import MethodView
import numpy as np
import os
from scipy import sparse


class TopNUsersAPI(MethodView):

    def get(self):
        user_handle = request.args.get('user_handle')
        top_n_users = self.top_n_similar_users(int(user_handle))
        return make_response(jsonify(top_n_users), 200)

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

    def compute_similarity_score(self, user1_feature_vec, user2_feature_vec):
        numerator = np.dot(user1_feature_vec, user2_feature_vec)
        denominator = np.linalg.norm(user1_feature_vec) * np.linalg.norm(user2_feature_vec)
        cosine_similarity = 0.0
        if denominator != 0:
            cosine_similarity = numerator / denominator
        return round(cosine_similarity, 4)

    def top_n_similar_users(self, user_handle, n=5):
        try:
            feature_matrix = sparse.load_npz(os.path.join(os.path.dirname(__file__), 'sparse_user_features.npz'))
            feature_matrix = np.array(feature_matrix.todense())  # convert csr matrix to dense representation
        except Exception as e:
            print(f'ERROR: Unable to load feature matrix: {e}')
            raise Exception()

        user_feature_vec = feature_matrix[user_handle - 1][1:]
        user_handles = feature_matrix[:, 0]  # get 0th column
        top_n_user_handles = []
        for user_handle_2 in user_handles:
            if user_handle != user_handle_2:
                user2_feature_vec = feature_matrix[int(user_handle_2) - 1][1:]
                similarity_score = self.compute_similarity_score(user_feature_vec, user2_feature_vec)
                top_n_user_handles.append({'user_handle': int(user_handle_2), 'similarity_score': similarity_score})

        # sort the users by similarity scores from highest to lowest, and return the top n
        return sorted(top_n_user_handles, key=lambda k: k['similarity_score'], reverse=True)[:n]
