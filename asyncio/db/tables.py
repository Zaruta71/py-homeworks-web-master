from sqlalchemy import Column, Integer, String, inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    birth_year = Column(String(80), nullable=False)
    eye_color = Column(String, nullable=False)
    films = Column(String, nullable=False)
    gender = Column(String(50), nullable=False)
    hair_color = Column(String(50), nullable=False)
    height = Column(String, nullable=False)
    homeworld = Column(String(100), nullable=False)
    mass = Column(String, nullable=False)
    name = Column(String(150), nullable=False)
    skin_color = Column(String(50), nullable=False)
    species = Column(String, nullable=False)
    starships = Column(String, nullable=False)
    vehicles = Column(String, nullable=False)


async def create_tables(engine):
    async with engine.begin() as conn:
        tables = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names()
        )
        if Person.__tablename__ in tables:
            print('already created')
        else:
            await conn.run_sync(Base.metadata.create_all)
            print("created")


async def get_session(engine):
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    return async_session

