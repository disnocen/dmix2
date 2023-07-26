bitcoin-cli -regtest loadwallet testing
address=$(bitcoin-cli -regtest --rpcwallet=testing getnewaddress)

watch -n 10 "bitcoin-cli --rpcwallet=testing -regtest generatetoaddress 1 $address"

