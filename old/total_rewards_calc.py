import requests
import json


class Networks:
    polka = ["polkadot", 10]
    kusama = ["kusama", 12]
    westend = ['westend', 12]


address = "13mAjFVjFDpfa42k2dLdSnUyrSzK8vAySsoudnxX2EKVtfaq"
current_network = Networks.polka


rewards = 0
rewards_count = 0
slash_count = 0
slash_amount = 0
block_number = 0
bond_value = 0

class SubQuery:
    def __init__(self):
        self.rewards_test_url = "https://api.subquery.network/sq/jiqiang90/staking-records"
        rewards_test_payload = "{\n    stakingRewards (filter:{address:{equalTo:\"%s\"}}) {\n        totalCount\n        nodes {\n            id\n            address\n            balance\n            date\n        }\n    edges{\n      cursor\n      node{\n        id\n        address\n        balance\n        date\n        createdAt\n        updatedAt\n      }\n    }\n    }\n  sumRewards(filter:{id:{equalTo: \"%s\"}}){\n  \tnodes{\n      id\n      accountReward\n      accountSlash\n      accountTotal\n      createdAt\n      updatedAt\n    }\n    edges{\n      cursor\n      node{\n        id\n        accountReward\n        accountSlash\n        accountTotal\n        createdAt\n        updatedAt\n      }\n    }\n    pageInfo{\n      hasNextPage\n      hasPreviousPage\n      startCursor\n      endCursor\n    }\n    totalCount\n  }\n}" % (address, address)
        self.rewards_test_query = {"query": rewards_test_payload}

        if current_network == Networks.kusama:
            self.url = "https://api.subquery.network/sq/OnFinality-io/sum-reward-kusama"
        else:
            self.url = "https://api.subquery.network/sq/OnFinality-io/sum-reward"
        query = "{sumReward   (id: \"%s\")\n   {accountTotal}\n}" % (address)
        self.payload = {"query": query}
        self.rewards_list = list()

class SubScan:
    def __init__(self):
        self.reward_url = "https://{}.api.subscan.io/api/scan/account/reward_slash".format(current_network[0])
        self.extrinsic_url = "https://{}.api.subscan.io/api/scan/extrinsics".format(current_network[0])
        self.rewards_list = list()


def payload_creator(address, n):
    return json.dumps({
        "address": address,
        "row": 100,
        "page": n
    })

def send_request(url, data):
    headers = {
    'Content-Type': 'application/json',
    'x-api-key': 'd5a1d1cffde69e7cbff6d9c0cf1cca6d'
    }
    return requests.request("POST", url, headers=headers,
                                    data=data)

# Initial data
subscan = SubScan()
subquery = SubQuery()

# Get data from SubScan
subscan_response = send_request(subscan.reward_url, payload_creator(address, 0)).json()
x = subscan_response
count = int(subscan_response.get("data").get("count"))
request_count = count/100

n = 0
while n < request_count:
    new_subscan_response = send_request(subscan.reward_url, payload_creator(address, n)).json()
    list_iterator = iter(new_subscan_response.get("data").get("list"))
    for i in list_iterator:
        current_block = i.get("block_num")
        current_ivent_id = i.get("event_id")
        current_amount = i.get("amount")
        subscan.rewards_list.append(i)
        if block_number == 0:
            block_number = current_block
        if block_number > current_block:
            block_number = current_block
        if current_ivent_id != "Reward" and "Slash":
            print(i)
        if current_ivent_id == "Slash":
            rewards = rewards - float(current_amount)
            slash_count += 1
            slash_amount = slash_amount + float(current_amount)
            continue
        rewards = rewards + float(current_amount)
        rewards_count += 1
    n += 1

# Get data from SubQuery
total_rewards_subquery_response = send_request(subquery.url, json.dumps(subquery.payload)).json()
subscan_extrinsic_response = send_request(subscan.extrinsic_url, payload_creator(address, 0)).json()
try:
    list_iterator = iter(subscan_extrinsic_response.get("data").get("extrinsics"))
except:
    print("Extrinsic is None: ",subscan_extrinsic_response)

for i in list_iterator:
    try:
        json_representation = json.loads(i.get("params"))
    except:
        print("Extrinsic params is null")
    call_module_function = i.get("call_module_function")
    if call_module_function == 'bond':
        bond_value = bond_value + float(json_representation[1].get("value"))
    if call_module_function == 'unbond':
        bond_value = bond_value - float(json_representation[0].get("value"))
    if call_module_function == 'bond_extra':
        bond_value = bond_value + float(json_representation[0].get("value"))
    if call_module_function == 'rebond':
        bond_value = bond_value + float(json_representation[0].get("value"))
    if call_module_function == 'batch':
        try:
            bond_value = bond_value + float(json_representation[0].get("value")[0].get("call_args")[1].get("value"))
        except:
            print("It's not staking batch",i)

subquery_compare_rewards_responce = send_request(subquery.rewards_test_url, json.dumps(subquery.rewards_test_query)).json()
list_subquery_wdges = iter(subquery_compare_rewards_responce.get("data").get("stakingRewards").get("edges"))

for i in list_subquery_wdges:
    subquery.rewards_list.append(i)


result_reward_list = subscan.rewards_list.copy()
for subs in subscan.rewards_list:
    amount_subscan = subs.get('amount')
    for subq in subquery.rewards_list:
        amount_subquery = subq.get('node').get('balance')
        if amount_subscan == amount_subquery:
            z=0
            for item in result_reward_list:
                if item.get("amount") == amount_subscan:
                    result_reward_list.pop(z)
                z+=1
            break

def hashes_and_blocks(difference_list):
    for item in difference_list:
        print("Block: {}\n Hash: {}\n Amount: {}\n".format(item.get("block_num"),item.get("extrinsic_hash"),item.get("amount")))

print("Bond amount: {}".format(bond_value/10**current_network[1]))
print("Account address: {}".format(address))
print("*** Subscan result: ***")
print("First block with rewards: {}".format(block_number))
print("SubScan rewards count: {}, Slash count: {}, Slash amount: {}".format(
    rewards_count, slash_count, slash_amount/10**current_network[1]))
print("Total rewards from Subscan:  {}".format(rewards/10**current_network[1]))
print("Locked balance: {}".format(bond_value/10**current_network[1]+rewards/10**current_network[1]))
print("\n")
print("*** SubQuery production result: ***")
print("Total rewards from Subquery: {}".format(float(total_rewards_subquery_response.get(
    "data").get("sumReward").get("accountTotal"))/10**current_network[1]))
print("Locked balance: {}".format(bond_value/10**current_network[1]+float(total_rewards_subquery_response.get(
    "data").get("sumReward").get("accountTotal"))/10**current_network[1]))
print("\n")
print("*** SubQuery test result: ***")
print("Subquery_test rewards count: {}".format(subquery_compare_rewards_responce.get("data").get("stakingRewards").get("totalCount")))
print("Subquery_test rewards amount: {}".format(float(subquery_compare_rewards_responce.get("data").get("sumRewards").get("edges")[0].get("node").get("accountTotal"))/10**current_network[1]))
print("Locked balance: {}".format(bond_value/10**current_network[1]+float(subquery_compare_rewards_responce.get("data").get("sumRewards").get("edges")[0].get("node").get("accountTotal"))/10**current_network[1]))


if current_network == Networks.polka:
    print("===========")
    print("Difference betwen SubScan and test SubQuery is {} extrinsics".format(len(result_reward_list)))
    hashes_and_blocks(result_reward_list)