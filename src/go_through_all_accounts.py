from data_module.SubscanData import SubscanData
from multichain_comparer import collect_data, compare_subquery_with_subscan

def collect_all_accounts(subscan_account_url, subscan_reward_url, subquery_url):
    account_type = "validator"
    subscan_accounts = SubscanData(url_accounts=subscan_account_url).get_all_accounts(account_type)
    print(f"Accounts with type: {account_type}\n will be processed...")
    for account in subscan_accounts:
        print("="*20)
        print(f"Calculate data for: {account.get('address')}")
        sub_query, sub_scan = collect_data(subquery_url, subscan_reward_url, account.get('address'))
        compare_subquery_with_subscan(sub_query, sub_scan)
    

if __name__ == '__main__':
    subquery_url = 'https://api.subquery.network/sq/nova-wallet/subquery-staking'
    subscan_accounts_url = 'https://polkadot.webapi.subscan.io/api/v2/scan/accounts'
    subscan_rewards_url = 'https://polkadot.webapi.subscan.io/api/v2/scan/account/reward_slash'
    collect_all_accounts(subscan_accounts_url, subscan_rewards_url, subquery_url)
    