import asyncio
import aiohttp

async def fetch_urls(urls: list):
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [await response.text() for response in responses]

# teste da função
if __name__ == "__main__":
    urls = ['https://dummyjson.com/users', 'https://dummyjson.com/posts', 'https://dummyjson.com/carts']
    results = asyncio.run(fetch_urls(urls))
    for i, content in enumerate(results, 1):
        print(f"Conteúdo da URL {i}:\n", content[:200], "\n---")
