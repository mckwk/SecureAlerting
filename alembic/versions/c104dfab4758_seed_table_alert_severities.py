"""Seed table alert_severities

Revision ID: c104dfab4758
Revises: 52e8149befa1
Create Date: 2025-11-24 13:22:43.664642

"""
from datetime import datetime
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from src.db.constants.alert_db_constants import AlertDbConstants

# revision identifiers, used by Alembic.
revision: str = 'c104dfab4758'
down_revision: Union[str, Sequence[str], None] = '52e8149befa1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    alert_severities_table = sa.table(
        'alert_severities',
        sa.column('id', sa.UUID),
        sa.column('created_at', sa.DateTime),
        sa.column('name', sa.String),
        sa.column('reference', sa.String),
        sa.column('max_risk_score', sa.Integer),
    )
    op.bulk_insert(
        alert_severities_table,
        [
            {
                "id": uuid4(),
                "created_at": datetime.now(),
                "name": "Low",
                "reference": AlertDbConstants.ALERT_SEVERITY_REF_LOW,
                "max_risk_score": 30,
            },
            {
                "id": uuid4(),
                "created_at": datetime.now(),
                "name": "Medium",
                "reference": AlertDbConstants.ALERT_SEVERITY_REF_MEDIUM,
                "max_risk_score": 50,
            },
            {
                "id": uuid4(),
                "created_at": datetime.now(),
                "name": "High",
                "reference": AlertDbConstants.ALERT_SEVERITY_REF_HIGH,
                "max_risk_score": 70,
            },
            {
                "id": uuid4(),
                "created_at": datetime.now(),
                "name": "Critical",
                "reference": AlertDbConstants.ALERT_SEVERITY_REF_CRITICAL,
                "max_risk_score": 90,
            },
        ]
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
