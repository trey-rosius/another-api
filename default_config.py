import os

DEBUG =True
SQLALCHEMY_DATABASE_URI ="sqlite:///data.db"
SQLALCHEMY_TRACK_MODIFICATIONS=False
PROPAGATE_EXCEPTIONS=True
#SECRET_KEY=os.environ["APP_SECRET_KEY"] or "you-will-not-ever-know"
SECRET_KEY="you-will-not-ever-know"
JWT_BLACKLIST_ENABLED=True
UPLOADED_IMAGES_DEST=os.path.join("static","images")
JWT_BLACKLIST_TOKEN_CHECKS=["access","refresh"]




