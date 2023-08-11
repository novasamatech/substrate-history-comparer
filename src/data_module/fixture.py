def historyElements_by_address(address, cursor=None):
    if cursor:
        query = '{historyElements(after: "%s" filter: {address: {equalTo: "%s"}}) {totalCount nodes {address assetTransfer blockNumber extrinsic extrinsicHash extrinsicIdx id nodeId reward timestamp transfer}pageInfo {endCursor hasNextPage}}}' % (cursor, address)
    else:
        query = '{historyElements(filter: {address: {equalTo: "%s"}}) {totalCount nodes {address assetTransfer blockNumber extrinsic extrinsicHash extrinsicIdx id nodeId reward timestamp transfer}pageInfo {endCursor hasNextPage}}}' % (address)
    return {"query": query}

def historyElement_by_id(id):
    query = '{\n    historyElement(id:\"%s\"){\n    id,\n    timestamp,\n    address,\n    reward,\n    extrinsic,\n    transfer\n  }\n}' % (id)
    return {"query": query}

def referenda_by_id(id):
    query = "query {\n   referendums(filter: {id: {equalTo: \"%s\"}}){\n    nodes {\n      id\n      trackId\n      finished\n      castingVotings {\n        edges {\n          node {\n            id\n            at\n            voter\n            delegateId\n            referendumId\n            standardVote\n            splitVote\n            splitAbstainVote\n            delegate {\n              id\n              accountId\n              delegatorVotes\n              delegators\n              delegateVotes{\n                nodes{\n                  id\n                  at\n                  voter\n                  delegateId\n                  referendumId\n                  standardVote\n                  splitVote\n                  splitAbstainVote\n                  delegate {\n                    id\n                  }\n                  referendum {\n                    id\n                  }\n                }\n              }\n            }\n            referendum {\n              id\n            }\n            delegatorVotes {\n              edges {\n                node {\n                  id\n                }\n              }\n            }\n          }\n        }\n      }\n      delegatesByCastingVotingReferendumIdAndDelegateId {\n        edges {\n          node {\n            id\n          }\n        }\n      }\n    }\n  }\n}"  % (id)
    return {"query": query}

def small_data_referenda_by_id(id):
    query = "query {castingVotings(filter: { referendumId: {equalTo: \"%s\"}}) {nodes {referendumId standardVote splitVote splitAbstainVote voter } } delegatorVotings(filter: {delegator: {equalTo: \"%s\"}}) { nodes {vote parent { referendumId delegate { accountId } standardVote } } } }" % (id, id)
    return {"query": query}

def referenda_all_account_votes(account_id):
    query = 'query {\n    castingVotings (filter: {voter: {equalTo: \"%s\"}}) {\n        nodes {\n          id\n          at\n          voter\n          delegateId\n          referendumId\n          standardVote\n          splitVote\n          splitAbstainVote\n          delegate{\n            id\n    accountId delegatorVotes delegators      },\n          referendum{\n            id\n          },\n          delegatorVotes{\n            nodes{\n              id\n            }\n          }\n        }\n    }\n}' % (account_id)
    return {"query": query}

def nova_accumulated_rewards(account_id):
    query = 'query {accumulatedRewards(filter: {id:{equalTo:"%s"}}) {nodes {id amount}}}' % (account_id)
    
    return {"query": query}

def multichain_accumulated_rewards(account_id):
    query = 'query {accumulatedRewards(filter: {address:{equalTo:"%s"}}) {nodes {address amount id networkId nodeId stakingType}}}' % (account_id)
    
    return {"query": query}

def multichain_account_rewards(account_id, cursor=None):
    if cursor:
        query = 'query {rewards(filter: { address: {equalTo:"%s"}} after: "%s") {nodes {address amount id networkId accumulatedAmount type}pageInfo { startCursor endCursor}}}' % (account_id, cursor)
    else:
        query = 'query {rewards(filter: { address: {equalTo:"%s"}}) {nodes {address amount id networkId accumulatedAmount type}pageInfo { startCursor endCursor}}}' % (account_id)
    
    return {"query": query}

def nova_account_rewards(account_id, cursor=None):
    if cursor:
        query = 'query {after: \"%s\", accountRewards(first: 100, filter: {address: {equalTo:"%s"}}) {nodes {id address blockNumber timestamp accumulatedAmount amount nodeId type } pageInfo {endCursor startCursor}}}' % (cursor, account_id)
    else:
        query = 'query {accountRewards(first: 100, filter: {address: {equalTo:"%s"}}) {nodes {id address blockNumber timestamp accumulatedAmount amount nodeId type } pageInfo {endCursor startCursor}}}' % (account_id)
    
    return {"query": query}

def multichain_accumulated_rewards_sum(account_id):
    query = 'query {rewards(filter: {or: [{ address: {equalTo:"%s"}}]}) {groupedAggregates(groupBy: [NETWORK_ID,  STAKING_TYPE]) {sum {amount}keys}}}' % (account_id)
    
    return {"query": query}

def history_elements_restricted_by_block(account_id, block, cursor=None):
    if cursor:
        query = 'query {historyElements(after: "%s" filter: {address: {equalTo: "%s"}, blockNumber:{lessThanOrEqualTo: %s}}) {pageInfo {endCursor hasNextPage} nodes { address assetTransfer blockNumber extrinsic extrinsicHash extrinsicIdx id nodeId reward timestamp transfer}}}' % (cursor, account_id, block)
    else:
        query = 'query {historyElements(filter: {address: {equalTo: "%s"}, blockNumber:{lessThanOrEqualTo: %s}}) {pageInfo {endCursor hasNextPage} nodes { address assetTransfer blockNumber extrinsic extrinsicHash extrinsicIdx id nodeId reward timestamp transfer}}}' % (account_id, block)
    
    return {"query": query}

def nova_accumulated_reward_by_account(account_id, block):
    query = "{accumulatedRewards(filter: {id: {equalTo: \"%s\"}}blockHeight: \"%s\") {nodes {amount id nodeId}}}" % (account_id, block)
    return {"query": query}
