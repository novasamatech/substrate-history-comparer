
from data_module.SubqueryData import SubqueryData
from data_module.SubscanData import SubscanData


def collect_data(subquery_url, subscan_url, address):
    """ Collects data from the subquery and subscan data sources """

    sub_query = SubqueryData(url=subquery_url)
    sub_scan = SubscanData(url_rewards=subscan_url, address=address)
    
    subquery_rewards = sub_query.getMultichainRewards(address)
    subscan_rewards = sub_scan.getRewards()
    
    return subquery_rewards, subscan_rewards

def compare_subquery_with_subscan(sub_query_rewards, sub_scan_rewards):

    def transfer_id_for_compare(string_to_transfer):
        new_string = string_to_transfer.split('-')[:2]
        return "-".join(new_string)
    
    sub_query_dict = {transfer_id_for_compare(reward['id']): reward for reward in sub_query_rewards}
    sub_scan_dict = {reward['event_index']: reward for reward in sub_scan_rewards}
    
    subscan_total_rewards = 0
    sorted_keys = sorted(sub_query_dict.keys())
    my_total_reward_calculation = 0
    for key in sorted_keys:
        my_total_reward_calculation += int(sub_query_dict[key].get('amount'))
    
    print(f"My accumulation rewards: {my_total_reward_calculation}")
    print(f"SubQuery accumulated erwards: {sub_query_dict[sorted_keys.pop()].get('accumulatedAmount')}")
    for sub_scan_id, subscan_reward in sub_scan_dict.items():

        subquery_reward = sub_query_dict[sub_scan_id]
        
        if subquery_reward.get('amount') != subscan_reward.get('amount'):
            print(f"Reward amount is not equal! {subquery_reward}, {subscan_reward}")
        
        if subscan_reward.get('event_id') == 'Rewarded':
            subscan_total_rewards += int(subscan_reward.get('amount'))
        else:
            raise Exception(f"Wrong event - {subscan_reward.get('event_id')}")
        
        del sub_query_dict[sub_scan_id]
    
    
    print(f"Subscan total rewards: {subscan_total_rewards}")
    print(f"Difference rewards: {sub_query_dict}")
    return sub_query_dict

def main():
    subquery_url = "https://api.subquery.network/sq/nova-wallet/subquery-staking"
    subscan_rewards_url = "https://polkadot.webapi.subscan.io/api/v2/scan/account/reward_slash"
    address = "1ChFWeNRLarAPRCTM3bfJmncJbSAbSS9yqjueWz7jX7iTVZ"
    sub_query, sub_scan = collect_data(subquery_url, subscan_rewards_url, address)
    compare_subquery_with_subscan(sub_query, sub_scan)


if __name__ == "__main__":
    main()