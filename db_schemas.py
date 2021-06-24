from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()


class UserAssessmentScores(Base):
    __tablename__ = 'user_assessment_scores'
    user_handle = Column(Integer, primary_key=True, nullable=False)
    user_assessment_date = Column(DateTime)
    assessment_tag = Column(String(50))
    user_assessment_score = Column(Integer)


class UserCourseViews(Base):
    __tablename__ = 'user_course_views'
    user_handle = Column(Integer, primary_key=True, nullable=False)
    view_date = Column(DateTime)
    course_name = Column(String(50))
    author_handle = Column(Integer)
    level = Column(String(12))
    course_view_time_seconds = Column(Integer)


class CourseTags(Base):
    """
    TODO: There are multiple tags for the same course id, these need to be combined
    """
    __tablename__ = 'course_tags'
    course_id = Column(String(80), primary_key=True)
    course_tags = Column(String(40))


class UserInterests(Base):
    __tablename__ = 'user_interests'
    user_handle = Column(Integer, primary_key=True, nullable=False)
    interest_tag = Column(String(40))
    date_followed = Column(DateTime)



