"""
Test API endpoints and measure response times
"""
import requests
import time
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api/fitness"

def test_endpoint(method, url, data=None, params=None):
    """Test an API endpoint and measure response time"""
    try:
        start_time = time.time()
        if method == 'GET':
            response = requests.get(url, params=params, timeout=5)
        elif method == 'POST':
            response = requests.post(url, json=data, timeout=5)
        elif method == 'PUT':
            response = requests.put(url, json=data, timeout=5)
        elif method == 'DELETE':
            response = requests.delete(url, timeout=5)
        else:
            return None, None, "Invalid method"
        
        elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        return response.status_code, elapsed_time, response.text
    except requests.exceptions.ConnectionError:
        return None, None, "Connection refused - Server not running"
    except requests.exceptions.Timeout:
        return None, None, "Request timeout"
    except Exception as e:
        return None, None, str(e)

def main():
    """Test all fitness API endpoints"""
    print("\n" + "="*60)
    print("TESTING FITNESS API ENDPOINTS")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    print(f"Timestamp: {datetime.now().isoformat()}\n")
    
    results = {}
    
    # Test Exercises endpoints
    print("Testing Exercises endpoints...")
    status, elapsed, response = test_endpoint('GET', f"{BASE_URL}/exercises/")
    results['exercises_list'] = {
        'status': status,
        'response_time_ms': elapsed,
        'response': response[:200] if response else None,
        'success': status == 200 if status else False
    }
    print(f"  GET /exercises/ - Status: {status}, Time: {elapsed:.2f}ms" if elapsed else f"  GET /exercises/ - Status: {status}, Error: {response}")
    
    # Test with filters
    status, elapsed, response = test_endpoint('GET', f"{BASE_URL}/exercises/", params={'type': 'cardio'})
    results['exercises_filter_type'] = {
        'status': status,
        'response_time_ms': elapsed,
        'success': status == 200 if status else False
    }
    print(f"  GET /exercises/?type=cardio - Status: {status}, Time: {elapsed:.2f}ms" if elapsed else f"  GET /exercises/?type=cardio - Status: {status}")
    
    status, elapsed, response = test_endpoint('GET', f"{BASE_URL}/exercises/", params={'difficulty': 'media'})
    results['exercises_filter_difficulty'] = {
        'status': status,
        'response_time_ms': elapsed,
        'success': status == 200 if status else False
    }
    print(f"  GET /exercises/?difficulty=media - Status: {status}, Time: {elapsed:.2f}ms" if elapsed else f"  GET /exercises/?difficulty=media - Status: {status}")
    
    # Test Routines endpoints
    print("\nTesting Routines endpoints...")
    status, elapsed, response = test_endpoint('GET', f"{BASE_URL}/routines/")
    results['routines_list'] = {
        'status': status,
        'response_time_ms': elapsed,
        'response': response[:200] if response else None,
        'success': status == 200 if status else False
    }
    print(f"  GET /routines/ - Status: {status}, Time: {elapsed:.2f}ms" if elapsed else f"  GET /routines/ - Status: {status}, Error: {response}")
    
    status, elapsed, response = test_endpoint('GET', f"{BASE_URL}/routines/", params={'is_template': 'true'})
    results['routines_filter_template'] = {
        'status': status,
        'response_time_ms': elapsed,
        'success': status == 200 if status else False
    }
    print(f"  GET /routines/?is_template=true - Status: {status}, Time: {elapsed:.2f}ms" if elapsed else f"  GET /routines/?is_template=true - Status: {status}")
    
    # Test Progress endpoints
    print("\nTesting Progress endpoints...")
    status, elapsed, response = test_endpoint('GET', f"{BASE_URL}/progress/")
    results['progress_list'] = {
        'status': status,
        'response_time_ms': elapsed,
        'response': response[:200] if response else None,
        'success': status == 200 if status else False
    }
    print(f"  GET /progress/ - Status: {status}, Time: {elapsed:.2f}ms" if elapsed else f"  GET /progress/ - Status: {status}, Error: {response}")
    
    # Test Recommendations endpoints
    print("\nTesting Recommendations endpoints...")
    status, elapsed, response = test_endpoint('GET', f"{BASE_URL}/recommendations/")
    results['recommendations_list'] = {
        'status': status,
        'response_time_ms': elapsed,
        'response': response[:200] if response else None,
        'success': status == 200 if status else False
    }
    print(f"  GET /recommendations/ - Status: {status}, Time: {elapsed:.2f}ms" if elapsed else f"  GET /recommendations/ - Status: {status}, Error: {response}")
    
    # Test Follow-ups endpoints
    print("\nTesting Follow-ups endpoints...")
    status, elapsed, response = test_endpoint('GET', f"{BASE_URL}/followups/")
    results['followups_list'] = {
        'status': status,
        'response_time_ms': elapsed,
        'response': response[:200] if response else None,
        'success': status == 200 if status else False
    }
    print(f"  GET /followups/ - Status: {status}, Time: {elapsed:.2f}ms" if elapsed else f"  GET /followups/ - Status: {status}, Error: {response}")
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    successful = sum(1 for r in results.values() if r.get('success', False))
    total = len(results)
    print(f"Successful requests: {successful}/{total}")
    
    if successful > 0:
        avg_time = sum(r.get('response_time_ms', 0) for r in results.values() if r.get('response_time_ms')) / successful
        print(f"Average response time: {avg_time:.2f}ms")
    
    return results

if __name__ == "__main__":
    main()

