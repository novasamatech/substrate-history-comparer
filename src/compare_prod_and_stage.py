


import json
import os
from data_module.SubqueryData import SubqueryData
from data_module.SubscanData import SubscanData
from web3 import Web3

def convert_to_checksum_address(address):
    if address[:2] == "0x" and len(address) == 42:
        address = address[2:]  # Remove the '0x' prefix if present
        return Web3.to_checksum_address(address)
    return address

def get_address_list(url):
    file_path = 'accounts.txt'
    
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            file_contents = file.read()
            json_data = json.loads(file_contents)
            return json_data
    else:
        account_type = 'nominator'
        accounts = SubscanData(url_accounts=url).get_all_accounts(type=account_type, batch_depth=10)
        accounts_list = [account.get('address') for account in accounts]
        with open(file_path, "w") as file:
            file.write(json.dumps(accounts_list))
        return accounts_list
    
def compare_history_elements(prod_elements: list, stage_elements: list):
    prod_dict = {element.get('id'): element for element in prod_elements}
    stage_dict = {element.get('id'): element for element in stage_elements}

    # Find elements in prod_dict that do not exist in stage_dict
    missing_elements_prod = {key: value for key, value in prod_dict.items() if key not in stage_dict}

    # Find elements in stage_dict that do not exist in prod_dict
    missing_elements_stage = {key: value for key, value in stage_dict.items() if key not in prod_dict}

    # Print the missing elements and where they were found
    for key, value in missing_elements_prod.items():
        print(f"Element '{value}' with key '{key}' was found in prod_dict 🚀 but not in stage_dict")

    for key, value in missing_elements_stage.items():
        print(f"Element '{value}' with key '{key}' was found in stage_dict 👷‍♂️ but not in prod_dict")

    
def compare_stage_with_prod(subquery_nova, subquery_stage, address_list):
    for address in address_list:
        address = convert_to_checksum_address(address)
        subquery_nova_project = SubqueryData(url=subquery_nova, address=address)
        history_prod = subquery_nova_project.fetchHistory()
        subquery_nova_stage_poject = SubqueryData(url=subquery_stage, address=address)
        history_stage = subquery_nova_stage_poject.fetchHistory()
        if len(history_prod) != len(history_stage):
            print(f"For account: {address} history elements! ❌")
            print(f"Prod: {len(history_prod)}, Stage: {len(history_stage)}")
            compare_history_elements(history_prod, history_stage)
        else:
            print(f"History elements processed for account: {address} successfully! ✅")
            
if __name__ == "__main__":
    subscan_account_url = 'https://moonbeam.webapi.subscan.io/api/v2/scan/accounts'
    subquery_nova_prod = 'https://api.subquery.network/sq/nova-wallet/nova-wallet-moonbeam'
    subquery_nova_stage = subquery_nova_prod+"__bm92Y"
    address_list = get_address_list(subscan_account_url)
    compare_stage_with_prod(subquery_nova_prod, subquery_nova_stage, address_list)