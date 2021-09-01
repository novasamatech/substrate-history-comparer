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

matching_value = []
subscan.getAllData()
subquery.fetchHistory()
subquery_elements = subquery.history_elements
for element in subscan.data:
    for into_element in element:
        data = subscan.type_of_subscan_operation_picker(into_element)
        for double_into_element in data:
            i = 0
            for dictionary in subquery.history_elements:
                for key, value in dictionary.items():
                    if key == 'timestamp':
                        if int(value) == double_into_element['block_timestamp']:
                            subquery_elements.pop(i)
                i+=1
print(subquery_elements)
print('Success')