from distributed_video.db.base import Base, engine
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Integer, String, Column


class FrameInfoModel(Base):
    __tablename__ = "frameinfo"

    id = Column(Integer, primary_key=True)
    task = Column(String)
    frame_number = Column(Integer)
    coordinates = Column(JSONB)
    process_time = Column(Integer)  # in sec
    node = Column(Integer)  # can be 1, 2

    def __init__(
        self,
        task: str,
        frame_number: int,
        coordinates: dict,
        process_time: int,
        node: int,
    ) -> None:
        self.task = task
        self.frame_number = frame_number
        self.coordinates = coordinates
        self.process_time = process_time
        self.node = node

    def __repr__(self) -> str:
        return f"{self.task}:{self.frame_number}"


Base.metadata.create_all(engine)
