"""Seed table alert_types

Revision ID: 52e8149befa1
Revises: 5e35f8c8870e
Create Date: 2025-11-24 13:08:57.468329

"""
from datetime import datetime
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from src.db.constants.alert_db_constants import AlertDbConstants

# revision identifiers, used by Alembic.
revision: str = '52e8149befa1'
down_revision: Union[str, Sequence[str], None] = '5e35f8c8870e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    alert_types_table = sa.table(
        'alert_types',
        sa.column('id', sa.UUID),
        sa.column('created_at', sa.DateTime),
        sa.column('name', sa.String),
        sa.column('reference', sa.String)
    )
    op.bulk_insert(
        alert_types_table,
        [
            {
                "id": uuid4(),
                "created_at": datetime.now(),
                "name": "Email",
                "reference": AlertDbConstants.ALERT_TYPE_REF_EMAIL
            },
            {
                "id": uuid4(),
                "created_at": datetime.now(),
                "name": "SMS",
                "reference": AlertDbConstants.ALERT_TYPE_REF_SMS
            },
        ]
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
