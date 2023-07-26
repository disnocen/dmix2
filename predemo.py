import btc_rpc as btc
from bitcoinutils.setup import setup
from bitcoinutils.keys import P2pkhAddress, PrivateKey, PublicKey
from bitcoinutils.utils import to_satoshis
from bitcoinutils.transactions import Transaction, TxInput, TxOutput
from bitcoinutils.script import Script
from bitcoinutils.constants import SIGHASH_ALL, SIGHASH_NONE, SIGHASH_SINGLE, SIGHASH_ANYONECANPAY

import hashlib
from ecdsa import der
import math
import subprocess
import time

setup('testnet')


def pubfromwif(wif):
    priv = PrivateKey.from_wif(wif)
    pub = priv.get_public_key().to_hex()
    return pub


def verifysig(txhash, r, s, pub):
    sig = r+s
    sig = bytes.fromhex(sig)
    message = bytes.fromhex(txhash)
    pub = bytes.fromhex(pub)
    vk = ecdsa.VerifyingKey.from_string(
        pub, curve=ecdsa.SECP256k1, hashfunc=sha256)  # the default is sha1
    vk.verify(sig, message)  # True

# der encoding from r and s


def der_encode_sig(r, s):
    r = int(r, 16)
    s = int(s, 16)
    return der.encode_sequence(der.encode_integer(r), der.encode_integer(s))


decs = 6
a_amt = 20.0
b_amt = 10.0
c_amt = 5.0

fees = round(6 * 10**-decs, decs)
fees_third = round((fees / 3) + 10**-decs, decs)
print("fees:", fees)
print("fees_third:", fees_third)
print("fees total:", round(fees + fees_third, decs))
input("Press Enter to continue...")

a_amt = round(a_amt + fees + fees_third, decs)
b_amt = round(b_amt + fees + fees_third, decs)
c_amt = round(c_amt + fees + fees_third, decs)


# to get the right int need the `round` workaround
a_amt_rec = int(round(a_amt - (fees + fees_third), 1))
b_amt_rec = int(round(b_amt - (fees + fees_third), 1))
c_amt_rec = int(round(c_amt - (fees + fees_third), 1))

amount_out = int(math.gcd(a_amt_rec, b_amt_rec, c_amt_rec))

a_req_addresses = a_amt_rec // amount_out
b_req_addresses = b_amt_rec // amount_out
c_req_addresses = c_amt_rec // amount_out

test_addr = btc.getnewaddress(legacy=True, wallet="testing")

print("Alice Bob and Carol have three addresses:")
a_addr = btc.getnewaddress(legacy=True, wallet="aliceWallet")
a_pub = pubfromwif(btc.dumprivkey(a_addr, wallet="aliceWallet"))
print("Alice's address:", a_addr)

b_addr = btc.getnewaddress(legacy=True, wallet="bobWallet")
b_pub = pubfromwif(btc.dumprivkey(b_addr, wallet="bobWallet"))
print("Bob's address:", b_addr)

c_addr = btc.getnewaddress(legacy=True, wallet="carolWallet")
c_pub = pubfromwif(btc.dumprivkey(c_addr, wallet="carolWallet"))
print("Carol's address:", c_addr)

print()

# a_txid = btc.sendtoaddress(a_addr, a_amt, wallet="testing")
# b_txid = btc.sendtoaddress(b_addr, b_amt, wallet="testing")
# c_txid = btc.sendtoaddress(c_addr, c_amt, wallet="testing")

a_txid = btc.sendtoaddress(a_addr, a_amt, wallet="aliceWallet")
b_txid = btc.sendtoaddress(b_addr, b_amt, wallet="bobWallet")
c_txid = btc.sendtoaddress(c_addr, c_amt, wallet="carolWallet")

# btc.generatetoaddress(2, btc.getnewaddress())
print("sleeping 20 sec")
[print(i, end='\r') or time.sleep(1) for i in range(20, 0, -1)]


