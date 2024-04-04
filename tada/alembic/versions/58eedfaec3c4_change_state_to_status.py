"""change state to status

Revision ID: 58eedfaec3c4
Revises: 64936edf6fcf
Create Date: 2024-04-02 00:48:07.909082

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "58eedfaec3c4"
down_revision: Union[str, None] = "64936edf6fcf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "articles",
        sa.Column(
            "status", sa.Enum("DRAFT", "PUBLISHED", name="status"), nullable=False
        ),
    )
    op.drop_column("articles", "state")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "articles",
        sa.Column(
            "state",
            postgresql.ENUM("DRAFT", "PUBLISHED", name="status"),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_column("articles", "status")
    # ### end Alembic commands ###