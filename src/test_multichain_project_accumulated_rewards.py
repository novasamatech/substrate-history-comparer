import sys  
from compare_prod_and_stage import convert_to_checksum_address, get_address_list
from data_module.SubqueryData import SubqueryData


def compare_subquery_prod_stage(prod_url, stage_url):
    prod = SubqueryData(url=prod_url)
    stage = SubqueryData(url=stage_url)
    
    addresses = get_address_list(subscan_account_url, temp_file, "nominator")
    
    for address in addresses:
        address = convert_to_checksum_address(address=address)
        prod_acc_reward = prod.get_multichain_accumulated_rewards(address)
        stage_acc_reward = stage.get_multichain_accumulated_rewards(address)
        if prod_acc_reward != stage_acc_reward:
            max_value = max((prod_acc_reward, 'prod_acc_reward'), (stage_acc_reward, 'stage_acc_reward'), key=lambda x: x[0])
            print(f"Address {address} ❌")
            print(f"Biggest is: {max_value[1]}")
            print(f"Prod rewards: {prod_acc_reward}\nStage rewards: {stage_acc_reward}\n")
        else:
            print(f"Address {address} ✅")
    
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <network>")
        sys.exit(1)

    prod_url = "https://api.subquery.network/sq/nova-wallet/subquery-staking"
    stage_url = prod_url + "__bm92Y"
    network = sys.argv[1]
    subscan_account_url = f"https://{network}.webapi.subscan.io/api/v2/scan/accounts"
    temp_file = f"{network}_accounts.txt"
    compare_subquery_prod_stage(prod_url, stage_url)