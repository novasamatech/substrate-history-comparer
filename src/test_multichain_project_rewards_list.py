import sys
from compare_prod_and_stage import convert_to_checksum_address

from data_module.SubqueryData import SubqueryData

def compare_results(prod_rewards, stage_rewards):
    num_differences = 0
    differences = []
    
    def __dict_key_grabler(difference, grabbed_dictionary_prod, grabbed_dictionary_stage):
        for key, value in grabbed_dictionary_prod.items():
            if isinstance(value, dict):
                __dict_key_grabler(difference, value, grabbed_dictionary_stage.get(key))
            if key == 'nodeId':
                continue
            if value != grabbed_dictionary_stage.get(key):
                difference["difference"] += f"{key}: prod - {value}, stage - {stage_rewards[id].get(key)} "
        return difference
    
    for id, prod_reward in prod_rewards.items():
        if id in stage_rewards:
            difference = {"id": id, "difference": ""}
            __dict_key_grabler(difference, prod_reward, stage_rewards[id])
            if difference["difference"] != "":
                differences.append(difference)
                num_differences += 1
        else:
            differences.append({
                "id": id,
                "difference": "not found in stage"
            })
            num_differences += 1

    for id, stage_reward in stage_rewards.items():
        if id not in prod_rewards:
            differences.append({
                "id": id,
                "difference": "not found in prod"
            })
            num_differences += 1

    print(f"Number of differences: {num_differences}")
    for difference in differences:
        print(f"ID: {difference['id']}:\n{difference['difference']}")
    

def compare_rewards_prod_stage(prod_url, stage_url, address):
    prod = SubqueryData(url=prod_url)
    stage = SubqueryData(url=stage_url)
    
    address = convert_to_checksum_address(address=address)
    prod_rewards = {reward["id"]: reward for reward in prod.getMultichainRewards(address)}
    stage_rewards = {reward["id"]: reward for reward in stage.getMultichainRewards(address)}
    
    compare_results(prod_rewards, stage_rewards)
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <address>")
        sys.exit(1)

    prod_url = "https://api.subquery.network/sq/nova-wallet/subquery-staking"
    stage_url = prod_url + "__bm92Y"
    address = sys.argv[1]
    compare_rewards_prod_stage(prod_url, stage_url, address)