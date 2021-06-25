from db_schemas import UserAssessmentScores, UserCourseViews, CourseTags, UserInterests
from sqlalchemy import create_engine, MetaData
import numpy as np

engine = create_engine('sqlite:///pluralsight.db', echo=True)
meta = MetaData()

csv_file_paths = ['data/user_assessment_scores.csv', 'data/user_course_views.csv', 'data/user_course_tags.csv',
                  'data/user_interests.csv']


def populate_db(create_tables=False, populate_tables=False):
    """
    Create 4 tables
    1. user_assessment_scores
    2. user_course_views
    3. course_tags
    4. user_interests

    TODO: Populate tables from csv files
    """
    if create_tables:
        UserAssessmentScores.__table__.create(engine)
        UserCourseViews.__table__.create(engine)
        CourseTags.__table__.create(engine)
        UserInterests.__table__.create(engine)

    if populate_tables:
        data = np.genfromtxt(csv_file_paths[0], delimiter=',', skip_header=1)
        for j in data:
            record = UserAssessmentScores()

        data = np.genfromtxt(csv_file_paths[1], delimiter=',', skip_header=1)


if __name__ == '__main__':
    create_tbls = False
    populate_tbls = True
    populate_db(create_tbls, populate_tbls)
