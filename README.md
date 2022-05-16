# README

This repository contains a demonstration of how DMix works[^aa].
The paper can be found at <https://www.researchgate.net/profile/Fadi-Barbara/publication/347266094_DMix_decentralized_mixer_for_unlinkability/links/60a3ec17a6fdcc74c1761384/DMix-decentralized-mixer-for-unlinkability.pdf>

You can find a video [here](https://fadibarbara.it/owncloud/index.php/s/YfnedvpveDdzMle) on how to play the demo

## TL;DR
Just enter the directory of the repository, and do:
```
python3 predemo.py
```

You'll get many error if this is the first time you use it. Read below for the proper way to operate the demonstration.

## requisite
You'll need the bitcoin core suite and the rust library on [multi-party ecdsa by ZenGo](https://github.com/ZenGo-X/multi-party-ecdsa)

### Bitcoin Core
Before starting  make sure `bitcoind` is running and you have a `./bitcoin.conf` file similar to those provided by the repository.

Start `bitcoind` in regtest as follows:

```
bitcoind -regtest -daemon -fallbackfee=0.09
```
 This will remove the need to specify the fees in transactions

 If this is the first time you operate, then you should create the wallets:

```
bitcoin-cli createwallet testing
bitcoin-cli createwallet aliceWallet
bitcoin-cli createwallet bobWallet
bitcoin-cli createwallet carolWallet

bitcoin-cli loadwallet testing
bitcoin-cli loadwallet aliceWallet
bitcoin-cli loadwallet bobWallet
bitcoin-cli loadwallet carolWallet
```

Then give you, in the `testing` wallet, some coins

```
addr=$(bitcoin-cli -rpcwallet=testing getnewaddress )
bitcoin-cli -repwallet=testing generatetoaddress 200 $addr
```

### Multiparty ECDSA
This library is used to operate the distributed key generation and the threshold signatures.

Compile the necessary programs by doing:
```
cargo +nightly build --examples --release
```

Obv, you should have a working installation of Rust, the nightly verstion

### Python
Assuming you have `pip` installed on your machine, do

```
pip install -r requisite.txt
```

then finally do 
```
python3 predemo.py
```

Then just press "Enter" to advance into the demo

***

for any problem contact me at:
- email: me [atsign] fadibara dot it
- telegram: @fadiabarbara

or open a issue here