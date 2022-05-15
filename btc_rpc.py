import subprocess
import json
import random

WALLET="testing"

def exec(script):
    return subprocess.check_output(script, shell=True).decode('utf-8').strip()

def getnewaddress(legacy=True,wallet=WALLET):
    if legacy:
        x=exec("bitcoin-cli -rpcwallet="+wallet+" getnewaddress '' legacy")
    else:
        x=exec("bitcoin-cli -rpcwallet="+wallet+" getnewaddress")
    return x

def dumprivkey(addr,wallet=WALLET):
    x=exec("bitcoin-cli -rpcwallet="+wallet+" dumpprivkey "+addr)
    return x

def sendtoaddress(address, amount, wallet=WALLET):
    
    # print("Sending {} btc to {}".format(str(amount),address))
    x=exec("bitcoin-cli -rpcwallet="+wallet+" sendtoaddress "+address+" "+str(amount))
    return x

def sendspecific(ins, out, wallet=WALLET):
    '''
    assumes ins and out are lists of dicts
    ins = [{"txid":str(txid),"vout": int(vout)}]
    out = [{address:float(amt)}]

    assumes all inputs are from the same wallet
    '''

    command_string = 'bitcoin-cli -rpcwallet='+wallet+' createrawtransaction \"['

    for i in range(len(ins)):
        if i != len(ins)-1:
            command_string += '{\\"txid\\":\\"'+ins[i]["txid"]+'\\",\\"vout\\":'+str(ins[i]["vout"])+'},'
        else:
            command_string += '{\\"txid\\":\\"'+ins[i]["txid"]+'\\",\\"vout\\":'+str(ins[i]["vout"])+'}'
    command_string += ']\" \"['

    for i in range(len(out)):
        if i != len(out)-1:
            for k,v in out[i].items():
                command_string += '{\\"'+k+'\\":'+str(v)+"},"
        else:
            for k,v in out[i].items():
                command_string += '{\\"'+k+'\\":'+str(v)+"}"
    command_string += ']\"'
    txrawhex = exec(command_string)
   
    command_string_signed = 'bitcoin-cli -rpcwallet='+wallet+' signrawtransactionwithkey \"'+txrawhex+'\" \"['

    for i in range(len(ins)):
        txid_details = gettransaction(ins[i]['txid'])["details"]
        vout = ins[i]['vout']
        privkey = ""
        for j in range(len(txid_details)):
            if txid_details[j]['vout'] == vout:
                privkey = dumprivkey(txid_details[j]['address'], wallet)
                break
        if i != len(ins)-1:
            command_string_signed += '\\"'+ privkey+ '\\",'
        else:
            command_string_signed += '\\"'+ privkey +'\\"'
    command_string_signed += ']\"'
    
    signedtx = eval(exec(command_string_signed).replace('true', "True").replace('false', "False"))
    print(signedtx)
    if signedtx["complete"]:
        txhash = sendrawtransaction(signedtx["hex"], wallet)
        return txhash
    else:
        print("Error: Transaction not complete")
        return signedtx
    # return signedtx

def generatetoaddress(nblocks, address, wallet=WALLET):
    x=exec("bitcoin-cli -rpcwallet="+wallet+" generatetoaddress "+str(nblocks)+" "+address)
    return x

def sendrawtransaction(txhex, wallet=WALLET):
    x=exec("bitcoin-cli -rpcwallet="+wallet+' sendrawtransaction \"'+txhex+'\"')
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

def importaddress(addr,wallet=WALLET):
    x=exec("bitcoin-cli -rpcwallet="+wallet+" importaddress "+addr+" '' false")
    return x

if __name__ == "__main__":
    # x=getnewaddress()
    # amt = random.randint(1,3)
    # print("getting a new address",x)
    # print("sending {} btc to {}".format(amt,x))
    # txhash=sendtoaddress(x,amt,wallet="aliceWallet")
    # # print(txhash)
    # generatetoaddress(2, getnewaddress())
    # print(json.dumps(gettransaction(txhash),indent=4))
    # # print("decode transaction {}".format(txhash))
    # # print(decodetransaction(txhash))
    # print("this the private key of address {}".format(x))
    # # print(dumprivkey(x))

    txid1 = "7cb48e0e939f5e882c12405e2f2eca705e125325ac99b01d9460c6e1a7614be9"
    txid2 = "1d1878c13e91ddc34ff4a02ce4cb09fcd8141dcff9a7cfe43fecea70628291d0"

    amt = 40.005
    x=getnewaddress()

    # ins = [{"txid":str(txid),"vout": int(vout)}]
    ins = [{'txid':str(txid1),'vout': 0},{'txid':str(txid2),'vout': 0}]
    out = [{x:str(amt)}]
    
    generatetoaddress(2, getnewaddress())

    print("sending {} btc to {}".format(amt,x))
    print(sendspecific(ins, out, wallet="aliceWallet"))