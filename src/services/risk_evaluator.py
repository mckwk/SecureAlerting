from src.models.risk_estimation import RiskModelFactory


class RiskEvaluator:
    def __init__(self):
        self.risk_model = RiskModelFactory.get_active_model()

    def evaluate_risk(self, alert):
        return self.risk_model.calculate_risk(alert)
