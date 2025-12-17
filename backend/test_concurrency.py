import asyncio
import httpx
import time
import random

# CONFIGURATION
API_URL = "http://127.0.0.1:8000/api/v1/mf/recommendations"
# Replace with the actual User ID existing in your database
TEST_USER_ID = "3767f181-eadb-4ac2-8b41-450954659cc3" 
CONCURRENT_REQUESTS = 20  # Increased to stress-test single document access

async def fetch_recommendation(client, user_id):
    """
    Fetches recommendation for a single user.
    """
    start_time = time.time()
    try:
        response = await client.get(f"{API_URL}/{user_id}")
        elapsed = time.time() - start_time
        return {
            "user_id": user_id,
            "status": response.status_code,
            "time": elapsed,
            "success": response.status_code == 200
        }
    except Exception as e:
        return {
            "user_id": user_id,
            "status": "ERROR",
            "time": time.time() - start_time,
            "success": False,
            "error": str(e)
        }

async def run_concurrency_test():
    print(f"Starting Concurrency Test with {CONCURRENT_REQUESTS} simultaneous requests for User ID: {TEST_USER_ID}...")
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = []
        for _ in range(CONCURRENT_REQUESTS):
            # All requests target the same user to test single-document read concurrency
            tasks.append(fetch_recommendation(client, TEST_USER_ID))
        
        # Run all requests simultaneously
        results = await asyncio.gather(*tasks)

    # analyze results
    success_count = sum(1 for r in results if r["success"])
    fail_count = len(results) - success_count
    avg_time = sum(r["time"] for r in results) / len(results)
    
    print("\nTEST RESULTS")
    print("=" * 30)
    print(f"Total Requests: {len(results)}")
    print(f"Successful:     {success_count}")
    print(f"Failed:         {fail_count}")
    print(f"Avg Response:   {avg_time:.4f} seconds")
    print("=" * 30)
    
    # Detail on failures
    if fail_count > 0:
        for r in results:
            if not r["success"]:
                print(f"Failed User {r['user_id']}: Status {r['status']}")

if __name__ == "__main__":
    # Ensure the API is running before executing this
    try:
        asyncio.run(run_concurrency_test())
    except KeyboardInterrupt:
        print("Test stopped.")
