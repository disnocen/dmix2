txhash=$1

bitcoin-cli -rpcwallet=testing gettransaction $txhash|jq .hex|xargs bitcoin-cli -rpcwallet=testing decoderawtransaction|jq '.vout'