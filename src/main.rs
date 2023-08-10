use bitcoin::blockdata::opcodes;
// use bitcoin::network::constants::Network;
use bitcoin::script::Builder;
use bitcoin::secp256k1::{rand, Secp256k1};
use bitcoin::ScriptBuf;
use bitcoin::{Address, Network, PublicKey};

fn main() {
    // Generate random key pair.
    let s = Secp256k1::new();
    // let public_key = PublicKey::new(s.generate_keypair(&mut thread_rng()).1);
    let public_key = PublicKey::new(s.generate_keypair(&mut rand::thread_rng()).1);

    // print public key.
    println!("the public key is: {}", public_key);

    /////// addrresses /////
    //
    // pub enum Network {
    //     Bitcoin,
    //     Testnet,
    //     Signet,
    //     Regtest,
    // }
    let network = Network::Regtest;

    // Generate pay-to-pubkey-hash address.
    let address_p2pkh = Address::p2pkh(&public_key, network);
    println!("p2pkh address: {}", address_p2pkh); //because returns an address

    let address_p2wpkh = Address::p2wpkh(&public_key, network);
    match address_p2wpkh {
        // because returns Result<Address, Error>
        Ok(address) => println!("p2wpkh address: {}", address),
        Err(e) => println!("p2wpkh address error: {}", e),
    }

    /////// scripts /////
    //
    // create new p2sh script
    // let script = bitcoin::blockdata::script::Builder::new();
    let script = ScriptBuf::new();
    println!("script: {}", script);
    // use the p2pkh script
    let script_p2pkh = ScriptBuf::new_p2pkh(&public_key.pubkey_hash());
    println!("script: {}", script_p2pkh);

    // create a simple script with just an opcode
    let script2 = Builder::new()
        .push_opcode(opcodes::all::OP_RETURN)
        .push_opcode(opcodes::all::OP_CHECKSIG)
        .into_script();
    println!("script2: {}", script2);

    // obtain the p2sh address from that script
    let address_p2sh = Address::p2sh(&script2, network);
    match address_p2sh {
        // because returns Result<Address, Error>
        Ok(address) => println!("p2sh address: {}", address),
        Err(e) => println!("p2sh address error: {}", e),
    }

    // obtain the p2wsh address from that script
    let address_p2wsh = Address::p2wsh(&script2, network);
    println!("p2wsh address: {}", address_p2wsh); //because returns an address
}
