import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY',os.urandom(24))
    SQLALCHEMY_DATABASE_URI = os.getenv('Database_URL','postgres://b03d6f05f12099501e8d1f6ab41b296fa462afa738f09e290ddd181389a80d36:sk_cPhmuv69mHxsb_L1qiiB4@db.prisma.io:5432/postgres?sslmode=require')
    SQLALCHEMY_TRACK_MODIFICATIONS = False