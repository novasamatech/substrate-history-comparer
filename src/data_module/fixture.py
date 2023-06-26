def historyElements_by_address(address):
    query = '{\n    historyElements(filter:{address:{equalTo:\"%s\"}}){\n    edges{\n      node{\n        id,\n        address,\n        extrinsic,\n        transfer,\n        reward,\n        timestamp\n      }\n    }\n  }\n}' % (address)
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
    query = 'query {accumulatedRewards(filter: {address:{equalTo:"%s"}}) {nodes {address amount}}}' % (account_id)
    
    return {"query": query}

def multichain_account_rewards(account_id, cursor=None):
    if cursor:
        query = 'query {rewards(filter: { address: {equalTo:"%s"}} after: "%s") {nodes {address amount id networkId accumulatedAmount type}pageInfo { startCursor endCursor}}}' % (account_id, cursor)
    else:
        query = 'query {rewards(filter: { address: {equalTo:"%s"}}) {nodes {address amount id networkId accumulatedAmount type}pageInfo { startCursor endCursor}}}' % (account_id)
    
    return {"query": query}

def nova_account_rewards(account_id, cursor=None):
    if cursor:
        query = 'query {\n        historyElements(\n            after: \"%s\",\n            first: 100,\n            orderBy: TIMESTAMP_DESC,\n            filter: { \n                address:{ equalTo: \"%s\"},\n                and: [{reward: {isNull: false}},{not: {and: [{extrinsic: {isNull: false}},{and: [{extrinsic: {contains: {module: \"balances\"}}},{or: [{extrinsic: {contains: {call: \"transfer\"}}},{extrinsic: {contains: {call: \"transferKeepAlive\"}}},{extrinsic: {contains: {call: \"transferAllowDeath\"}}},{extrinsic: {contains: {call: \"forceTransfer\"}}},{extrinsic: {contains: {call: \"transferAll\"}}}]}]}]}}]\n            }\n        ) {\n            pageInfo {\n                startCursor,\n                endCursor\n            },\n            nodes {\n                id\n                timestamp\n                extrinsicHash\n                address\n                reward\n                extrinsic\n                transfer\n            }\n        }\n    }' % (cursor, account_id)
    else:
        query = 'query {\n        historyElements(\n            after: null,\n            first: 100,\n            orderBy: TIMESTAMP_DESC,\n            filter: { \n                address:{ equalTo: \"%s\"},\n                and: [{reward: {isNull: false}},{not: {and: [{extrinsic: {isNull: false}},{and: [{extrinsic: {contains: {module: \"balances\"}}},{or: [{extrinsic: {contains: {call: \"transfer\"}}},{extrinsic: {contains: {call: \"transferKeepAlive\"}}},{extrinsic: {contains: {call: \"transferAllowDeath\"}}},{extrinsic: {contains: {call: \"forceTransfer\"}}},{extrinsic: {contains: {call: \"transferAll\"}}}]}]}]}}]\n            }\n        ) {\n            pageInfo {\n                startCursor,\n                endCursor\n            },\n            nodes {\n                id\n                timestamp\n                extrinsicHash\n                address\n                reward\n                extrinsic\n                transfer\n            }\n        }\n    }' % (account_id)
    
    return {"query": query}
