from typing import List
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from src.config.settings import settings
from src.models.alert import Alert
from src.services.kafka_producer import AlertProducer

router = APIRouter()

alerts_db: List[Alert] = []
producer = AlertProducer()


@router.post("/alerts/")
async def create_alert(request: Request):
    data = await request.json()
    message = data.get("message")
    severity = data.get("severity")

    if not message or not severity:
        raise HTTPException(status_code=400, detail="Invalid alert data")

    new_id = len(alerts_db) + 1
    alert_obj = Alert(
        id=new_id,
        message=message,
        severity=severity,
        timestamp="N/A"
    )
    alerts_db.append(alert_obj)

    # Publish the alert to Kafka
    producer.send_alert(settings.NOTIFICATION_TOPIC, alert_obj)

    return JSONResponse(
        status_code=201, content={
            "status": "Alert published to Kafka"
        }
    )


@router.get("/alerts/")
async def get_alerts():
    return [alert.to_dict() for alert in alerts_db]


@router.get("/alerts/{alert_id}")
async def get_alert(alert_id: int):
    for alert in alerts_db:
        if alert.id == alert_id:
            return alert.to_dict()
    raise HTTPException(status_code=404, detail="Alert not found")
