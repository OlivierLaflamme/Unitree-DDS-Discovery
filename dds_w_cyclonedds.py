#!/usr/bin/env python3
import os
import time
from cyclonedds.domain import DomainParticipant
from cyclonedds.sub import DataReader
from cyclonedds.topic import Topic
from cyclonedds.core import Qos, Policy
from cyclonedds.builtin import BuiltinDataReader, BuiltinTopicDcpsSubscription, BuiltinTopicDcpsPublication

os.environ['CYCLONEDDS_URI'] = '''<CycloneDDS>
  <Domain id="0">
    <General>
      <NetworkInterfaceAddress>en0</NetworkInterfaceAddress>
    </General>
    <Discovery>
      <Peers>
        <Peer address="192.168.123.161"/>
      </Peers>
    </Discovery>
  </Domain>
</CycloneDDS>'''

print("[*] Joining DDS domain 0...")
print("[*] Discovering topics from robot at 192.168.123.161...")

dp = DomainParticipant(0)
time.sleep(10)

try:
    # Get publications (DataWriters on the robot)
    pub_reader = BuiltinDataReader(dp, BuiltinTopicDcpsPublication)
    pubs = pub_reader.take(100)
    
    topics_found = set()
    for pub in pubs:
        if hasattr(pub, 'topic_name'):
            topics_found.add(pub.topic_name)
    
    if topics_found:
        print(f"[+] Found {len(topics_found)} active topics:")
        for topic in sorted(topics_found):
            print(f"    → {topic}")
    else:
        print("[!] No topics discovered")
    
except Exception as e:
    print(f"[!] Could not read builtin topics: {e}")