from collections import defaultdict
import requests
import json
import time

from .fixture import history_elements_restricted_by_block, historyElements_by_address, historyElement_by_id, multichain_account_rewards, multichain_accumulated_rewards, multichain_accumulated_rewards_sum, nova_account_rewards, nova_accumulated_reward_by_account, nova_accumulated_rewards, referenda_by_id, referenda_all_account_votes, small_data_referenda_by_id


class SubqueryData:
    url = ""
    address = ""
    history_elements = []
    referenda_dict = {}
    account_votes_dictionary = {}
    voter_dict = defaultdict(list)

    def __init__(self, url, address=None):
        self.url = url
        self.address = address

    def getHistoryList(self):
        total_history = []
        query = json.dumps(historyElements_by_address(self.address))
        data = self.__send_request(self.url, query)
        hystory_elements = data.get('data').get('historyElements')
        has_next_page = hystory_elements.get('pageInfo').get('hasNextPage')
        total_history = total_history + hystory_elements.get('nodes')
        
        def make_deep_request(cursor):
            new_query = json.dumps(historyElements_by_address(self.address, cursor=cursor))
            new_data = self.__send_request(self.url, new_query)
            new_hystory_elements = new_data.get('data').get('historyElements')
            return new_hystory_elements

        while has_next_page:
            hystory_elements = make_deep_request(hystory_elements.get('pageInfo').get('endCursor'))
            total_history = total_history + hystory_elements.get('nodes')
            has_next_page = hystory_elements.get('pageInfo').get('hasNextPage')
            
        return total_history

    def getHistoryElement(self, id):
        query = json.dumps(historyElement_by_id(id))
        data = self.__send_request(self.url, query)
        return data.text

    def fetchHistory(self):
        history_list = self.getHistoryList()
        self.history_elements = history_list
        
        return history_list
            

    def fetch_referenda_data(self, referenda_id_array):
        self.getReferendaList(referenda_id_array)
        for referenda_id, referendum in self.referenda_dict.items():
            for voter in referendum['data']['castingVotings']['nodes']:
                self.voter_dict[voter['voter']].append(voter)

        return self.voter_dict

    def getReferendaList(self, referenda_id_array):
        for referenda_id in referenda_id_array:
            print(f"Getting referenda data for {referenda_id}...")
            self.referenda_dict[referenda_id] = self.getReferendaById(referenda_id)

        return self.referenda_dict

    def getReferendaById(self, referenda_id):
        # query = json.dumps(referenda_by_id(referenda_id))
        query = json.dumps(small_data_referenda_by_id(referenda_id))
        data = self.__send_request(self.url, query)
        return data

    def getReferendaVotesForAddress(self, account_id):
        query = json.dumps(referenda_all_account_votes(account_id))
        data = self.__send_request(self.url, query)
        self.account_votes_dictionary[account_id] = data

        return data
    
    def getNovaAccumulatedRewards(self, account_id):
        query = json.dumps(nova_accumulated_rewards(account_id))
        data = self.__send_request(self.url, query)
        try:
            return data.get('data').get('accumulatedRewards').get('nodes')[0].get('amount')
        except:
            return '0'
        
    
    def getNovaRewards(self, account_id):
        total_rewards = []
        query = json.dumps(nova_account_rewards(account_id))
        data = self.__send_request(self.url, query)
        rewards = data.get('data').get('accountRewards')
        total_rewards = total_rewards + rewards.get('nodes')
        
        def make_deep_request(cursor):
            new_query = json.dumps(nova_account_rewards(account_id, cursor=cursor))
            new_data = self.__send_request(self.url, new_query)
            new_rewards = new_data.get('data').get('historyElements')
            return new_rewards
        
        while (len(rewards.get('nodes')) == 100):
            rewards = make_deep_request(rewards.get('pageInfo').get('endCursor'))
            total_rewards = total_rewards + rewards.get('nodes')
            
        return total_rewards
    
    
    def getMultichainAccumulatedRewards(self, account_id):
        query = json.dumps(multichain_accumulated_rewards(account_id))
        data = self.__send_request(self.url, query)
        
        return data.get('data').get('accumulatedRewards').get('nodes')[0].get('amount')
        
    def getMultichainRewards(self, account_id):
        total_rewards = []
        query = json.dumps(multichain_account_rewards(account_id))
        data = self.__send_request(self.url, query)
        rewards = data.get('data').get('rewards')
        total_rewards = total_rewards + rewards.get('nodes')
        
        def make_deep_request(cursor):
            new_query = json.dumps(multichain_account_rewards(account_id, cursor=cursor))
            new_data = self.__send_request(self.url, new_query)
            new_rewards = new_data.get('data').get('rewards')
            return new_rewards
        
        while (len(rewards.get('nodes')) == 100):
            rewards = make_deep_request(rewards.get('pageInfo').get('endCursor'))
            total_rewards = total_rewards + rewards.get('nodes')
            
        return total_rewards
    
    def getMultichainAmountRewards(self, account_id):
        query = json.dumps(multichain_accumulated_rewards_sum(account_id))
        data = self.__send_request(self.url, query)
        
        try:
            return data.get('data').get('rewards').get('groupedAggregates')[0].get('sum').get('amount')
        except:
            return '0'
    
    def collect_history_data_from_block(self, block, account_id):
        total_elements = []
        
        query = json.dumps(history_elements_restricted_by_block(account_id, block))
        data =self.__send_request(self.url, query)
        history_elements = data.get('data').get('historyElements')
        new_elements = total_elements + history_elements.get('nodes')
        
        def make_deep_request(cursor):
            new_query = json.dumps(history_elements_restricted_by_block(account_id, block, cursor=cursor))
            new_data = self.__send_request(self.url, new_query)
            new_elements = new_data.get('data').get('historyElements')
            return new_elements
        
        while (history_elements.get('pageInfo').get('hasNextPage') == True):
            history_elements = make_deep_request(history_elements.get('pageInfo').get('endCursor'))
            new_elements = new_elements + history_elements.get('nodes')
            
        return new_elements
        

    def get_multichain_accumulated_rewards(self, accounti_id):
        query = json.dumps(multichain_accumulated_rewards(accounti_id))
        data = self.__send_request(self.url, query)
        try:
            return data.get('data').get('accumulatedRewards').get('nodes')[0].get('amount')
        except:
            return '0'
    
    def nova_get_accumulated_reward(self, account_id, block):
        query = json.dumps(nova_accumulated_reward_by_account(account_id, block))
        data = self.__send_request(self.url, query)
        try:
            return data.get('data').get('accumulatedRewards').get('nodes')[0].get('amount')
        except:
            return '0'
            

    def __send_request(self, url, data):
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': 'd5a1d1cffde69e7cbff6d9c0cf1cca6d'
        }
        try:
            response = requests.request("POST", url, headers=headers, data=data)
            response_data = json.loads(response.text)
        except:
            time.sleep(5)
            return self.__send_request(url, data)

        # Workaround to cover case when SubQuery return an "Unexpected error"
        if 'message' in response_data:
            time.sleep(5)
            return self.__send_request(url, data)

        return response_data
