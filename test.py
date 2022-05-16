from bitcoinutils.setup import setup
from bitcoinutils.keys import P2pkhAddress, PrivateKey, PublicKey
from bitcoinutils.setup import setup
from bitcoinutils.utils import to_satoshis
from bitcoinutils.transactions import Transaction, TxInput, TxOutput
from bitcoinutils.script import Script
import subprocess
import hashlib
from ecdsa import der
import btc_rpc as btc
setup('testnet')

# execute a bash script and return the output
def bash_output(script):
    return subprocess.check_output(script, shell=True).decode('utf-8').strip()
# def bash(script):
#     subprocess.call(script, shell=True)
# output a double sha256
def double_sha256(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest().hex()

# der encoding from r and s
def der_encode_sig(r, s):
    r=int(r,16)
    s=int(s,16)
    return der.encode_sequence(der.encode_integer(r), der.encode_integer(s))

def getscript(txhash,amountt):
    vv=subprocess.check_output(["/bin/sh", "-c","./gettxscript.sh "+txhash ]).decode('utf-8').strip()
    vv=eval(vv)
    print("vv is",vv)
    for i in vv:
        asm = i['scriptPubKey']['asm']
        n= i['n']
        print("value is",i['value'])
        # print("asm is {} of type {}".format(asm,type(asm)))
        if i["value"] == amountt:
            print("in if")
            print("asm is",asm.split())
            return (Script(asm.split()))

# sort list in alphabetical order
def sort_list(ll):
    return sorted(ll, key=lambda x: x.lower())
x=bash_output("pwd")
print("the directory is: " + x)
# print(bash("./demo/keygen.sh"))

# read file keys2.store and get the content of the file
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
print(pub.get_address().to_string())
print(pub.to_hex())


########################################

addr1="msEfKNiAEDMj2NMLH21n6cHafHmsULT5dN"
addr2="mhyZjdGjwyGc7h3dXAsTeYr728LDC3ubr1"
addr3="mgUuyfPT7xgkNUuCEcrye8WeWmxmTgEqP5"
addr4="mg8QfhauhZXLft18aDg9xsA2L5jTDGcLVE"


########################################
amountIn=110
amount= 108//3
txhash="e65da9451baa4b40ca7f3ddb7479311b47dc884838b43f315e40af9274b4abb9"

inscript=getscript(txhash, amountIn)
print("inscript is",inscript)
vout=0

########################################

 # create transaction input from tx id of UTXO (contained 0.4 tBTC)
txin = TxInput(txhash, vout,inscript)

 # create transaction output using P2PKH scriptPubKey (locking script)
addr1 = P2pkhAddress(addr1)
txout1 = TxOutput(to_satoshis(amount), Script(['OP_DUP', 'OP_HASH160', addr1.to_hash160(),'OP_EQUALVERIFY', 'OP_CHECKSIG']) )

addr2 = P2pkhAddress(addr2)
txout2 = TxOutput(to_satoshis(amount), Script(['OP_DUP', 'OP_HASH160', addr2.to_hash160(),'OP_EQUALVERIFY', 'OP_CHECKSIG']) )

addr3 = P2pkhAddress(addr3)
txout3 = TxOutput(to_satoshis(amount), Script(['OP_DUP', 'OP_HASH160', addr3.to_hash160(),'OP_EQUALVERIFY', 'OP_CHECKSIG']) )

addr4  = P2pkhAddress(addr4)
txout4 = TxOutput(to_satoshis(1.99), Script(['OP_DUP', 'OP_HASH160', addr4.to_hash160(),'OP_EQUALVERIFY', 'OP_CHECKSIG']) )

tx = Transaction([txin], [txout1, txout2, txout3, txout4])
digest=tx.get_transaction_digest(vout,inscript)

print("\nRaw unsigned transaction:\n" + tx.serialize())
txhashnew=double_sha256(bytes.fromhex(tx.serialize()))
txbytes=bytes(txhashnew, 'utf-8')

print("\ndouble hash Raw unsigned transaction:\n" + txhashnew)

subprocess.check_output(["/bin/sh", "-c","./demo/thsign.sh "+digest.hex() ]).decode('utf-8').strip()
# subprocess.check_output(["/bin/sh", "-c","./demo/thsign.sh"], input=txbytes.strip()).decode('utf-8').strip()


with open('./signature.json', 'r') as ff:
    sig = eval(ff.read())
ff.close()

print("the r of the signature is: " + sig["r"])
print("the s of the signature is: " + sig["s"])
r= sig["r"]
s= sig["s"]

dersig=der_encode_sig(r,s).hex()+'01'
print("signature der:", dersig)

txin.script_sig=Script([dersig,pub.to_hex()])
signed_tx = tx.serialize()

print("the whole transaction is:\n" + signed_tx)
# bf846bdf71f1c588b8abecdfa6296c91d408263ea13e44643a78a44f6549a1b8


# TODO:
# - decide which transactino to use
# - communication between parties
#     - fees
#     - amountOut
#     - amountIn
#     - addresses






# msxu7mAjB7kEENeHC1BsgLpCGEFtZxJ9ry;20.003;93661540b32b03cda43415995f7d6e7700e62918b63292dafaa863769c222ea6
# the one up is for aliceWallet of alice
# n3r6SkUN1espwVb2CgtnEa2Wn4qZX4nqYN;10.003;7eae209db1efb1091d7187d93456f6ba75247922d9512a1fac130326508f8d2b
# the one up is for bobWallet of bob
# mw4LLJ46Lkmudubjktxb8eEFGQsaTcw5JF;5.003;5b9ace84d2550bbb85ef6c587b956930d2cc727cbc27fcfed029d3bf1024f728
# the one up is for carolWallet of carol