a_txid_vout = btc.getvoutfromamount(a_txid, a_amt, wallet="aliceWallet")
b_txid_vout = btc.getvoutfromamount(b_txid, b_amt, wallet="bobWallet")
c_txid_vout = btc.getvoutfromamount(c_txid, c_amt, wallet="carolWallet")

print("Alice's balance:", btc.gettransaction(
    a_txid, wallet="aliceWallet")["amount"])
print("Bob's balance:", btc.gettransaction(
    b_txid, wallet="bobWallet")["amount"])
print("Carol's balance:", btc.gettransaction(
    c_txid, wallet="carolWallet")["amount"])

print()

print(f"The fees are: {fees}. Therefore:")
print(f"Alice will receive {a_amt_rec} btc")
print(f"Bob will receive {b_amt_rec} btc")
print(f"Carol will receive {c_amt_rec} btc")

print()

print(f"Since the GCD of the three amounts is {amount_out}")
print(f"Alice will need {a_req_addresses} addresses")
print(f"Bob will need {b_req_addresses} addresses")
print(f"Carol will need {c_req_addresses} addresses")

print()
input("Press Enter to continue...")

a_out_addr = [btc.getnewaddress(legacy=True, wallet="aliceWallet")
              for i in range(a_req_addresses)]
b_out_addr = [btc.getnewaddress(legacy=True, wallet="bobWallet")
              for i in range(b_req_addresses)]
c_out_addr = [btc.getnewaddress(legacy=True, wallet="carolWallet")
              for i in range(c_req_addresses)]

### INSErt sending from alice to bob here #####
all_out_addresses = a_out_addr + b_out_addr + c_out_addr
all_out_addresses.sort()

print("these are the addresses that will be used:")
print(all_out_addresses)
print()

print("some of them belong to Alice, some of them to Bob, some to Carol. But you don't know which one!")

input("Press Enter to continue...")


print("They create a public key toghether. This is the public key that will be used to create the DMix instance. In practice, they control the public key together.")

print(btc.exec("./demo/keygen.sh"))

with open('./keys2.store', 'r') as f:
    content = f.read()
f.close()

a = eval(content)[1]["y"]["point"]
# a= [2,229,44,186,242,228,15,79,21,78,148,183,200,188,203,93,35,233,29,132,25,168,27,215,97,8,160,97,51,118,78,55,11]

b = [hex(a[i])[2:] for i in range(len(a))]

for i in range(len(b)):
    if len(b[i]) == 1:
        b[i] = '0' + b[i]

# print(b)
b = ''.join(b)
# print(b)

DMix_pub = PublicKey.from_hex(b)
print("the DMix public key is:", DMix_pub.to_hex())
DMix_addr = P2pkhAddress(DMix_pub.get_address().to_string())
print("the DMix address is:", DMix_addr.to_string())


btc.importaddress(DMix_addr.to_string(), wallet="testing")

print()
input("Press Enter to continue...")


print("Now each party sends a transaction to the public key. This is the first transaction.")

print("Alice sends a transaction to the public key. the amount is she sends is {} btc".format(
    round(a_amt-fees, decs)))
a_ins = [{"txid": a_txid, "vout": a_txid_vout}]
a_outs = [{DMix_addr.to_string(): round(a_amt-fees, decs)}]
a_txid_indmix = btc.sendspecific(a_ins, a_outs, wallet="aliceWallet")
a_txid_indmix_vout = btc.getvoutfromamount(
    a_txid_indmix, round(a_amt-fees, decs), wallet="aliceWallet")
print("Alice's transaction to DMix:", a_txid_indmix)

print("Bob sends a transaction to the public key. the amount is he sends is {} btc".format(
    round(b_amt-fees, decs)))
b_ins = [{"txid": b_txid, "vout": b_txid_vout}]
b_outs = [{DMix_addr.to_string(): round(b_amt-fees, decs)}]
b_txid_indmix = btc.sendspecific(b_ins, b_outs, wallet="bobWallet")
b_txid_indmix_vout = btc.getvoutfromamount(
    b_txid_indmix, round(b_amt-fees, decs), wallet="bobWallet")
print("Bob's transaction to DMix:", b_txid_indmix)

