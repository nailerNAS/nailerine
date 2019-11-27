from modules.db_model.misc import Base


def create_db():
    try:
        Base.metadata.create_all()
    except:
        Base.metadata.drop_all()
        Base.metadata.create_all()
