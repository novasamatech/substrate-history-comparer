from collections import defaultdict
import requests
import math
import json


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
    payload = {"row":100,"page":0,"signed":"signed","address":extrinsic['account_display']['address'],"module":"convictionvoting","call":"remove_vote","no_params":True}
    response = request_processor('https://kusama.webapi.subscan.io/api/v2/scan/extrinsics', payload)
    for remove_vote_extr in response:
        if remove_vote_extr['data']['extrinsics'] is None:
            return False
        for data in remove_vote_extr['data']['extrinsics']:
            detailed_payload = {"hash":data['extrinsic_hash'],"events_limit":10,"only_extrinsic_event":True,"focus":""}
            temp_extr = send_request('https://kusama.webapi.subscan.io/api/scan/extrinsic', detailed_payload)
            detailed_temp_extr = json.loads(temp_extr.text)['data']
            for param in detailed_temp_extr['params']:
                if param['value'] == pol_index:
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

indexes = get_extrinsic_indexes('results_3.txt')
# indexes = [element for element in data_dict.keys()]
request_data_from_subscan(indexes)