print("Carol sends a transaction to the public key. the amount is she sends is {} btc".format(
    round(c_amt-fees, decs)))
c_ins = [{"txid": c_txid, "vout": c_txid_vout}]
c_outs = [{DMix_addr.to_string(): round(c_amt-fees, decs)}]
c_txid_indmix = btc.sendspecific(c_ins, c_outs, wallet="carolWallet")
c_txid_indmix_vout = btc.getvoutfromamount(
    c_txid_indmix, round(c_amt-fees, decs), wallet="carolWallet")
print("Carol's transaction to DMix:", c_txid_indmix)

indmix_tx_data = [{"txid": a_txid_indmix, "vout": a_txid_indmix_vout, "script": btc.getscriptfromvout(a_txid_indmix, a_txid_indmix_vout, wallet="aliceWallet"), "pub": a_pub}, {"txid": b_txid_indmix, "vout": b_txid_indmix_vout, "script": btc.getscriptfromvout(
    b_txid_indmix, b_txid_indmix_vout, wallet="bobWallet"), "pub": b_pub}, {"txid": c_txid_indmix, "vout": c_txid_indmix_vout, "script": btc.getscriptfromvout(c_txid_indmix, c_txid_indmix_vout, wallet="carolWallet"), "pub": c_pub}]

# sort indmix_tx_data by the txids; this is needed to create the DMix transaction with the same order as the other parties
indmix_tx_data.sort(key=lambda x: x['txid'])

# used to advance chain
# btc.generatetoaddress(7, btc.getnewaddress())
# sleep 20 sec
print("sleeping 20 sec")
[print(i, end='\r') or time.sleep(1) for i in range(20, 0, -1)]


print()
print("DMix balance:", abs(btc.gettransaction(a_txid_indmix, wallet="aliceWallet")["amount"])+abs(btc.gettransaction(
    b_txid_indmix, wallet="bobWallet")["amount"])+abs(btc.gettransaction(c_txid_indmix, wallet="carolWallet")["amount"]))
input("Press Enter to continue...")

print()
print("Now Alice and Bob and Carol have to spend funds from the DMix address. This is the second transaction.\nAll parties have the transaction id to spend from the DMix address:\n{}\nthe amount of the outputs is {} and the list of receiving addresses is:\n{}\n\nShould we start?".format(indmix_tx_data, amount_out, all_out_addresses))
input("Press Enter to continue...")

dmix_tx_in0 = TxInput(indmix_tx_data[0]["txid"], indmix_tx_data[0]["vout"], Script(
    indmix_tx_data[0]["script"].split()))
dmix_tx_in1 = TxInput(indmix_tx_data[1]["txid"], indmix_tx_data[1]["vout"], Script(
    indmix_tx_data[1]["script"].split()))
dmix_tx_in2 = TxInput(indmix_tx_data[2]["txid"], indmix_tx_data[2]["vout"], Script(
    indmix_tx_data[2]["script"].split()))

addr_out0 = P2pkhAddress(all_out_addresses[0])
dmix_tx_out0 = TxOutput(to_satoshis(amount_out), Script(
    ['OP_DUP', 'OP_HASH160', addr_out0.to_hash160(), 'OP_EQUALVERIFY', 'OP_CHECKSIG']))

addr_out1 = P2pkhAddress(all_out_addresses[1])
dmix_tx_out1 = TxOutput(to_satoshis(amount_out), Script(
    ['OP_DUP', 'OP_HASH160', addr_out1.to_hash160(), 'OP_EQUALVERIFY', 'OP_CHECKSIG']))

addr_out2 = P2pkhAddress(all_out_addresses[2])
dmix_tx_out2 = TxOutput(to_satoshis(amount_out), Script(
    ['OP_DUP', 'OP_HASH160', addr_out2.to_hash160(), 'OP_EQUALVERIFY', 'OP_CHECKSIG']))

addr_out3 = P2pkhAddress(all_out_addresses[3])
dmix_tx_out3 = TxOutput(to_satoshis(amount_out), Script(
    ['OP_DUP', 'OP_HASH160', addr_out3.to_hash160(), 'OP_EQUALVERIFY', 'OP_CHECKSIG']))

