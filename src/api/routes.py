from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.services.kafka_producer import AlertProducer

router = APIRouter()


class Alert(BaseModel):
    id: int
    message: str
    severity: str


class AlertCreate(BaseModel):
    message: str
    severity: str


alerts_db: List[Alert] = []
producer = AlertProducer()


@router.post("/alerts/")
async def create_alert(alert: AlertCreate):
    new_id = len(alerts_db) + 1
    alert_obj = Alert(
        id=new_id,
        message=alert.message,
        severity=alert.severity)
    alerts_db.append(alert_obj)

    # Publish the alert to Kafka
    producer.send_alert("alert_notifications", alert_obj.dict())

    return JSONResponse(
        status_code=201, content={
            "status": "Alert published to Kafka"})


@router.get("/alerts/", response_model=List[Alert])
async def get_alerts():
    return alerts_db


@router.get("/alerts/{alert_id}", response_model=Alert)
async def get_alert(alert_id: int):
    for alert in alerts_db:
        if alert.id == alert_id:
            return alert
    raise HTTPException(status_code=404, detail="Alert not found")
