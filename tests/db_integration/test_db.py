from db.repository.alert.alert_sending_status_repository import AlertSendingStatusRepository
from db.repository.alert.alert_severity_repository import AlertSeverityRepository
from db.repository.alert.alert_type_repository import AlertTypeRepository
from db.repository.risk.risk_estimation_model_repository import RiskEstimationModelRepository


def test_alert_types_fetch_all(db_session):
    repo: AlertTypeRepository = AlertTypeRepository(db_session)
    fetched = repo.find_all()
    assert fetched is not None
    assert len(fetched) == 2


def test_alert_severities_fetch_all(db_session):
    repo: AlertSeverityRepository = AlertSeverityRepository(db_session)
    fetched = repo.find_all()
    assert fetched is not None
    assert len(fetched) == 4


def test_alert_sending_statuses_fetch_all(db_session):
    repo: AlertSendingStatusRepository = AlertSendingStatusRepository(db_session)
    fetched = repo.find_all()
    assert fetched is not None
    assert len(fetched) == 3


def test_risk_estimation_models_fetch_all(db_session):
    repo: RiskEstimationModelRepository = RiskEstimationModelRepository(db_session)
    fetched = repo.find_all()
    assert fetched is not None
    assert len(fetched) == 1
