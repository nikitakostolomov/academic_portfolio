import asyncio
from hfc.fabric import Client

loop = asyncio.get_event_loop()

cli = Client(net_profile="test/fixtures/network.json")
org1_admin = cli.get_user(org_name='org1.example.com', name='Admin')

config_tx_file = './configtx.yaml'

orderer_admin = cli.get_user(org_name='orderer.example.com', name='Admin')
loop.run_until_complete(cli.channel_update(
        orderer='orderer.example.com',
        channel_name='businesschannel',
        requestor=orderer_admin,
        config_tx=config_tx_file))