import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase):
    __tablename__ = 'jobs'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    team_leader = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=True)
    job = sa.Column(sa.String, nullable=True)
    work_size = sa.Column(sa.Integer, nullable=True)
    collaborators = sa.Column(sa.String, nullable=True)
    start_date = sa.Column(sa.DateTime, default=datetime.datetime.now)
    end_date = sa.Column(sa.DateTime)
    is_finished = sa.Column(sa.Boolean, default=False)

    user = orm.relationship('User', back_populates='jobs')
    categories = orm.relationship("Category",
                                  secondary="association",
                                  backref="jobs")

    def __repr__(self):
        return f"{self.team_leader} {self.job} {self.work_size} {self.collaborators} {self.is_finished}"
