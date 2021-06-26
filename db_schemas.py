from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class UserAssessmentScores(Base):
    __tablename__ = 'user_assessment_scores'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_handle = Column(Integer)
    user_assessment_date = Column(String(30))
    assessment_tag = Column(String(50))
    user_assessment_score = Column(Integer)


class UserCourseViews(Base):
    __tablename__ = 'user_course_views'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_handle = Column(Integer)
    view_date = Column(String(30))
    course_name = Column(String(50))
    author_handle = Column(Integer)
    level = Column(String(12))
    course_view_time_seconds = Column(Integer)


class CourseTags(Base):
    __tablename__ = 'course_tags'
    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(String(80))
    course_tags = Column(String(40))


class UserInterests(Base):
    __tablename__ = 'user_interests'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_handle = Column(Integer)
    interest_tag = Column(String(40))
    date_followed = Column(String(30))



