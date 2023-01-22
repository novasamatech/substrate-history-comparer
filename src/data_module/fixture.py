def historyElements_by_address(address):
    query = '{\n    historyElements(filter:{address:{equalTo:\"%s\"}}){\n    edges{\n      node{\n        id,\n        address,\n        extrinsic,\n        transfer,\n        reward,\n        timestamp\n      }\n    }\n  }\n}' % (address)
    return {"query": query}

def historyElement_by_id(id):
    query = '{\n    historyElement(id:\"%s\"){\n    id,\n    timestamp,\n    address,\n    reward,\n    extrinsic,\n    transfer\n  }\n}' % (id)
    return {"query": query}

def referenda_by_id(id):
    query = "query {\n   referendums(filter: {id: {equalTo: \"%s\"}}){\n    nodes {\n      id\n      trackId\n      finished\n      castingVotings {\n        edges {\n          node {\n            id\n            at\n            voter\n            delegateId\n            referendumId\n            standardVote\n            splitVote\n            splitAbstainVote\n            delegate {\n              id\n              accountId\n              delegatorVotes\n              delegators\n              delegateVotes{\n                nodes{\n                  id\n                  at\n                  voter\n                  delegateId\n                  referendumId\n                  standardVote\n                  splitVote\n                  splitAbstainVote\n                  delegate {\n                    id\n                  }\n                  referendum {\n                    id\n                  }\n                }\n              }\n            }\n            referendum {\n              id\n            }\n            delegatorVotes {\n              edges {\n                node {\n                  id\n                }\n              }\n            }\n          }\n        }\n      }\n      delegatesByCastingVotingReferendumIdAndDelegateId {\n        edges {\n          node {\n            id\n          }\n        }\n      }\n    }\n  }\n}"  % (id)
    return {"query": query}

def referenda_all_account_votes(account_id):
    query = 'query {\n    castingVotings (filter: {voter: {equalTo: \"%s\"}}) {\n        nodes {\n          id\n          at\n          voter\n          delegateId\n          referendumId\n          standardVote\n          splitVote\n          splitAbstainVote\n          delegate{\n            id\n    accountId delegatorVotes delegators      },\n          referendum{\n            id\n          },\n          delegatorVotes{\n            nodes{\n              id\n            }\n          }\n        }\n    }\n}' % (account_id)
    return {"query": query}