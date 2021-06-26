from db_schemas import UserAssessmentScores, UserCourseViews, CourseTags, UserInterests
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.orm import sessionmaker
import csv
import numpy as np
import pandas as pd
from scipy import sparse
from config import *

engine = create_engine('sqlite:///pluralsight.db', echo=True)
meta = MetaData()

session = sessionmaker()
session.configure(bind=engine)
s = session()


def build_feature_matrix():
    user_course_views_df = pd.read_csv(USER_COURSE_VIEWS_PATH)
    user_interests_df = pd.read_csv(USER_INTERESTS_PATH)
    unique_users = user_interests_df.user_handle.unique()
    interest_tags = user_interests_df.interest_tag.unique()
    course_tags = user_course_views_df.course_id.unique()
    user_feature_matrix = []
    for user in unique_users:
        d = dict()
        d['user_handle'] = user
        user_interests = user_interests_df[user_interests_df.user_handle == user].interest_tag.unique()
        user_courses_taken = user_course_views_df[user_course_views_df.user_handle == user].course_id.unique()
        for col in interest_tags:
            if col in user_interests:
                d[col] = 1
            else:
                d[col] = 0
        for col in course_tags:
            if col in user_courses_taken:
                d[col] = 1
            else:
                d[col] = 0
        user_feature_matrix.append(d)
    user_feature_matrix_df = pd.DataFrame(user_feature_matrix)
    user_feature_matrix_df.to_csv('data/user_feature_matrix.csv', index=False)


def csv_to_csr():
    feature_matrix = np.loadtxt(FEATURE_MATRIX_CSV_PATH, dtype=int, skiprows=1, delimiter=',')
    sparse_feature_matrix = sparse.csr_matrix(feature_matrix)
    sparse.save_npz('sparse_user_features.npz', sparse_feature_matrix)


def populate_db(create_tables=False, populate_tables=False):
    """
    Create 4 tables
    1. user_assessment_scores
    2. user_course_views
    3. course_tags
    4. user_interests
    """
    if create_tables:
        insp = inspect(engine)
        if insp.has_table('user_assessment_scores'):
            UserAssessmentScores.__table__.drop(engine)
        if insp.has_table('user_course_views'):
            UserCourseViews.__table__.drop(engine)
        if insp.has_table('course_tags'):
            CourseTags.__table__.drop(engine)
        if insp.has_table('user_interests'):
            UserInterests.__table__.drop(engine)
        UserAssessmentScores.__table__.create(engine)
        UserCourseViews.__table__.create(engine)
        CourseTags.__table__.create(engine)
        UserInterests.__table__.create(engine)

    if populate_tables:
        dataset_paths = [USER_COURSE_VIEWS_PATH, COURSE_TAGS_PATH, USER_INTERESTS_PATH, USER_ASSESSMENTS_PATH]
        for path in dataset_paths:
            with open(path, newline='') as csvfile:
                data = csv.reader(csvfile, delimiter=',')
                next(data)  # skip first row
                if path == USER_COURSE_VIEWS_PATH:
                    for row in data:
                        record = UserCourseViews(user_handle=row[0], view_date=row[1],
                                                 course_name=row[2], author_handle=row[3], level=row[4],
                                                 course_view_time_seconds=row[5])
                        s.add(record)
                    s.commit()
                elif path == COURSE_TAGS_PATH:
                    for row in data:
                        record = CourseTags(course_id=row[0], course_tags=row[1])
                        s.add(record)
                    s.commit()
                elif path == USER_INTERESTS_PATH:
                    for row in data:
                        record = UserInterests(user_handle=row[0], interest_tag=row[1], date_followed=row[2])
                        s.add(record)
                    s.commit()
                elif path == USER_ASSESSMENTS_PATH:
                    for row in data:
                        record = UserAssessmentScores(user_handle=row[0], user_assessment_date=row[1],
                                                      assessment_tag=row[2], user_assessment_score=row[3])
                        s.add(record)
                    s.commit()


if __name__ == '__main__':
    create_tbls = False
    populate_tbls = False
    populate_db(create_tbls, populate_tbls)
