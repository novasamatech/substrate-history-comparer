from src.data_module.SubqueryData import SubqueryData
from src.data_module.SubscanData import SubscanData
from settings import *
from src.compare_history import compare_history
from src.loger import *


def compare_subs_with_subq(address):
    subscan = SubscanData(address=address, url_extrinsics=url_extrinsics,
                          url_rewards=url_rewards, url_transfers=url_transfers)
    subquery = SubqueryData(url=subquery_url, address=address)

    print('Fetch data for address: %s' % address)
    compare_history(subscan=subscan, subquery=subquery)
    subscan_total_rewards = subscan.calculate_rewards()
    subquery_total_rewards = subquery.calculate_rewards()
    print('\nSubs total rewards is: %s \nSubq total rewards is: %s' %
          (subscan_total_rewards, subquery_total_rewards))


def main():
    account_address = '13mAjFVjFDpfa42k2dLdSnUyrSzK8vAySsoudnxX2EKVtfaq'
    single_mode = False
    if (single_mode):
        compare_subs_with_subq(address=account_address)
    else:
        i = 0
        for address in addresses:
            start = time.time()
            print('********* Iteration: %s of %s *********' %
                  (i, len(addresses)))
            compare_subs_with_subq(address=address)
            print('Call function spent: %s seconds' % (time.time() - start))
            i += 1


if __name__ == "__main__":
    main()
