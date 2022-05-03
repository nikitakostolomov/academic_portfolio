import asyncio
from hfc.fabric import Client

loop = asyncio.get_event_loop()
cli = Client(net_profile="test/fixtures/network.json")
org1_admin = cli.get_user('org1.example.com', 'Admin')
print(cli._channels)

# first get the hash by calling 'query_info'
response = loop.run_until_complete(cli.query_info(
               requestor=org1_admin,
               channel_name='businesschannel',
               peers=['peer0.org1.example.com'],
               decode=True
               ))

"""
# An example response:

height: 3
currentBlockHash: "\\\255\317\341$\"\371\242aP\030u\325~\263!\352G\014\007\353\353\247\235<\353\020\026\345\254\252r"
previousBlockHash: "\324\214\275z\301)\351\224 \225\306\"\250jBMa\3432r\035\023\310\250\017w\013\303!f\340\272"
"""

test_hash = response.currentBlockHash

response = loop.run_until_complete(cli.query_block_by_hash(
               requestor=org1_admin,
               channel_name='businesschannel',
               peers=['peer0.org1.example.com'],
               block_hash=test_hash,
               decode=True
               ))

tx_id = response.get('data').get('data')[0].get(
    'payload').get('header').get(
    'channel_header').get('tx_id')

response = loop.run_until_complete(cli.query_block_by_txid(
               requestor=org1_admin,
               channel_name='businesschannel',
               peers=['peer0.org1.example.com'],
               tx_id=tx_id,
               decode=True
               ))