import asyncio

import aiohttp

from models import save_person_in_db

API_ENDPOINT = 'https://swapi.dev/api/people'




async def get_person(person_id: int) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{API_ENDPOINT}/{person_id}') as response:
            response = await response.json()
            return response


async def main():
    result = await asyncio.gather(*[get_person(i) for i in range(1, 10)])
    return result


if __name__ == "__main__":
    asyncio.run(save_person_in_db(asyncio.run(main())))
