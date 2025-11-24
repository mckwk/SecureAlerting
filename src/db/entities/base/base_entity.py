from datetime import datetime
from typing import Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseEntity(DeclarativeBase):
    created_at: Mapped[Optional[datetime]] = mapped_column(
        default=datetime.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        default=datetime.now(),
        onupdate=datetime.now()
    )
    deleted_at: Mapped[Optional[datetime]]