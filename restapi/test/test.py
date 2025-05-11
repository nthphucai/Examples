import asyncio
import time

async def fetch_data(url):
    """
    Fetches data from a URL asynchronously.

    Args:
        url: The URL to fetch data from.

    Returns:
        The fetched data.
    """
    # Simulate an I/O-bound operation (e.g., fetching data from a website)
    await asyncio.sleep(1)  # Simulate a 1-second delay
    return f"Data from {url}"

async def main_async():
    """
    Fetches data from multiple URLs asynchronously.
    """
    urls = ["https://www.example1.com", "https://www.example2.com", "https://www.example3.com"]
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)

def main_sync():
    """
    Fetches data from multiple URLs synchronously.
    """
    urls = ["https://www.example1.com", "https://www.example2.com", "https://www.example3.com"]
    results = []
    start_time = time.time()
    for url in urls:
        result = fetch_data(url)  # This will block until the function completes
        results.append(result)
    end_time = time.time()
    print(f"\nSynchronous execution time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main_async())
    end_time = time.time()
    print(f"Asynchronous execution time: {end_time - start_time:.2f} seconds")

    main_sync()