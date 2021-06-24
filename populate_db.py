from db_schemas import UserAssessmentScores, UserCourseViews, CourseTags, UserInterests
from sqlalchemy import create_engine, MetaData

engine = create_engine('sqlite:///pluralsight.db', echo=True)
meta = MetaData()


def populate_db(create_tables):
    """
    Create 4 tables
    1. user_assessment_scores
    2. user_course_views
    3. course_tags
    4. user_interests
    """
    if create_tables:
        UserAssessmentScores.__table__.create(engine)
        UserCourseViews.__table__.create(engine)
        CourseTags.__table__.create(engine)
        UserInterests.__table__.create(engine)


if __name__ == '__main__':
    create_tbls = True
    populate_db(create_tbls)
