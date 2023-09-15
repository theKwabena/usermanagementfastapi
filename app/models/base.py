import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column

class CommonBase:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())

