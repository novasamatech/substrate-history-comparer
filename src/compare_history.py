from settings import *

from src.loger import *
from src.matching_value import matching_values


def compare_history(subscan, subquery):
    value = []
    subscan.getAllData()
    subquery.fetchHistory()
    subscan_data = subscan.store_all_operation_in_one_list()
    print('Subscan data has: %s elements' % len(subscan_data))
    print('Subscan transfers: %s, extrinsics: %s, rewards: %s' %
          (subscan.transfer_count, subscan.extrinsic_count, subscan.reward_count))
    print('=====================================')
    value = matching_values(subscan_data=subscan_data,
                            subquery_data=subquery.history_elements)
    print('=====================================')
    print('Found non match events: %s' % len(value))
    for found_element in value:
        print(found_element)
