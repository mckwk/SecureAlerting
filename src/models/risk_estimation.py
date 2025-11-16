import os
from abc import ABC, abstractmethod

from config import settings


class RiskEstimationModule(ABC):
    @abstractmethod
    def calculate_risk(self, alert):
        """
        Calculate the risk score and level for the given alert.
        """
        pass


class BaselineRiskModel(RiskEstimationModule):
    def calculate_risk(self, alert):
        severity = alert.get("severity", "low").lower()
        if severity == "critical":
            return {"risk_score": 90, "risk_level": "Critical"}
        elif severity == "high":
            return {"risk_score": 70, "risk_level": "High"}
        elif severity == "medium":
            return {"risk_score": 50, "risk_level": "Medium"}
        else:
            return {"risk_score": 30, "risk_level": "Low"}


class RiskModelFactory:
    @staticmethod
    def get_active_model() -> RiskEstimationModule:
        model_name = settings.RISK_MODEL
        if model_name == "BaselineRiskModel":
            return BaselineRiskModel()
        else:
            raise ValueError(f"Unknown risk model: {model_name}")
