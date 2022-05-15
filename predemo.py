import btc_rpc as btc
from bitcoinutils.setup import setup
from bitcoinutils.keys import P2pkhAddress, PrivateKey, PublicKey
from bitcoinutils.setup import setup
from bitcoinutils.utils import to_satoshis
from bitcoinutils.transactions import Transaction, TxInput, TxOutput
from bitcoinutils.script import Script
import hashlib
from ecdsa import der
import math

setup('testnet')


a_amt=20.012
b_amt=10.012
c_amt=5.012

fees=0.009

a_amt_rec = int(a_amt - (fees +fees//3))
b_amt_rec = int(b_amt - (fees +fees//3))
c_amt_rec = int(c_amt - (fees +fees//3))

amount_out = int(math.gcd(a_amt_rec, b_amt_rec, c_amt_rec))

a_req_addresses = a_amt_rec // amount_out
b_req_addresses = b_amt_rec // amount_out
c_req_addresses = c_amt_rec // amount_out



print("Alice Bob and Carol have three addresses:")
a_addr = btc.getnewaddress(legacy=True,wallet="aliceWallet")
print("Alice's address:", a_addr)

b_addr = btc.getnewaddress(legacy=True,wallet="bobWallet")
print("Bob's address:", b_addr)

c_addr = btc.getnewaddress(legacy=True,wallet="carolWallet")
print("Carol's address:", c_addr)

print()

a_txid = btc.sendtoaddress(a_addr,a_amt,wallet="testing")
b_txid = btc.sendtoaddress(b_addr,b_amt,wallet="testing")
c_txid = btc.sendtoaddress(c_addr,c_amt,wallet="testing")

btc.generatetoaddress(2, btc.getnewaddress())
print("Alice's balance:", btc.gettransaction(a_txid,wallet="aliceWallet")["amount"])
print("Bob's balance:", btc.gettransaction(b_txid,wallet="bobWallet")["amount"])
print("Carol's balance:", btc.gettransaction(c_txid,wallet="carolWallet")["amount"])

print()

print("the fees are: {}. Therefore:".format(fees))
print("Alice will receive {} btc".format(a_amt_rec))
print("Bob will receive {} btc".format(b_amt_rec))
print("Carol will receive {} btc".format(c_amt_rec))

print()

print("Since the GCD of the three amounts is {}".format(amount_out))
print("Alice will need {} addresses".format(a_req_addresses))
print("Bob will need {} addresses".format(b_req_addresses))
print("Carol will need {} addresses".format(c_req_addresses))

print()
input("Press Enter to continue...")

a_out_addr = [ btc.getnewaddress(legacy=True,wallet="aliceWallet") for i in range(a_req_addresses) ]
b_out_addr = [ btc.getnewaddress(legacy=True,wallet="bobWallet") for i in range(b_req_addresses) ]
c_out_addr = [ btc.getnewaddress(legacy=True,wallet="carolWallet") for i in range(c_req_addresses) ]

all_out_addresses = a_out_addr + b_out_addr + c_out_addr
all_out_addresses.sort()

print("these are the addresses that will be used:")
print(all_out_addresses)
print()

print("some of them belong to Alice, some of them to Bob, some to Carol. But you don't know which one!")

input("Press Enter to continue...")


print("They create a public key toghether. This is the public key that will be used to create the DMix instance. In practice, they control the public key together.")

btc.exec("./demo/keygen.sh")

with open('./keys2.store', 'r') as f:
    content = f.read()
f.close()

a= eval(content)[1]["y"]["point"]
# a= [2,229,44,186,242,228,15,79,21,78,148,183,200,188,203,93,35,233,29,132,25,168,27,215,97,8,160,97,51,118,78,55,11]

b = [hex(a[i])[2:] for i in range(len(a))]

for i in range(len(b)):
    if len(b[i]) == 1:
        b[i] = '0' + b[i]

# print(b)
b = ''.join(b)
# print(b)

pub = PublicKey.from_hex(b)
print("the DMix public key is:", pub.to_hex())
DMix_addr = P2pkhAddress(pub.get_address().to_string())
print("the DMix address is:", DMix_addr.to_string())


btc.importaddress(DMix_addr.to_string(),wallet="testing")

print()
input("Press Enter to continue...")


print("Now each party sends a transaction to the public key. This is the first transaction.")

print("Alice sends a transaction to the public key. the amount is she sends is {} btc".format(round(a_amt-fees,3)))
a_txin = btc.sendtoaddress(DMix_addr.to_string(),round(a_amt-fees,3),wallet="aliceWallet")
print("Alice's transaction to DMix:", a_txin)

print("Bob sends a transaction to the public key. the amount is he sends is {} btc".format(round(b_amt-fees,3)))
b_txin = btc.sendtoaddress(DMix_addr.to_string(),round(b_amt-fees,3),wallet="bobWallet")
print("Bob's transaction to DMix:", b_txin)

print("Carol sends a transaction to the public key. the amount is she sends is {} btc".format(round(c_amt-fees,3)))
c_txin = btc.sendtoaddress(DMix_addr.to_string(),round(c_amt-fees,3),wallet="carolWallet")
print("Carol's transaction to DMix:", c_txin)

btc.generatetoaddress(7, btc.getnewaddress())


print()
print("DMix balance:", btc.gettransaction(a_txin,wallet="testing")["amount"]+btc.gettransaction(b_txin,wallet="testing")["amount"]+btc.gettransaction(c_txin,wallet="testing")["amount"])
input("Press Enter to continue...")




