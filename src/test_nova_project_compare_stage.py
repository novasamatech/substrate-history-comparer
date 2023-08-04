import sys
from compare_prod_and_stage import get_address_list

from data_module.SubqueryData import SubqueryData
from test_multichain_project_rewards_list import compare_results

def calculate_rewards(prod_elements):
    rewards_accumulator = 0
    for _, element in prod_elements.items():
        reward = element.get('reward')
        if reward:
            if reward['isReward']:
                rewards_accumulator+=int(reward['amount'])
            else:
                rewards_accumulator-=int(reward['amount'])
    
    return rewards_accumulator

def nova_stage_compare(prod_url, stage_url, addresses):
    block = 4275128
    account = "12Ea3kSFDH3Meg5Br63o5BXZh4ELvhapCj96ygaXiTtpVhUM"
    prod = SubqueryData(prod_url)
    stage = SubqueryData(stage_url)
    
    for address in addresses:
        print(f"Processing address: {address}")
        prod_elements = {element['id']: element for element in prod.collect_history_data_from_block(block, address)}
        stage_elements = {element['id']: element for element in stage.collect_history_data_from_block(block, address)}
        compare_results(prod_elements, stage_elements)
        prod_acc_rewards = calculate_rewards(prod_elements)
        stage_acc_rewards = int(stage.nova_get_accumulated_reward(address, block))
        if prod_acc_rewards != stage_acc_rewards:
            print(f"Accumulated rewards is not the same: ❌")
            print(f"Prod rewards:\n{prod_acc_rewards}\nStage rewards:{stage_acc_rewards}\n")
        else:
            print("Accumulated rewards the same! ✅")

if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     print("Usage: python script.py <network>")
    #     sys.exit(1)

    prod_url = "https://api.subquery.network/sq/nova-wallet/nova-wallet-polkadot"
    stage_url = prod_url + "__bm92Y"
    # network = sys.argv[1]
    network="polkadot"
    subscan_account_url = f"https://{network}.webapi.subscan.io/api/v2/scan/accounts"
    temp_file = f"{network}_accounts.txt"
    addresses = get_address_list(subscan_account_url, temp_file, "nominator")
    nova_stage_compare(prod_url, stage_url, addresses=addresses)