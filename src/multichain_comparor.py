
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
    
    check_difference_between_rewards(sub_scan_dict, sub_query_dict)
    check_accumulated_rewards_difference(sub_scan_dict, sub_query_dict)
    
    return sub_query_dict

def check_difference_between_rewards(subscan_reards: dict, subquery_rewards: dict):
    new_dict = subquery_rewards.copy()
    
    for sub_scan_id, subscan_reward in subscan_reards.items():
        try:
            subquery_reward = subquery_rewards[sub_scan_id]
        except:
            print(f"Can't find on SubQuery reward: {sub_scan_id}")
            continue
        
        if subquery_reward.get('amount') != subscan_reward.get('amount'):
            print(f"Reward amount is not equal! {subquery_reward}, {subscan_reward}")
        
        del new_dict[sub_scan_id]
    
    print(f"Count of difference rewards: {len(new_dict.keys())}")
    print(f"Difference rewards: {new_dict}")

def check_accumulated_rewards_difference(subscan_rewards: dict, subquery_rewards: dict):
    subscan_total_rewards = 0
    sorted_keys = sorted(subquery_rewards.keys())
    my_total_reward_calculation = 0
    
    first_element_with_problem = None
    for key in sorted_keys:
        subq_reward = subquery_rewards[key]
        subquery_amount = int(subq_reward.get('amount'))
        subquery_accumulated_amount = int(subq_reward.get('accumulatedAmount'))
        if subq_reward.get('type') == 'reward':
            my_total_reward_calculation += subquery_amount  
        else: 
            my_total_reward_calculation -= subquery_amount 
        
        previous_reward = subq_reward
        if subquery_accumulated_amount != my_total_reward_calculation:
            # Skip processing if found element from which calculation is wrong
            if first_element_with_problem:
                continue
            
            print(f"Clculation is not the same: {subquery_accumulated_amount} vs {my_total_reward_calculation}")
            print(f"Subquery data: {subq_reward}")
            first_element_with_problem = previous_reward
            print(f"First reward with problem - {first_element_with_problem}")
        else:
            previous_reward = subq_reward
    
    # Calculate subscan total rewards
    for _, subscan_reward in subscan_rewards.items():
        event = subscan_reward.get('event_id')
        if event == 'Rewarded' or event == 'Reward':
            subscan_total_rewards += int(subscan_reward.get('amount'))
        elif event == "Slashed":
            subscan_total_rewards -= int(subscan_reward.get('amount'))
        else:
            raise Exception(f"Wrong event - {subscan_reward.get('event_id')}")

    print(f"Calculated accumulatedRewards, based on subquery data: {my_total_reward_calculation}")
    print(f"SubQuery accumulated rewards: {subquery_rewards[sorted_keys.pop()].get('accumulatedAmount')}")
    print(f"Subscan total rewards: {subscan_total_rewards}")


def main():
    subquery_url = "https://api.subquery.network/sq/nova-wallet/subquery-staking"
    options = ["kusama", "polkadot", "moonbeam", "moonriver", "westend"]
    selection = input("Please type a network, use one of this list: " + ", ".join(options) + "\n")
    if selection not in ["moonbeam", "moonriver"]:
        subscan_rewards_url = f"https://{selection}.webapi.subscan.io/api/v2/scan/account/reward_slash"
    else:
        subscan_rewards_url = f"https://{selection}.webapi.subscan.io/api/scan/account/reward_slash"
    address = input("Account address: ")
    print("Data collection takes some time...")
    sub_query, sub_scan = collect_data(subquery_url, subscan_rewards_url, address)
    compare_subquery_with_subscan(sub_query, sub_scan)


if __name__ == "__main__":
    main()