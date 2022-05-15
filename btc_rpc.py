import subprocess

WALLET="testing"

def exec(script):
    return subprocess.check_output([script], shell=True).decode('utf-8').strip()

def getnewaddress(legacy=True,wallet=WALLET):
    if legacy:
        x=exec("bitcoin-cli -rpcwallet="+wallet+" getnewaddress '' legacy")
    else:
        x=exec("bitcoin-cli -rpcwallet="+wallet+" getnewaddress")
    return x

def sendtoaddress(address, amount, wallet=WALLET):
    x=exec("bitcoin-cli -rpcwallet="+wallet+" sendtoaddress "+address+" "+str(amount))
    return x

def generatetoaddress(nblocks, address, wallet=WALLET):
    x=exec("bitcoin-cli -rpcwallet="+wallet+" generatetoaddress "+str(nblocks)+" "+address)
    return x

def sendrawtransaction(txhex, wallet=WALLET):
    x=exec("bitcoin-cli -rpcwallet="+wallet+" sendrawtransaction "+txhex)
    return x

def getbalance(wallet=WALLET):
    x=exec("bitcoin-cli -rpcwallet="+wallet+" getbalance")
    return x

def gettransaction(txid, wallet=WALLET):
    x=exec("bitcoin-cli -rpcwallet="+wallet+" gettransaction "+txid)
    # print(x)
    return eval(x.replace("true","True").replace("false","False"))

def gettransactionhex(txid, wallet=WALLET):
    x=gettransaction(txid, wallet)
    return x["hex"]

def decodetransaction(txid, wallet=WALLET):
    txhex=gettransactionhex(txid, wallet)
    x=exec("bitcoin-cli -rpcwallet="+wallet+" decoderawtransaction "+txhex)
    return x

def createwallet(wallet):
    x=exec("bitcoin-cli createwallet "+wallet)
    return x


if __name__ == "__main__":
    x=getnewaddress()
    print("getting a new address",x)
    print("sending 1 btc to {}".format(x))
    txhash=sendtoaddress(x,1)
    print(txhash)
    # generatetoaddress(10, getnewaddress())
    print("decode transaction {}".format(txhash))
    print(decodetransaction(txhash))
    print("decode transaction {}".format("9bbd2d44b3bdc0b66dbf739ec2fdba1056b175500510feae0471201f79505227"))
    print(decodetransaction("9bbd2d44b3bdc0b66dbf739ec2fdba1056b175500510feae0471201f79505227"))