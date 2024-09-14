import time
import httpx
from concurrent.futures import ThreadPoolExecutor


def benchmark_llm_api(url: str, total_requests: int, concurrent_requests: int):
    start_time = time.time()
    success = 0

    body = {
        "system_prompt": "You are a helpful assistant.",
        "user_prompt": "Hello, how are you?",
    }

    def send_request():
        nonlocal success
        try:
            response = httpx.post(url, json=body, timeout=300)
            if response.status_code == 200:
                success += 1
        except Exception as e:
            print(f"Request failed: {e}")

    with ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
        for _ in range(total_requests):
            executor.submit(send_request)

    end_time = time.time()
    duration = end_time - start_time
    print(
        f"Sent {total_requests} requests with {concurrent_requests} concurrent workers."
    )
    print(f"Successful requests: {success}")
    print(f"Total time: {duration:.2f} seconds")
    print(f"Requests per second: {total_requests / duration:.2f}")


if __name__ == "__main__":
    import os

    benchmark_llm_api(
        os.getenv("BENCH_LALA_ENDPOINT", "http://localhost:8000/chat"),
        total_requests=int(os.getenv("BENCH_LALA_TOTAL_REQUESTS", "100")),
        concurrent_requests=int(os.getenv("BENCH_LALA_CONCURRENT_REQUESTS", "10")),
    )

""" 
Baseline llama mac cpu run
Sent 20 requests with 10 concurrent workers.
Successful requests: 0
Total time: 44.64 seconds
Requests per second: 0.45
"""
