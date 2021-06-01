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

if current_network==Networks.kusama: subquery_url = "https://api.subquery.network/sq/OnFinality-io/sum-reward-kusama"
else: subquery_url = "https://api.subquery.network/sq/OnFinality-io/sum-reward"
query = "{sumReward   (id: \"%s\")\n   {accountTotal}\n}"%(address)

subquery_payload = {
	"query": query
}

subscan_url = "https://{}.subscan.io/api/scan/account/reward_slash".format(
    current_network[0])
n = 0

def payload_creator(address, n):
    return json.dumps({
        "address": address,
        "row": 100,
        "page": n
    })


headers = {
    'Content-Type': 'application/json'
}

subscan_response = requests.request("POST", subscan_url, headers=headers,
                     data=payload_creator(address, n)).json()
count = int(subscan_response.get("data").get("count"))
request_count = count/100

while n < request_count:
    new_subscan_response = requests.request("POST", subscan_url, headers=headers, data=payload_creator(
        address, n)).json()
    list_iterator = iter(new_subscan_response.get("data").get("list"))
    for i in list_iterator:
        current_block = i.get("block_num")
        current_ivent_id = i.get("event_id")
        current_amount = i.get("amount")
        if block_number == 0: block_number = current_block
        if block_number > current_block: block_number = current_block
        if current_ivent_id != "Reward":
            print(i)
        if current_ivent_id == "Slash":
            rewards = rewards - float(current_amount)
            slash_count+=1
            slash_amount = slash_amount + float(current_amount)
            continue
        rewards = rewards + float(current_amount)
        rewards_count+=1
    n += 1

subquery_response = requests.request("POST", subquery_url, headers=headers,
                     data=json.dumps(subquery_payload)).json()

print("Account address: {}".format(address))
print("First block with rewards from subscan: {}".format(block_number))
print("Rewards count: {}, Slash count: {}, Slash amount: {}".format(rewards_count, slash_count, slash_amount/10**current_network[1]))
print("Subscan results:  {}".format(rewards/10**current_network[1]))
print("Subquery results: {}".format(float(subquery_response.get("data").get("sumReward").get("accountTotal"))/10**current_network[1]))