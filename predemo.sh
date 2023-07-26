#!/bin/sh

echo "this is predemo.sh"

a_addr=$(bitcoin-cli -rpcwallet=aliceWallet getnewaddress "" legacy)
b_addr=$(bitcoin-cli -rpcwallet=bobWallet getnewaddress "" legacy)
c_addr=$(bitcoin-cli -rpcwallet=carolWallet getnewaddress "" legacy)


a_txhash=$(bitcoin-cli -rpcwallet=testing sendtoaddress $a_addr 20.003)
b_txhash=$(bitcoin-cli -rpcwallet=testing sendtoaddress $b_addr 10.003)
c_txhash=$(bitcoin-cli -rpcwallet=testing sendtoaddress $c_addr 5.003)

echo "Alice's address: $a_addr and txhash: $a_txhash"
echo "Bob's address: $b_addr and txhash: $b_txhash"
echo "Carol's address: $c_addr and txhash: $c_txhash"

# bitcoin-cli -rpcwallet=testing generatetoaddress  105 bcrt1qkut7d6pwtj6t6lk768ldzggghnpt7ptx7scrjs > /dev/null
echo "{'Alice':{'address':'$a_addr','txhash':'$a_txhash'},'Bob':{'address':'$b_addr','txhash':'$b_txhash'},'Carol':{'address':'$c_addr','txhash':'$c_txhash'}}" > demo_data.json