from collections import defaultdict
import requests
import math
import json


data_dict = {'16936690-2': {'problem': True}, '16938105-5': {'problem': True}, '16946369-3': {'problem': True}, '16845782-2': {'problem': True}, '16643361-2': {'problem': True}, '16617821-5': {'problem': True}, '16671751-2': {'problem': True}, '16489219-3': {'problem': True}, '16542327-4': {'problem': True}, '16457445-2': {'problem': True}, '16347116-4': {'problem': True}, '16342955-4': {'problem': True}, '16342368-5': {'problem': True}, '16342383-3': {'problem': True}, '16342380-2': {'problem': True}, '16247677-2': {'problem': True}, '16247679-2': {'problem': True}, '16427972-2': {'problem': True}, '16247682-2': {'problem': True}, '16411663-4': {'problem': True}, '16342373-4': {'problem': True}, '16411660-3': {'problem': True}, '16397473-8': {'problem': True}, '16342370-3': {'problem': True}, '16218180-6': {'problem': True}, '16228859-3': {'problem': True}, '16228862-5': {'problem': True}, '16174714-2': {'problem': True}, '16174747-2': {'problem': True}, '15874829-4': {'problem': True}, '15843196-3': {'problem': True}, '15840973-3': {'problem': True}, '15826658-3': {'problem': True}, '15820649-2': {'problem': True}, '15820647-2': {'problem': True}, '15820589-2': {'problem': True}, '15817299-2': {'problem': True}, '15775652-2': {'problem': True}, '15869168-2': {'problem': True}, '15775147-2': {'problem': True}, '15771172-2': {'problem': True}, '15869170-2': {'problem': True}, '15754536-5': {'problem': True}, '15729333-4': {'problem': True}, '15730486-2': {'problem': True}, '15729332-2': {'problem': True}, '15730494-2': {'problem': True}, '15729330-2': {'problem': True}, '15729329-3': {'problem': True}, '15718224-5': {'problem': True}, '15718209-10': {'problem': True}, '15901668-2': {'problem': True}, '15730490-2': {'problem': True}, '15729337-3': {'problem': True}, '15718225-4': {'problem': True}, '15718187-4': {'problem': True}, '15719347-5': {'problem': True}, '15686333-2': {'problem': True}, '15686324-2': {'problem': True}, '15659434-4': {'problem': True}, '15659241-4': {'problem': True}, '15658592-4': {'problem': True}, '15658576-7': {'problem': True}, '15658508-4': {'problem': True}, '15658416-4': {'problem': True}, '15659441-2': {'problem': True}, '15659248-6': {'problem': True}, '15658606-6': {'problem': True}, '15658569-5': {'problem': True}, '15658404-3': {'problem': True}, '15656786-2': {'problem': True}, '15659444-2': {'problem': True}, '15659252-5': {'problem': True}, '15658600-9': {'problem': True}, '15658560-5': {'problem': True}, '15658395-2': {'problem': True}, '15656740-9': {'problem': True}, '15659664-5': {'problem': True}, '15659470-3': {'problem': True}, '15659470-2': {'problem': True}, '15659277-5': {'problem': True}, '15643853-2': {'problem': True}, '15643529-2': {'problem': True}, '15642773-2': {'problem': True}, '15642505-10': {'problem': True}, '15641812-5': {'problem': True}, '15638034-3': {'problem': True}, '15633229-2': {'problem': True}, '15626006-3': {'problem': True}, '15626003-3': {'problem': True}, '15659670-4': {'problem': True}, '15659484-2': {'problem': True}, '15659454-2': {'problem': True}, '15659264-6': {'problem': True}, '15643792-3': {'problem': True}, '15642828-3': {'problem': True}, '15641810-7': {'problem': True}, '15638028-3': {'problem': True}, '15633226-2': {'problem': True}, '15624112-2': {'problem': True}, '15623122-4': {'problem': True}, '15623118-2': {'problem': True}, '15719351-7': {'problem': True}, '15659725-3': {'problem': True}, '15659620-4': {'problem': True}, '15659446-3': {'problem': True}, '15659254-6': {'problem': True}, '15643885-2': {'problem': True}, '15643664-3': {'problem': True}, '15642454-4': {'problem': True}, '15641807-3': {'problem': True}, '15638026-3': {'problem': True}, '15632912-6': {'problem': True}, '15610808-3': {'problem': True}, '15610805-7': {'problem': True}, '15610429-2': {'problem': True}, '15597402-2': {'problem': True}, '15597399-2': {'problem': True}, '15659461-3': {'problem': True}, '15659269-11': {'problem': True}, '15643841-2': {'problem': True}, '15643513-5': {'problem': True}, '15643334-3': {'problem': True}, '15642872-3': {'problem': True}, '15610412-2': {'problem': True}, '15583195-3': {'problem': True}, '15583192-6': {'problem': True}, '15528650-2': {'problem': True}, '15490975-2': {'problem': True}, '15490969-2': {'problem': True}, '15490961-2': {'problem': True}, '15484656-3': {'problem': True}, '15483625-6': {'problem': True}, '15483622-5': {'problem': True}, '15483196-2': {'problem': True}, '15483194-2': {'problem': True}, '15659468-2': {'problem': True}, '15659276-5': {'problem': True}, '15643868-3': {'problem': True}, '15643600-6': {'problem': True}, '15642699-2': {'problem': True}, '15641804-5': {'problem': True}, '15633207-3': {'problem': True}, '15484658-4': {'problem': True}, '15483552-5': {'problem': True}, '15483549-10': {'problem': True}, '15482776-2': {'problem': True}, '15659466-2': {'problem': True}, '15659274-7': {'problem': True}, '15643875-3': {'problem': True}, '15643657-10': {'problem': True}, '15642887-3': {'problem': True}, '15641799-3': {'problem': True}, '15633193-2': {'problem': True}, '15484657-4': {'problem': True}, '15483529-6': {'problem': True}, '15483526-7': {'problem': True}, '15482771-2': {'problem': True}, '15468074-8': {'problem': True}, '15468072-7': {'problem': True}, '15659452-2': {'problem': True}, '15659262-2': {'problem': True}, '15644417-2': {'problem': True}, '15643488-5': {'problem': True}, '15642836-4': {'problem': True}, '15641797-3': {'problem': True}, '15633189-2': {'problem': True}, '15484654-4': {'problem': True}, '15483653-6': {'problem': True}, '15483650-7': {'problem': True}, '15482671-2': {'problem': True}, '15467021-2': {'problem': True}, '15467014-3': {'problem': True}, '15659464-3': {'problem': True}, '15659273-7': {'problem': True}, '15643861-2': {'problem': True}, '15643590-5': {'problem': True}, '15642825-3': {'problem': True}, '15642590-4': {'problem': True}, '15641795-4': {'problem': True}, '15633182-3': {'problem': True}, '15484657-3': {'problem': True}, '15483515-3': {'problem': True}, '15483504-4': {'problem': True}, '15482766-2': {'problem': True}, '15454186-3': {'problem': True}, '15452273-2': {'problem': True}, '15452270-2': {'problem': True}, '15659448-2': {'problem': True}, '15659260-8': {'problem': True}, '15643832-4': {'problem': True}, '15643497-5': {'problem': True}, '15641791-4': {'problem': True}, '15633173-2': {'problem': True}, '15484653-6': {'problem': True}, '15483636-6': {'problem': True}, '15483633-6': {'problem': True}, '15444953-2': {'problem': True}, '15440322-9': {'problem': True}, '15440306-2': {'problem': True}, '15659456-2': {'problem': True}, '15659266-8': {'problem': True}, '15644426-2': {'problem': True}, '15643749-8': {'problem': True}, '15643445-2': {'problem': True}, '15643250-2': {'problem': True}, '15642803-3': {'problem': True}, '15587220-3': {'problem': True}, '15484655-5': {'problem': True}, '15444908-2': {'problem': True}, '15440320-2': {'problem': True}, '15440301-3': {'problem': True}, '15428430-4': {'problem': True}}

