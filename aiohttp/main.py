import aiohttp
import asyncio
from validation import PersonModel, validator_model
from db.tables import create_tables, get_session, Person
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine


async def converts_to_a_string(session, data: dict, key_1: str, key_2: str) -> dict:
    try:
        urls_list = data[key_1]
        if urls_list:
            names_list = []
            for url in urls_list:
                async with session.get(url) as res:
                    names_list.append((await res.json()).get(key_2))
            data[key_1] = ', '.join(names_list)
        else:
            data[key_1] = 'empty'
    except KeyError:
        data[key_1] = 'empty'

    return data


async def get_data_person(id_):
    HOST = 'https://swapi.dev/api/people/'
    async with aiohttp.client.ClientSession() as session:
        async with session.get(HOST + f'{id_}') as response:
            all_data = await response.json()
            all_data['id'] = id_
            await converts_to_a_string(session, all_data, 'films', 'title')
            await converts_to_a_string(session, all_data, 'species', 'name')
            await converts_to_a_string(session, all_data, 'starships', 'name')
            await converts_to_a_string(session, all_data, 'vehicles', 'name')
            if all_data['homeworld']:
                async with session.get(all_data['homeworld']) as resp:
                    all_data['homeworld'] = (await resp.json()).get('name', 'empty')
            else:
                all_data['homeworld'] = 'empty'

            return all_data


async def writing_to_the_database(id_):
    data = await get_data_person(id_)
    validate_data = validator_model(data, PersonModel)
    Session = await get_session(engine)
    async with Session() as session:
        new_person = Person(**validate_data)
        session.add(new_person)
        await session.commit()


async def main():
    tasks = []
    for index in range(1, 11):
        task = asyncio.create_task(writing_to_the_database(index))
        tasks.append(task)
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    load_dotenv()
    engine = create_async_engine(os.getenv("ENGINE"), echo=True)
    # asyncio.run(create_tables(engine))
    asyncio.run(main())
