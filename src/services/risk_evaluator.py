from src.models.alert import Alert
from src.models.risk_estimation import RiskModelFactory


class RiskEvaluator:
    def __init__(self):
        self.risk_model = RiskModelFactory.get_active_model()

    def evaluate_risk(self, alert: Alert):
        return self.risk_model.calculate_risk(alert.to_dict())
