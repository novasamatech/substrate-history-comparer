def historyElements_by_address(address):
    query = '{\n    historyElements(filter:{address:{equalTo:\"%s\"}}){\n    edges{\n      node{\n        id,\n        address,\n        extrinsic,\n        transfer,\n        reward,\n        timestamp\n      }\n    }\n  }\n}' % (address)
    return {"query": query}


def historyElement_by_id(id):
    query = '{\n    historyElement(id:\"%s\"){\n    id,\n    timestamp,\n    address,\n    reward,\n    extrinsic,\n    transfer\n  }\n}' % (
        id)
    return {"query": query}


def get_rewards(address):
    query = '{\n    historyElements(\n         orderBy: TIMESTAMP_DESC,\n         filter: {\n             address: { equalTo: \"%s\"},\n             reward: { isNull: false }\n         }\n     ) {\n        nodes {\n            id\n            timestamp\n            address\n            reward\n            extrinsic\n            transfer\n        }\n     }\n}' % (address)
    return {"query": query}
