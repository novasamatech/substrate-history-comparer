from collections import defaultdict
import json
import os

from data_module.SubscanData import SubscanData
from data_module.SubqueryData import SubqueryData

def diff_dicts(nova_data, multichain_data, address):
    new_elements = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    for key in nova_data.keys():
        if key not in multichain_data.keys():
            new_elements["nova_project"][key] = nova_data[key]
    for key in multichain_data.keys():
        if key not in nova_data.keys():
            new_elements["multichain_project"][key] = multichain_data[key]
    
    with open("account_diff/"+address+".json", "w") as file:
        file.write(json.dumps(new_elements))
    
    return new_elements

def compare_subqery_accumulated_rewards(subquery_nova, subquery_multichain, address_list):
    for address in address_list:
        subquery_nova_project = SubqueryData(url=subquery_nova, address=address)
        rewards_nova = subquery_nova_project.getNovaAccumulatedRewards(address)
        subquery_multi_project = SubqueryData(url=subquery_multichain, address=address)
        rewards_multichain = subquery_multi_project.getMultichainAccumulatedRewards(address)
        if rewards_nova != rewards_multichain:
            print(f"For account: {address} accumulated rewards not the same! ❌")
            print(f"Nova project: {rewards_nova}, multichain project: {rewards_multichain}")
        else:
            print(f"Accumulated rewards processed for account: {address} successfully! ✅")

def get_address_list(url):
    file_path = 'accounts.txt'
    
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            file_contents = file.read()
            json_data = json.loads(file_contents)
            return json_data
    else:
        account_type = 'nominator'
        accounts = SubscanData(url_accounts=url).get_all_accounts(type=account_type)
        accounts_list = [account.get('address') for account in accounts]
        with open(file_path, "w") as file:
            file.write(json.dumps(accounts_list))
        return accounts_list

def transfer_id_for_compare(string_to_transfer):
        new_string = string_to_transfer.split('-')[:2]
        return "-".join(new_string)
    
def compare_each_reward(subquery_nova, subquery_multichain, address_list):
    for address in address_list:
        subquery_nova_project = SubqueryData(url=subquery_nova, address=address)
        nova_rewards = subquery_nova_project.getNovaRewards(address)
        subquery_multi_project = SubqueryData(url=subquery_multichain, address=address)
        multichain_rewards = subquery_multi_project.getMultichainRewards(address)
        dict_nova_rewards = {transfer_id_for_compare(nova_reward.get('id')): nova_reward for nova_reward in nova_rewards}
        dict_multi_rewards = {transfer_id_for_compare(multi_reward.get('id')): multi_reward for multi_reward in multichain_rewards}
        if len(dict_nova_rewards) != len(dict_multi_rewards):
            print(f"Reward list NOT the same for account: {address} ❌")
            print(f"Multichain project rewards count: {len(dict_multi_rewards)}")
            print(f"Nova project rewards count: {len(dict_nova_rewards)}")
            diff_dicts(dict_nova_rewards, dict_multi_rewards, address)
        else:
            print(f"Reward list the same for account: {address} ✅")


def compare_subqery_accumulated_rewards_case_2(subquery_nova, subquery_multichain, address_list):
    for address in address_list:
        subquery_nova_project = SubqueryData(url=subquery_nova, address=address)
        rewards_nova = subquery_nova_project.getNovaAccumulatedRewards(address)
        subquery_multi_project = SubqueryData(url=subquery_multichain, address=address)
        rewards_multichain = subquery_multi_project.getMultichainAmountRewards(address)
        if rewards_nova != rewards_multichain:
            print(f"For account: {address} accumulated rewards not the same! ❌")
            print(f"Nova project: {rewards_nova}, multichain project: {rewards_multichain}")
        else:
            print(f"Accumulated rewards processed for account: {address} successfully! ✅")

if __name__ == "__main__":
    subquery_multichain = 'https://api.subquery.network/sq/nova-wallet/subquery-staking'
    subquery_nova = 'https://api.subquery.network/sq/nova-wallet/nova-wallet-kusama'
    subscan_account_url = 'https://kusama.webapi.subscan.io/api/v2/scan/accounts'
    address_list = get_address_list(subscan_account_url)
    # compare_each_reward(subquery_nova, subquery_multichain, address_list)
    compare_subqery_accumulated_rewards_case_2(subquery_nova, subquery_multichain, address_list)
    # compare_subqery_accumulated_rewards(subquery_nova, subquery_multichain, address_list)