addr_out4 = P2pkhAddress(all_out_addresses[4])
dmix_tx_out4 = TxOutput(to_satoshis(amount_out), Script(
    ['OP_DUP', 'OP_HASH160', addr_out4.to_hash160(), 'OP_EQUALVERIFY', 'OP_CHECKSIG']))

addr_out5 = P2pkhAddress(all_out_addresses[5])
dmix_tx_out5 = TxOutput(to_satoshis(amount_out), Script(
    ['OP_DUP', 'OP_HASH160', addr_out5.to_hash160(), 'OP_EQUALVERIFY', 'OP_CHECKSIG']))

addr_out6 = P2pkhAddress(all_out_addresses[6])
dmix_tx_out6 = TxOutput(to_satoshis(amount_out), Script(
    ['OP_DUP', 'OP_HASH160', addr_out6.to_hash160(), 'OP_EQUALVERIFY', 'OP_CHECKSIG']))

# dmix_tx = Transaction([dmix_tx_in0], [dmix_tx_out0,dmix_tx_out1,dmix_tx_out2,dmix_tx_out3])
dmix_tx = Transaction([dmix_tx_in0, dmix_tx_in1, dmix_tx_in2], [
                      dmix_tx_out0, dmix_tx_out1, dmix_tx_out2, dmix_tx_out3, dmix_tx_out4, dmix_tx_out5, dmix_tx_out6])

digest0 = dmix_tx.get_transaction_digest(0, Script(
    indmix_tx_data[0]["script"].split()), sighash=SIGHASH_ALL | SIGHASH_ANYONECANPAY)
digest1 = dmix_tx.get_transaction_digest(1, Script(
    indmix_tx_data[1]["script"].split()), sighash=SIGHASH_ALL | SIGHASH_ANYONECANPAY)
digest2 = dmix_tx.get_transaction_digest(2, Script(
    indmix_tx_data[2]["script"].split()), sighash=SIGHASH_ALL | SIGHASH_ANYONECANPAY)

print("the parties sign the digest of first input of the transaction", digest0.hex())
# print("the script is","./demo/thsign.sh "+digest0.hex())
# btc.exec("sh ./demo/thsign.sh "+digest0.hex())
subprocess.check_output(
    ["/bin/sh", "-c", "./demo/thsign.sh "+digest0.hex()]).decode('utf-8').strip()
with open('./signature.json', 'r') as ff:
    sig = eval(ff.read())
ff.close()
r = sig["r"]
s = sig["s"]
# print("Is the digest well signed?", verify_sig(digest0,r,s,)
# 81 is for the SIGHASH_ALL|SIGHASH_ANYONECANPAY
dersig0 = der_encode_sig(r, s).hex()+'81'
dmix_tx_in0.script_sig = Script([dersig0, DMix_pub.to_hex()])

print("the parties sign the second input of the transaction")
btc.exec("./demo/thsign.sh "+digest1.hex())
with open('./signature.json', 'r') as ff:
    sig = eval(ff.read())
ff.close()
r = sig["r"]
s = sig["s"]
dersig1 = der_encode_sig(r, s).hex()+'81'
dmix_tx_in1.script_sig = Script([dersig1, DMix_pub.to_hex()])

print("the parties sign the third input of the transaction")
subprocess.check_output(
    ["/bin/sh", "-c", "./demo/thsign.sh "+digest2.hex()]).decode('utf-8').strip()
with open('./signature.json', 'r') as ff:
    sig = eval(ff.read())
ff.close()
r = sig["r"]
s = sig["s"]
dersig2 = der_encode_sig(r, s).hex()+'81'
dmix_tx_in2.script_sig = Script([dersig2, DMix_pub.to_hex()])

signed_tx = dmix_tx.serialize()
print("the whole transaction is:\n" + signed_tx)
input("Press Enter to send the transaction to the blockchain...")
print("sending the transaction to the blockchain...")
dmix_tx_hash = btc.sendrawtransaction(signed_tx)
print("the transaction hash is: " + dmix_tx_hash)