def send_request(url, data):
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': 'd5a1d1cffde69e7cbff6d9c0cf1cca6d',
        'baggage': 'sentry-public_key=da3d374c00b64b6196b5d5861d4d1374,sentry-trace_id=fb6a06eb7a3c4ada9263c2451eadfba2,sentry-sample_rate=0.01',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    return requests.request("POST", url, headers=headers,
                            json=data)

def request_processor(url, payload):
        return_data = []
        first_response = send_request(
            url, payload_update(payload, 0)).json()
        count = int(first_response.get("data").get("count"))
        request_count = math.ceil(count/100)
        if count <= 100:
            return_data.append(first_response)
        else:
            for i in range(request_count):
                response = send_request(
                    url, payload_update(payload, i)).json()
                return_data.append(response)
        return return_data

def payload_update(payload, n) -> str:
    payload['page'] = n
    payload['row'] = 100
    return payload

def get_extrinsic_indexes(filename):
    extrinsic_indexes = []
    with open(filename, 'r') as f:
        for line in f:
            if 'extrinsic_index' in line:
                string_part = line.split('\'extrinsic_index\':')[-1].strip()
                index = string_part.split('\'')[1]
                extrinsic_indexes.append(index)
    return extrinsic_indexes

def was_vote_removed(extrinsic):
    extrinsic_payload = {"hash":extrinsic['extrinsic_hash'],"events_limit":10,"only_extrinsic_event":True,"focus":""}
    vote_detail = send_request('https://kusama.webapi.subscan.io/api/scan/extrinsic', extrinsic_payload)
    extrinsic_data = json.loads(vote_detail.text)['data']
    pol_index = [param['value'] for param in extrinsic_data['params'] if param['name'] == 'poll_index'][0]

    # Was votes removed by single call?
    payload_for_remove_vote = {"row":100,"page":0,"signed":"signed","address":extrinsic['account_display']['address'],"module":"convictionvoting","call":"remove_vote","no_params":True}
    call_list = request_processor('https://kusama.webapi.subscan.io/api/v2/scan/extrinsics', payload_for_remove_vote)
    for remove_vote_extr in call_list:
        if remove_vote_extr['data']['extrinsics'] is None:
            return False
        for data in remove_vote_extr['data']['extrinsics']:
            detailed_payload = {"hash":data['extrinsic_hash'],"events_limit":10,"only_extrinsic_event":True,"focus":""}
            temp_extr = send_request('https://kusama.webapi.subscan.io/api/scan/extrinsic', detailed_payload)
            detailed_temp_extr = json.loads(temp_extr.text)['data']
            for param in detailed_temp_extr['params']:
                if param['value'] == pol_index:
                    return True

    # Was votes removed by batch call?
    payload_for_batch = {"row":100,"page":0,"signed":"signed","address":extrinsic['account_display']['address'],"module":"utility","call":"batch","no_params":True}
    batch_list = request_processor('https://kusama.webapi.subscan.io/api/v2/scan/extrinsics', payload_for_batch)
    for batch_extr in batch_list:
        if batch_extr['data']['extrinsics'] is None:
            return False
        for data in batch_extr['data']['extrinsics']:
            detailed_batch_payload = {"hash":data['extrinsic_hash'],"events_limit":10,"only_extrinsic_event":True,"focus":""}
            temp_batch_extr = send_request('https://kusama.webapi.subscan.io/api/scan/extrinsic', detailed_batch_payload)
            detailed_temp_batch = json.loads(temp_batch_extr.text)['data']
            for param in detailed_temp_batch['params']:
                for call in param['value']:
                    if call.get('call_name', None) is None or call.get('call_module', None) is None:
                        continue
                    if call['call_name'] == 'remove_vote' and call['call_module'] == 'ConvictionVoting':
                        if call['params'][1]['value'] == pol_index:
                            return True

    return False

