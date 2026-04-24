from app.db.repositories import DBRepository
from app.models.body_metric import BodyMetric
from app.schemas.body_metric import BodyMetricCreate


class BodyMetricService:
    def __init__(self, repo: DBRepository, session):
        self.repo = repo
        self.session = session

    def create_metric(self, user_id: int, data: BodyMetricCreate):
        metric = BodyMetric(user_id=user_id, **data.model_dump())
        self.repo.save_body_metric(metric, self.session)
        self.session.refresh(metric)
        return metric

    def list_metrics(self, user_id: int):
        return self.repo.get_body_metrics_by_user(user_id, self.session)
