from src.loger import *


def matching_values(subquery_data, subscan_data):
    print('Subquery data has: %s elements' % len(subquery_data))
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
    print('Subquery transfers: %s, extrinsics: %s, rewards: %s' %
          (len(subq_transfers), len(subq_extrinsics), len(subq_rewards)))

    for transfer in subq_transfers:
        value = transfer['transfer']['extrinsicId']
        subscan_data[:] = [d for d in subscan_data if d.get(
            'extrinsic_index') != value]
    for extrinsic in subq_extrinsics:
        value = extrinsic['id']
        subscan_data[:] = [d for d in subscan_data if d.get(
            'extrinsic_hash') != value]
    for reward in subq_rewards:
        value = reward['id']
        subscan_data[:] = [
            d for d in subscan_data if d.get('event_index') != value]

    return subscan_data
