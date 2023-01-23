'''
This file is used to test the open gov subquery project
'''

import json

from src.data_module.SubqueryData import SubqueryData
from src.data_module.subsquare_data import SubSquare

def collect_data(subquery_url, subsquare_url):
    """ Collects data from the subquery and subsquare data sources and returns them as objects """

    sub_query = SubqueryData(url=subquery_url)
    sub_square = SubSquare(url=subsquare_url)
    local_data = read_data_from_json('referenda_data.json')

    if local_data is None:
        referenda_list = sub_square.getReferendaList()
        for referenda_id in referenda_list:
            print(f"Getting voters for referenda {referenda_id}...")
            sub_square.getReferendaVoters(referenda_id)
    else:
        sub_square.referenda_dict = local_data

    return sub_query, sub_square

def check_data_in_subquery(sub_query, sub_square: SubSquare):
    subquery_voters_dict = {}

    def find_index(arr, referenda_id):
        return next((i for i, x in enumerate(arr) if x['referendumId'] == referenda_id), None)

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
            subquery_voter_votes = subquery_voters_dict[voter['voter']]['data']['castingVotings']['nodes']
            find_proper_vote_and_compare(subquery_voter_votes, referenda_id, voter)


def save_data_in_json(subsquare_referenda_dict):
    with open('referenda_data.json', 'w') as outfile:
        json.dump(subsquare_referenda_dict, outfile)


def read_data_from_json(path):
    try:
        with open(path) as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return None


def main():
    subquery_url = "https://api.subquery.network/sq/nova-wallet/nova-wallet-kusama-governance"
    subsquery_url = "https://kusama.subsquare.io"
    sub_query, sub_square = collect_data(subquery_url, subsquery_url)
    save_data_in_json(sub_square.referenda_dict)
    check_data_in_subquery(sub_query, sub_square)


if __name__ == "__main__":
    main()
