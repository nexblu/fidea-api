from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Boolean,
    Float,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import registry, relationship
from databases import metadata, db_session

mapper_registry = registry()


class StoreDatabase:
    query = db_session.query_property()

    def __init__(self, user_id, seller, created_at, updated_at):
        self.user_id = user_id
        self.seller = seller
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"<Store {self.seller!r}>"


store_table = Table(
    "store",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "user_id",
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    ),
    Column("seller", String(collation="C"), unique=True, nullable=False),
    Column("created_at", Float, nullable=False),
    Column("updated_at", Float, nullable=False),
    Column("amount", Float, default=0),
    Column("is_active", Boolean, default=True),
    Column("banned_at", Float, default=None),
    Column("unbanned_at", Float, default=None),
    CheckConstraint("user_id >= 0", name="positive_user_id"),
    CheckConstraint("created_at >= 0", name="positive_created_at"),
    CheckConstraint("updated_at >= 0", name="positive_updated_at"),
    CheckConstraint("amount >= 0", name="positive_amount"),
    CheckConstraint(
        "(banned_at >= 0) OR (banned_at IS NULL)", name="positive_banned_at_or_null"
    ),
    CheckConstraint(
        "(unbanned_at >= 0) OR (unbanned_at IS NULL)",
        name="positive_un_banned_at_or_null",
    ),
)

mapper_registry.map_imperatively(StoreDatabase, store_table)
