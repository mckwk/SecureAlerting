from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.services.notifier import Notifier

router = APIRouter()


class Alert(BaseModel):
    id: int
    message: str
    severity: str


class AlertCreate(BaseModel):
    message: str
    severity: str


alerts_db: List[Alert] = []
notifier = Notifier()


@router.post("/alerts/")
async def create_alert(alert: AlertCreate):
    new_id = len(alerts_db) + 1
    alert_obj = Alert(
        id=new_id,
        message=alert.message,
        severity=alert.severity)
    alerts_db.append(alert_obj)

    # Send the notification
    notifier.send_notification(alert_obj.model_dump())

    return JSONResponse(
        status_code=201, content={
            "status": "Notification sent"})


@router.get("/alerts/", response_model=List[Alert])
async def get_alerts():
    return alerts_db


@router.get("/alerts/{alert_id}", response_model=Alert)
async def get_alert(alert_id: int):
    for alert in alerts_db:
        if alert.id == alert_id:
            return alert
    raise HTTPException(status_code=404, detail="Alert not found")
