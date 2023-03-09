from distributed_video.db.base import Base, engine

Base.metadata.create_all(engine)

# metadata_obj.create_all(engine)
