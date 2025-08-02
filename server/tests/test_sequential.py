import requests
import threading
import time

def make_request(text, request_id, key):
    """Make a request to the obsidize endpoint with a specific key"""
    start_time = time.time()
    print(f"Request {request_id} (key: {key}) starting at {start_time}")
    
    try:
        response = requests.post(
            'http://localhost:5000/obsidize',
            json={'input': f'Request {request_id}: {text}', 'key': key},
            timeout=30
        )
        end_time = time.time()
        print(f"Request {request_id} (key: {key}) completed at {end_time} (took {end_time - start_time:.2f}s)")
        return response.json()
    except Exception as e:
        print(f"Request {request_id} (key: {key}) failed: {e}")

def test_same_key_sequential():
    """Test that requests with the same key are processed sequentially"""
    print("\n=== Testing SAME KEY (should be sequential) ===")
    print("Starting 3 requests with key 'user1'...")
    
    threads = []
    for i in range(3):
        thread = threading.Thread(
            target=make_request, 
            args=(f"Same key test {i+1}", f"A{i+1}", "user1")
        )
        threads.append(thread)
    
    # Start all threads at roughly the same time
    start_time = time.time()
    for thread in threads:
        thread.start()
    
    # Wait for all to complete
    for thread in threads:
        thread.join()
    
    total_time = time.time() - start_time
    print(f"Same key requests completed in {total_time:.2f} seconds")
    print("These should have run one after another (sequential)")

def test_different_keys_parallel():
    """Test that requests with different keys can run in parallel"""
    print("\n=== Testing DIFFERENT KEYS (should be parallel) ===")
    print("Starting 3 requests with different keys...")
    
    threads = []
    keys = ["user1", "user2", "user3"]
    for i in range(3):
        thread = threading.Thread(
            target=make_request, 
            args=(f"Different key test {i+1}", f"B{i+1}", keys[i])
        )
        threads.append(thread)
    
    # Start all threads at roughly the same time
    start_time = time.time()
    for thread in threads:
        thread.start()
    
    # Wait for all to complete
    for thread in threads:
        thread.join()
    
    total_time = time.time() - start_time
    print(f"Different key requests completed in {total_time:.2f} seconds")
    print("These should have run in parallel (overlapping times)")

def test_mixed_scenario():
    """Test mixed scenario: some same keys, some different keys"""
    print("\n=== Testing MIXED SCENARIO ===")
    print("Starting 6 requests: 2x user1, 2x user2, 2x user3...")
    
    requests_config = [
        ("Mixed test 1A", "C1", "user1"),
        ("Mixed test 1B", "C2", "user1"),  # Same as C1, should be sequential
        ("Mixed test 2A", "C3", "user2"),
        ("Mixed test 2B", "C4", "user2"),  # Same as C3, should be sequential
        ("Mixed test 3A", "C5", "user3"),
        ("Mixed test 3B", "C6", "user3"),  # Same as C5, should be sequential
    ]
    
    threads = []
    for text, request_id, key in requests_config:
        thread = threading.Thread(
            target=make_request, 
            args=(text, request_id, key)
        )
        threads.append(thread)
    
    # Start all threads at roughly the same time
    start_time = time.time()
    for thread in threads:
        thread.start()
    
    # Wait for all to complete
    for thread in threads:
        thread.join()
    
    total_time = time.time() - start_time
    print(f"Mixed scenario completed in {total_time:.2f} seconds")
    print("Expected: user1 requests sequential, user2 requests sequential, user3 requests sequential")
    print("But all three groups should run in parallel with each other")

def test_per_key_sequential_execution():
    """Test the complete per-key sequential execution behavior"""
    print("🧪 Testing Per-Key Sequential Execution")
    print("=" * 50)
    
    # Test 1: Same key should be sequential
    test_same_key_sequential()
    
    time.sleep(2)  # Brief pause between tests
    
    # Test 2: Different keys should be parallel
    test_different_keys_parallel()
    
    time.sleep(2)  # Brief pause between tests
    
    # Test 3: Mixed scenario
    test_mixed_scenario()
    
    print("\n" + "=" * 50)
    print("✅ Per-key sequential testing complete!")
    print("Check the timestamps above to verify:")
    print("  - Same key requests run one after another")
    print("  - Different key requests overlap in time")

if __name__ == "__main__":
    test_per_key_sequential_execution() 