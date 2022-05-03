import asyncio
from hfc.fabric import Client

loop = asyncio.get_event_loop()
cli = Client(net_profile="test/fixtures/network.json")
org1_admin = cli.get_user('org1.example.com', 'Admin')

# Query Peer installed chaincodes, make sure the chaincode is installed
response = loop.run_until_complete(cli.query_installed_chaincodes(
               requestor=org1_admin,
               peers=['peer0.org1.example.com'],
               decode=True
               ))
print(response)
"""
# An example response:

chaincodes {
  name: "example_cc"
  version: "v1.0"
  path: "github.com/example_cc"
  id: "\374\361\027j(\332\225\367\253\030\242\303U&\356\326\241\2003|\033\266:\314\250\032\254\221L#\006G"
}
"""

# Query Peer Joined channel
response = loop.run_until_complete(cli.query_channels(
               requestor=org1_admin,
               peers=['peer0.org1.example.com'],
               decode=True
               ))
print(response)
"""
# An example response:

channels {
  channel_id: "businesschannel"
}
"""