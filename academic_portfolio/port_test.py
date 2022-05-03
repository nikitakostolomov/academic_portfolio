import asyncio
from hfc.fabric import Client

loop = asyncio.get_event_loop()

cli = Client(net_profile="test/fixtures/network.json")
org1_admin = cli.get_user(org_name='org1.example.com', name='Admin')

# Create a New Channel, the response should be true if succeed
response = loop.run_until_complete(cli.channel_create(
            orderer='orderer.example.com',
            channel_name='businesschannel',
            requestor=org1_admin,
            config_yaml='C:/Projects/hf/fabric-sdk-py/test/fixtures/e2e_cli/',
            channel_profile='TwoOrgsChannel',
            # config_tx='test/fixtures/e2e_cli/configtx.yaml'
            ))
print(response == True)

# Join Peers into Channel, the response should be true if succeed
orderer_admin = cli.get_user(org_name='orderer.example.com', name='Admin')
responses = loop.run_until_complete(cli.channel_join(
               requestor=org1_admin,
               channel_name='businesschannel',
               peers=['peer0.org1.example.com',
                      'peer1.org1.example.com'],
               orderer='orderer.example.com'
               ))
print(len(responses) == 2)


# Join Peers from a different MSP into Channel
org2_admin = cli.get_user(org_name='org2.example.com', name='Admin')

# For operations on peers from org2.example.com, org2_admin is required as requestor
responses = loop.run_until_complete(cli.channel_join(
               requestor=org2_admin,
               channel_name='businesschannel',
               peers=['peer0.org2.example.com',
                      'peer1.org2.example.com'],
               orderer='orderer.example.com'
               ))
print(len(responses) == 2)

# Make the client know there is a channel in the network
cli.new_channel('businesschannel')

# Install Example Chaincode to Peers
# GOPATH setting is only needed to use the example chaincode inside sdk
import os
gopath_bak = os.environ.get('GOPATH', '')
gopath = os.path.normpath(os.path.join(
                      os.path.dirname(os.path.realpath('__file__')),
                      'test/fixtures/chaincode'
                     ))
os.environ['GOPATH'] = os.path.abspath(gopath)

# The response should be true if succeed
responses = loop.run_until_complete(cli.chaincode_install(
               requestor=org1_admin,
               peers=['peer0.org1.example.com',
                      'peer1.org1.example.com'],
               cc_path='github.com/academic_port',
               cc_name='af_cc',
               cc_version='v1.0'
               ))

# Instantiate Chaincode in Channel, the response should be true if succeed
args = ['a', '200', 'b', '300']

# policy, see https://hyperledger-fabric.readthedocs.io/en/release-1.4/endorsement-policies.html
policy = {
    'identities': [
        {'role': {'name': 'member', 'mspId': 'Org1MSP'}},
    ],
    'policy': {
        '1-of': [
            {'signed-by': 0},
        ]
    }
}
response = loop.run_until_complete(cli.chaincode_instantiate(
               requestor=org1_admin,
               channel_name='businesschannel',
               peers=['peer0.org1.example.com'],
               args=[],
               cc_name='af_cc',
               cc_version='v1.0',
               # cc_endorsement_policy=policy, # optional, but recommended
               collections_config=None, # optional, for private data policy
               transient_map=None, # optional, for private data
               wait_for_event=True # optional, for being sure chaincode is instantiated
               ))

# # Invoke a chaincode
# args = ['a', 'b', '100']
# # The response should be true if succeed
# response = loop.run_until_complete(cli.chaincode_invoke(
#                requestor=org1_admin,
#                channel_name='businesschannel',
#                peers=['peer0.org1.example.com'],
#                args=args,
#                cc_name='example_cc',
#                transient_map=None, # optional, for private data
#                wait_for_event=True, # for being sure chaincode invocation has been commited in the ledger, default is on tx event
#                #cc_pattern='^invoked*' # if you want to wait for chaincode event and you have a `stub.SetEvent("invoked", value)` in your chaincode
#                ))
#
# # Query a chaincode
# args = ['b']
# # The response should be true if succeed
# response = loop.run_until_complete(cli.chaincode_query(
#                requestor=org1_admin,
#                channel_name='businesschannel',
#                peers=['peer0.org1.example.com'],
#                args=args,
#                cc_name='example_cc'
#                ))
#
# # Upgrade a chaincode
# # policy, see https://hyperledger-fabric.readthedocs.io/en/release-1.4/endorsement-policies.html
# # policy = {
# #     'identities': [
# #         {'role': {'name': 'member', 'mspId': 'Org1MSP'}},
# #         {'role': {'name': 'admin', 'mspId': 'Org1MSP'}},
# #     ],
# #     'policy': {
# #         '1-of': [
# #             {'signed-by': 0}, {'signed-by': 1},
# #         ]
# #     }
# # }
# # response = loop.run_until_complete(cli.chaincode_upgrade(
# #                requestor=org1_admin,
# #                channel_name='businesschannel',
# #                peers=['peer0.org1.example.com'],
# #                args=args,
# #                cc_name='example_cc',
# #                cc_version='v1.0',
# #                cc_endorsement_policy=policy, # optional, but recommended
# #                collections_config=None, # optional, for private data policy
# #                transient_map=None, # optional, for private data
# #                wait_for_event=True # optional, for being sure chaincode is upgraded
# #                ))
#
# # first get the hash by calling 'query_info'
# response = loop.run_until_complete(cli.query_info(
#                requestor=org1_admin,
#                channel_name='businesschannel',
#                peers=['peer0.org1.example.com'],
#                decode=True
#                ))
#
# """
# # An example response:
#
# height: 3
# currentBlockHash: "\\\255\317\341$\"\371\242aP\030u\325~\263!\352G\014\007\353\353\247\235<\353\020\026\345\254\252r"
# previousBlockHash: "\324\214\275z\301)\351\224 \225\306\"\250jBMa\3432r\035\023\310\250\017w\013\303!f\340\272"
# """
#
# test_hash = response.currentBlockHash
#
# response = loop.run_until_complete(cli.query_block_by_hash(
#                requestor=org1_admin,
#                channel_name='businesschannel',
#                peers=['peer0.org1.example.com'],
#                block_hash=test_hash,
#                decode=True
#                ))
#
# tx_id = response.get('data').get('data')[0].get(
#     'payload').get('header').get(
#     'channel_header').get('tx_id')
#
# response = loop.run_until_complete(cli.query_block_by_txid(
#                requestor=org1_admin,
#                channel_name='businesschannel',
#                peers=['peer0.org1.example.com'],
#                tx_id=tx_id,
#                decode=True
#                ))
# print(response)