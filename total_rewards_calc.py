import requests
import json


class Networks:
    polka = ["polkadot", 10]
    kusama = ["kusama", 12]
    westend = ['westend', 12]


address = "EwL4UJNYbhknJsYbbhkkKxVFNKBKBPoTj9pKiavCCp2ttM3"
current_network = Networks.kusama
rewards = 0
rewards_count = 0
slash_count = 0
slash_amount = 0
block_number = 0

if current_network == Networks.kusama:
    subquery_url = "https://api.subquery.network/sq/OnFinality-io/sum-reward-kusama"
else:
    subquery_url = "https://api.subquery.network/sq/OnFinality-io/sum-reward"
query = "{sumReward   (id: \"%s\")\n   {accountTotal}\n}" % (address)

subquery_payload = {"query": query}

subscan_reward_url = "https://{}.subscan.io/api/scan/account/reward_slash".format(
    current_network[0])
subscan_extrinsic_url = "https://{}.api.subscan.io/api/scan/extrinsics".format(
    current_network[0])
subscan_payload = {"row": 100, "address": address, "page": 0}
n = 0


def payload_creator(address, n):
    return json.dumps({
        "address": address,
        "row": 100,
        "page": n
    })


headers = {
    'Content-Type': 'application/json',
    'x-api-key': 'd5a1d1cffde69e7cbff6d9c0cf1cca6d'
}

subscan_response = requests.request("POST", subscan_reward_url, headers=headers,
                                    data=payload_creator(address, n)).json()
count = int(subscan_response.get("data").get("count"))
request_count = count/100

while n < request_count:
    new_subscan_response = requests.request("POST", subscan_reward_url, headers=headers, data=payload_creator(
        address, n)).json()
    list_iterator = iter(new_subscan_response.get("data").get("list"))
    for i in list_iterator:
        current_block = i.get("block_num")
        current_ivent_id = i.get("event_id")
        current_amount = i.get("amount")
        if block_number == 0:
            block_number = current_block
        if block_number > current_block:
            block_number = current_block
        if current_ivent_id != "Reward":
            print(i)
        if current_ivent_id == "Slash":
            rewards = rewards - float(current_amount)
            slash_count += 1
            slash_amount = slash_amount + float(current_amount)
            continue
        rewards = rewards + float(current_amount)
        rewards_count += 1
    n += 1

subquery_response = requests.request("POST", subquery_url, headers=headers,
                                     data=json.dumps(subquery_payload)).json()

subscan_extrinsic_response = requests.request("POST", subscan_extrinsic_url, headers=headers,
                                              data=json.dumps(subscan_payload)).json()
list_iterator = iter(subscan_extrinsic_response.get("data").get("extrinsics"))
bond_value = 0
reward_destination = ''
for i in list_iterator:
    json_representation = json.loads(i.get("params"))
    call_module_function = i.get("call_module_function")
    if call_module_function == 'bond':
        bond_value = bond_value + float(json_representation[1].get("value"))
        reward_destination = json_representation[2].get("value")
    if call_module_function == 'unbond':
        bond_value = bond_value - float(json_representation[0].get("value"))
    if call_module_function == 'bond_extra':
        bond_value = bond_value + float(json_representation[0].get("value"))
    if call_module_function == 'rebond':
        bond_value = bond_value + float(json_representation[0].get("value"))
    if call_module_function == 'batch':
        bond_value = bond_value + float(json_representation[0].get("value")[0].get("call_args")[1].get("value"))




print("Bond amount: {}".format(bond_value/10**current_network[1]))
print("Reward destination: {}".format(reward_destination))
print("Account address: {}".format(address))
print("First block with rewards from subscan: {}".format(block_number))
print("Rewards count: {}, Slash count: {}, Slash amount: {}".format(
    rewards_count, slash_count, slash_amount/10**current_network[1]))
print("Subscan results:  {}".format(rewards/10**current_network[1]))
print("Subquery results: {}".format(float(subquery_response.get(
    "data").get("sumReward").get("accountTotal"))/10**current_network[1]))
print("Locked balance with subscan result: {}".format(bond_value/10**current_network[1]+rewards/10**current_network[1]))
print("Locked balance with subquery result: {}".format(bond_value/10**current_network[1]+float(subquery_response.get(
    "data").get("sumReward").get("accountTotal"))/10**current_network[1]))