def request_data_from_subscan(indexes_array):
    batch_count = 0
    multisig_count = 0
    proxy_inside_batch_count = 0
    other_problems = defaultdict(dict)
    conviction_voting = defaultdict(dict)
    proxy_count = defaultdict(dict)
    for index in indexes_array:
        print(f'Processing failed extrinsics... {index}')
        payload = {"extrinsic_index":index,"events_limit":10,"only_extrinsic_event":True,"focus":""}
        response = send_request('https://kusama.webapi.subscan.io/api/scan/extrinsic', payload)
        extrinsic_data = json.loads(response.text)['data']
        if extrinsic_data['success'] is True:
            if extrinsic_data['call_module'] == 'utility':
                batch_count += 1
                processed = False
                for event in extrinsic_data['event']:
                    if event['module_id'] == 'proxy' and not processed:
                        proxy_inside_batch_count += 1
                        processed = True
                        continue
            elif extrinsic_data['call_module'] == 'multisig':
                multisig_count += 1
            elif extrinsic_data['call_module'] == 'convictionvoting':
                vote_removed = was_vote_removed(extrinsic_data)
                if vote_removed is not True:
                    conviction_voting[index] = {'problem': True}
            elif extrinsic_data['call_module'] == 'proxy':
                proxy_count[index] = {'problem': True}
            else:
                other_problems[index] = {'problem': True}
        else:
            print(f"Extrinsic was failed {extrinsic_data['extrinsic_hash']}")

        print(f'Batch count:{batch_count}, proxy_inside_batch:{proxy_inside_batch_count}, multisig_count:{multisig_count}, other problems:{len(other_problems)}, conviction votings: {len(conviction_voting)}, proxy_count: {len(proxy_count)}')
    print(other_problems)
    print(conviction_voting)
    print(proxy_count)

# indexes = get_extrinsic_indexes('result_2.txt')
indexes = [element for element in data_dict.keys()]
request_data_from_subscan(indexes)
