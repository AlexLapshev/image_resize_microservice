from gino import Gino


db = Gino()
url = 'postgresql://db_user:123456@0.0.0.0:5432/image_microservice'


class ImageForResize(db.Model):
    __tablename__ = 'images'

    image_id = db.Column(db.Integer(), primary_key=True)
    image_path = db.Column(db.String())
    image_status = db.Column(db.Integer, db.ForeignKey('status.status_id'))


class Status(db.Model):
    __tablename__ = 'status'

    status_id = db.Column(db.Integer(), primary_key=True)
    status_name = db.Column(db.String())


async def connect_to_db(*args, **kwargs):
    await db.set_bind(url)
    # await db.gino.create_all()


async def disconnect_from_db(*args, **kwargs):
    await db.pop_bind().close()


