from src.data_module.addresses import kusama_addresses, polkadot_addresses

class Networks:
    polka = ["polkadot", 10,
             'https://api.subquery.network/sq/ef1rspb/fearless-wallet', polkadot_addresses]
    kusama = ["kusama", 12,
              'https://api.subquery.network/sq/ef1rspb/fearless-wallet-ksm', kusama_addresses]
    westend = ['westend', 12]


network = Networks.polka
addresses = network[3]

url_extrinsics = 'https://%s.api.subscan.io/api/scan/extrinsics' % (network[0])
url_rewards = 'https://%s.api.subscan.io/api/scan/account/reward_slash' % (
    network[0])
url_transfers = 'https://%s.api.subscan.io/api/scan/transfers' % (network[0])
subquery_url = network[2]