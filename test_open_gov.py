'''
This file is used to test the open gov subquery project
'''

import json
from src.data_module.SubscanData import SubscanData

from src.data_module.kusama_governance import KusamaGovernance
from src.data_module.SubqueryData import SubqueryData
from src.data_module.subsquare_data import SubSquare

def collect_data(subquery_url, subsquare_url):
    """ Collects data from the subquery and subsquare data sources and returns them as objects """

    sub_query = SubqueryData(url=subquery_url)
    sub_square = SubSquare(url=subsquare_url)
    try:
        local_data = read_data_from_json('subsquare_referenda_data.json')
    except FileNotFoundError:
        local_data = None

    if local_data is None:
        referenda_list = sub_square.getReferendaList()
        for referenda_id in referenda_list:
            print(f"Getting voters for referenda {referenda_id}...")
            sub_square.getReferendaVoters(referenda_id)
    else:
        sub_square.referenda_dict = local_data

    return sub_query, sub_square


def compare_subquery_with_subsquare(sub_query, sub_square: SubSquare):
    subquery_voters_dict = {}

    def find_index(arr, referenda_id):
        return next((i for i, x in enumerate(arr) if int(x['referendumId']) == int(referenda_id)), None)

    def find_proper_vote_and_compare(arr, referenda_id, subsquare_vote):
        try:
            index = find_index(arr, referenda_id)
            compare_vote_data(arr[index], subsquare_vote)
        except TypeError:
            print("Element not found ❌")
            print(f"for account {subsquare_vote['voter']} and referendum {referenda_id}")
            print(f"Subsquare vote: {subsquare_vote}")

    def compare_vote_data(subquery_vote, sub_square_vote):
        if sub_square_vote['isSplitAbstain']:
            tested_aye_amount = subquery_vote['splitAbstainVote']['ayeAmount']
            tested_nay_amount = subquery_vote['splitAbstainVote']['nayAmount']
            tested_abstain_amount = subquery_vote['splitAbstainVote']['abstainAmount']

            vote_aye_amount = sub_square_vote['vote']['aye']
            vote_nay_amount = sub_square_vote['vote']['nay']
            vote_abstain_amount = sub_square_vote['vote']['abstain']

            if tested_aye_amount == vote_aye_amount and tested_nay_amount == vote_nay_amount and tested_abstain_amount == vote_abstain_amount:
                print(f"Votes match ✅\nfor {sub_square_vote['voter']} and referendum {sub_square_vote['referendumIndex']}.")
            else:
                print(f"Votes don't match ❌\n{sub_square_vote['voter']} and referendum {sub_square_vote['referendumIndex']}.")
                print(f"Subquery vote: {subquery_vote}")
                print(f"Subsquare vote: {sub_square_vote}")
        else:
            if subquery_vote['splitAbstainVote']:
                print("Split abstain vote is not empty ❌")
                print(f"for account {sub_square_vote['voter']} and referendum {sub_square_vote['referendumIndex']}")
                print(f"Subquery vote: {subquery_vote}")
                print(f"Subsquare vote: {sub_square_vote}")
            else:
                tested_vote_amount = subquery_vote['standardVote']['vote']['amount']
                conviction_string = subquery_vote['standardVote']['vote']['conviction']
                if conviction_string == 'None':
                    tested_vote_conviction = 0
                else:
                    tested_vote_conviction = int(''.join([n for n in conviction_string if n.isdigit()]))
                tested_vote_direction = subquery_vote['standardVote']['aye']

                vote_amount = sub_square_vote['vote']['balance']
                vote_conviction = sub_square_vote['vote']['vote']['conviction']
                vote_direction = sub_square_vote['vote']['vote']['isAye']

                if tested_vote_amount == vote_amount and tested_vote_conviction == vote_conviction and tested_vote_direction == vote_direction:
                    print(f"Votes match ✅\nfor {sub_square_vote['voter']} and referendum {sub_square_vote['referendumIndex']}.")
                else:
                    print(f"Votes don't match ❌\n{sub_square_vote['voter']} and referendum {sub_square_vote['referendumIndex']}.")
                    print(f"Subquery vote: {subquery_vote}")
                    print(f"Subsquare vote: {sub_square_vote}")

    for referenda_id, referenda in sub_square.referenda_dict.items():
        for voter in referenda['voters']:
            if voter['voter'] not in subquery_voters_dict:
                subquery_voters_dict[voter['voter']] = sub_query.getReferendaVotesForAddress(voter['voter'])
            try:
                subquery_voter_votes = subquery_voters_dict[voter['voter']]['data']['castingVotings']['nodes']
                find_proper_vote_and_compare(subquery_voter_votes, referenda_id, voter)
            except:
                print('Oops')


def compare_subquery_with_kusama_gov(sub_query, sub_square: SubSquare):
    subquery_voters_dict = {}
    kusama_voters_dict = {}
    kusama_gov = KusamaGovernance()

    def compare_votes(subquery_voter_votes, referenda_id, kusama_gov_voter):
        pass

    for referenda_id, referenda in sub_square.referenda_dict.items():
        for voter in referenda['voters']:
            if voter['voter'] not in subquery_voters_dict:
                kusama_voters_dict[voter['voter']] = kusama_gov.getAccountData(voter['voter'])
                subquery_voters_dict[voter['voter']] = sub_query.getReferendaVotesForAddress(voter['voter'])
            subquery_voter_votes = subquery_voters_dict[voter['voter']]['data']['castingVotings']['nodes']
            compare_votes(subquery_voter_votes, referenda_id, kusama_voters_dict[voter['voter']])


