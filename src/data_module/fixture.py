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

def multichain_account_rewards(account_id, cursor=None):
    if cursor:
        query = 'query {rewards(filter: { address: {equalTo:"%s"}} after: "%s") {nodes {address amount id networkId accumulatedAmount type}pageInfo { startCursor endCursor}}}' % (account_id, cursor)
    else:
        query = 'query {rewards(filter: { address: {equalTo:"%s"}}) {nodes {address amount id networkId accumulatedAmount type}pageInfo { startCursor endCursor}}}' % (account_id)
    
    return {"query": query}