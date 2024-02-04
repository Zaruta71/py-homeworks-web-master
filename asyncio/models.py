import aiohttp
import asyncio
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.util import asyncio
from datetime import datetime

engine = create_engine('postgresql://admin:1234@127.0.0.1:5432/asyncio_netology')
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Person_model(Base):
    __tablename__ = 'persons'

    id = Column(Integer, primary_key=True)
    birth_year = Column(Date)
    eye_color = Column(String(20))
    films = Column(String)
    gender = Column(String(20))
    hair_color = Column(String(20))
    height = Column(Integer)
    homeworld = Column(String)
    mass = Column(Integer)
    name = Column(String(100), nullable=False)
    skin_color = Column(String(20))
    species = Column(String)
    starships = Column(String)
    vehicles = Column(String)




async def get_info(url) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{url}') as response:
            response = await response.json()
            return response


async def info_list(url):
    result = await asyncio.gather(*[get_info(i) for i in url])

    result =  ", ".join([i.get('title') for i in result])
    return result

async def save_person_in_db(p_data):
    async with Session() as session:
        async with session.begin():
            for person in p_data:
                birth_year = datetime.strptime(person['birth_year'])
                eye_color = person['eye_color']
                films = asyncio.run(info_list(person['films']))
                gender = person['gender']
                hair_color = person['hair_color']
                height = int(person['eye_color'])
                homeworld = person['homeworld']
                mass = int(person['mass'])
                name = person['name']
                skin_color = person['skin_color']
                species = asyncio.run(info_list(person['species']))
                starships = asyncio.run(info_list(person['starships']))
                vehicles = asyncio.run(info_list(person['vehicles']))
                person = Person_model(birth_year=birth_year, eye_color=eye_color, films=films, gender=gender,
                                      hair_color=hair_color, height=height, homeworld=homeworld, mass=mass,
                                      name=name, skin_color=skin_color, species=species, starships=starships,
                                      vehicles=vehicles, person=person
                                      )
                session.add(person)
                session.commit()

# Base.metadata.create_all(engine)
