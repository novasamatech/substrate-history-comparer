from src.data_module.SubqueryData import SubqueryData
from src.data_module.SubscanData import SubscanData


class Networks:
    polka = ["polkadot", 10]
    kusama = ["kusama", 12]
    westend = ['westend', 12]


network = Networks.polka
address = "13mAjFVjFDpfa42k2dLdSnUyrSzK8vAySsoudnxX2EKVtfaq"

url_extrinsics = 'https://%s.api.subscan.io/api/scan/extrinsics' % (network[0])
url_rewards = 'https://%s.api.subscan.io/api/scan/account/reward_slash' % (
    network[0])
url_transfers = 'https://%s.api.subscan.io/api/scan/transfers' % (network[0])
subquery_url = 'https://api.subquery.network/sq/ef1rspb/fearless-wallet'

subscan = SubscanData(address=address, url_extrinsics=url_extrinsics,
                      url_rewards=url_rewards, url_transfers=url_transfers)

subquery = SubqueryData(url=subquery_url, address=address)

def getKeysForValueComp(dictionary, value):
    return [key for key in dictionary if dictionary[key] == value]

def matching_values(subquery_data, subscan_data):
    print('Subquery data has: %s' % len(subquery_data))
    print('Subscan data has: %s' % len(subscan_data))
    subq_extrinsics = []
    subq_transfers = []
    subq_rewards = []
    for subq_element in subquery_data:
        if subq_element.get('transfer'):
            subq_transfers.append(subq_element)
        if subq_element.get('extrinsic'):
            subq_extrinsics.append(subq_element)
        if subq_element.get('reward'):
            subq_rewards.append(subq_element)

    for transfer in subq_transfers:
        value = transfer['transfer']['extrinsicId']
        subscan_data[:] = [d for d in subscan_data if d.get('extrinsic_index') != value]
    for extrinsic in subq_extrinsics:
        value = extrinsic['id']
        subscan_data[:] = [d for d in subscan_data if d.get('extrinsic_hash') != value]
    for reward in subq_rewards:
        value = reward['id']
        subscan_data[:] = [d for d in subscan_data if d.get('event_index') != value]

    return subscan_data



subscan.getAllData()
subquery.fetchHistory()
subquery_elements = subquery.history_elements
subscan_data = subscan.store_all_operation_in_one_list()
value = matching_values(subscan_data=subscan_data, subquery_data=subquery_elements)
print('Found non match events: %s' % len(value))
for found_element in value:
    print(found_element)