def compare_subquery_with_subscan(subquery_url, subscan_referenda_url):
    sub_query = SubqueryData(url=subquery_url)
    sub_scan = SubscanData(referenda_url=subscan_referenda_url)

    referendums = read_data_from_json('subscan_referenda_data.json')
    
    if referendums is None:
        referendums_dict = sub_scan.get_referenda_list()
        voters = sub_scan.get_all_votes(referendums_dict)
        save_data_in_json(sub_scan.all_referenda, 'subscan_referenda_data.json')
        referendums = sub_scan.all_referenda
    
    voters = sub_query.fetch_referenda_data(referendums.keys())

    def find_index(arr, referenda_id):
        return next((i for i, x in enumerate(arr) if int(x['referendumId']) == int(referenda_id)), None)

    def find_aproper_vote_and_compare(arr, referenda_id, subscan_vote):
        try:
            index = find_index(arr, referenda_id)
            compare_vote_data(arr[index], subscan_vote)
        except TypeError:
            print("Element not found ❌")
            print(f"for account {subscan_vote['account']['address']} and referendum {referenda_id}")
            print(f"Subsquare vote: {subscan_vote}")

    def compare_vote_data(subquery_vote, sub_scan_vote):
        if sub_scan_vote['status'] == 'Abstains':
            tested_aye_amount = subquery_vote['splitAbstainVote']['ayeAmount']
            tested_nay_amount = subquery_vote['splitAbstainVote']['nayAmount']
            tested_abstain_amount = subquery_vote['splitAbstainVote']['abstainAmount']

            vote_abstain_amount = sub_scan_vote['amount']
            vote_aye_amount = '0'
            vote_nay_amount = '0'

            if tested_aye_amount == vote_aye_amount and tested_nay_amount == vote_nay_amount and tested_abstain_amount == vote_abstain_amount:
                print(f"Votes match ✅\nfor {sub_scan_vote['account']['address']} and referendum {subquery_vote['referendumId']}.")
            else:
                print(f"Votes don't match ❌\n{sub_scan_vote['account']['address']} and referendum {subquery_vote['referendumId']}.")
                print(f"Subquery vote: {subquery_vote}")
                print(f"Subsquare vote: {sub_scan_vote}")
        elif subquery_vote['splitVote'] is not None:
            tested_aye_amount = subquery_vote['splitVote']['ayeAmount']
            tested_nay_amount = subquery_vote['splitVote']['nayAmount']
            tested_vote_amount = int(tested_aye_amount) + int(tested_nay_amount)

            vote_amount = int(sub_scan_vote['amount'])
            vote_conviction = sub_scan_vote['conviction']

            if tested_vote_amount == vote_amount:
                print(f"Votes match ✅\nfor {sub_scan_vote['account']['address']} and referendum {subquery_vote['referendumId']}.")
            else:
                print(f"Votes don't match ❌\n{sub_scan_vote['account']['address']} and referendum {subquery_vote['referendumId']}.")
                print(f"Subquery vote: {subquery_vote}")
                print(f"Subsquare vote: {sub_scan_vote}")

        else:
            tested_vote_amount = subquery_vote['standardVote']['vote']['amount']
            conviction_string = subquery_vote['standardVote']['vote']['conviction']
            if conviction_string == 'None':
                tested_vote_conviction = '0.1'
            else:
                tested_vote_conviction = str(''.join([n for n in conviction_string if n.isdigit()]))
            tested_vote_direction = subquery_vote['standardVote']['aye']

            vote_amount = sub_scan_vote['amount']
            vote_conviction = sub_scan_vote['conviction']
            vote_direction = True if sub_scan_vote['status'] == 'Ayes' else False

            if tested_vote_amount == vote_amount and tested_vote_conviction == vote_conviction and tested_vote_direction == vote_direction:
                print(f"Votes match ✅\nfor {sub_scan_vote['account']['address']} and referendum {subquery_vote['referendumId']}.")
            else:
                print(f"Votes don't match ❌\n{sub_scan_vote['account']['address']} and referendum {subquery_vote['referendumId']}.")
                print(f"Subquery vote: {subquery_vote}")
                print(f"Subsquare vote: {sub_scan_vote}")

    subquery_voters_dict = {}
    for referenda_id, referenda in referendums.items():
        for vote in referenda['votes']:
            voter_address = vote['account']['address']

            try:
                voters[voter_address]
            except:
                print("Element not found ❌")
                print(f"for account {voter_address} and referendum {referenda_id}")
                print(f"Subsquare vote: {vote}")
                continue
            find_aproper_vote_and_compare(voters[voter_address], referenda_id, vote)




def save_data_in_json(subsquare_referenda_dict, path='referenda_data.json'):
    with open(path, 'w') as outfile:
        json.dump(subsquare_referenda_dict, outfile)


def read_data_from_json(path):
    try:
        with open(path) as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return None


def main():
    subquery_url = "https://api.subquery.network/sq/nova-wallet/nova-wallet-kusama-governance2"
    subsquery_url = "https://kusama.subsquare.io"
    subscan_referenda_url = "https://kusama.webapi.subscan.io/api/scan/referenda/referendums"
    sub_query, sub_square = collect_data(subquery_url, subsquery_url)
    # save_data_in_json(sub_square.referenda_dict)
    compare_subquery_with_subsquare(sub_query, sub_square)
    compare_subquery_with_subscan(subquery_url, subscan_referenda_url)
    # compare_subquery_with_kusama_gov(sub_query, sub_square)


if __name__ == "__main__":
    main()
