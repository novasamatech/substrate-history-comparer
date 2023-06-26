import json
import os

from data_module.SubscanData import SubscanData
from data_module.SubqueryData import SubqueryData


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
        account_type = 'validator'
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
        dict_nova_rewards = {nova_reward.get('id'): nova_reward for nova_reward in nova_rewards}
        dict_multi_rewards = {transfer_id_for_compare(multi_reward.get('id')): multi_reward for multi_reward in multichain_rewards}
        if len(dict_nova_rewards) != len(dict_multi_rewards):
            print(f"Reward list NOT the same for account: {address} ❌")
            print(f"Multichain project rewards count: {len(dict_multi_rewards)}")
            print(f"Nova project rewards count: {len(dict_nova_rewards)}")
        else:
            print(f"Reward list the same for account: {address} ✅")


if __name__ == "__main__":
    subquery_multichain = 'https://api.subquery.network/sq/nova-wallet/subquery-staking'
    subquery_nova = 'https://api.subquery.network/sq/nova-wallet/nova-wallet-polkadot'
    subscan_account_url = 'https://polkadot.webapi.subscan.io/api/v2/scan/accounts'
    address_list = get_address_list(subscan_account_url)
    compare_each_reward(subquery_nova, subquery_multichain, address_list)
    # compare_subqery_accumulated_rewards(subquery_nova, subquery_multichain, address_list)