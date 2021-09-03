from settings import *

from src.data_module.SubqueryData import SubqueryData
from src.data_module.SubscanData import SubscanData
from src.loger import *
from src.matching_value import matching_values


def call_by_address(address):
    value = []
    subscan = SubscanData(address=address, url_extrinsics=url_extrinsics,
                          url_rewards=url_rewards, url_transfers=url_transfers)

    subquery = SubqueryData(url=subquery_url, address=address)
    print('=====================================')
    print('Fetch data for address: %s' % address)
    subscan.getAllData()
    subquery.fetchHistory()
    print('Subscan transfers: %s, extrinsics: %s, rewards: %s' %
          (subscan.transfer_count, subscan.extrinsic_count, subscan.reward_count))
    subscan_data = subscan.store_all_operation_in_one_list()
    value = matching_values(subscan_data=subscan_data,
                            subquery_data=subquery.history_elements)
    print('Found non match events: %s' % len(value))
    for found_element in value:
        print(found_element)
