import asyncio
import aiohttp
from models import save_person_in_db

API_ENDPOINT = 'https://swapi.dev/api/people'

async def get_film_title(film_url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(film_url) as response:
            film_data = await response.json()
            return film_data.get('title', '')


async def main():
    result = await asyncio.gather(*[get_person(i) for i in range(1, 10)])
    return result


if __name__ == "__main__":
    asyncio.run(save_person_in_db(asyncio.run(main())))
