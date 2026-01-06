#!/usr/bin/env python3
import time
import sys
import subprocess

# Check Unitree SDK
try:
    from unitree_sdk2py.core.channel import ChannelSubscriber, ChannelPublisher
    from unitree_sdk2py.idl.unitree_go.msg.dds_ import LowState_
    SDK_VERSION = "new"
except ImportError:
    try:
        from unitree_sdk2py.go2.robot_state.robot_state_client import RobotStateClient
        SDK_VERSION = "old"
    except ImportError:
        print("[!] Cannot find unitree_sdk2py")
        print("    cd ~/unitree_sdk2_python && pip3 install -e .")
        sys.exit(1)

# Check cyclonedds
try:
    from cyclonedds.domain import DomainParticipant
    from cyclonedds.topic import Topic
    from cyclonedds.util import duration
except ImportError:
    print("[!] cyclonedds not found")
    print("    pip3 install cyclonedds")
    sys.exit(1)

print("[*] Creating DDS participant on domain 0...")
dp = DomainParticipant(0)

print("[*] Waiting for discovery...")
time.sleep(5)

# Get topics
try:
    result = subprocess.run(['ddsls', '-a'], capture_output=True, text=True, timeout=5)
    if result.returncode == 0 and result.stdout:
        print("[+] Available topics:")
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                print(f"    {line}")
        
        if 'rt/api/programming_actuator/request' in result.stdout:
            print("\n[+] programming_actuator found - exploit ready")
    else:
        print("[!] ddsls failed")
except:
    print("[!] ddsls not installed")