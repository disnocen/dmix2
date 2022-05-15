#!/usr/bin/env bash
file_as_string=`cat params.json`

n=`echo "$file_as_string" | cut -d "\"" -f 4 `
t=`echo "$file_as_string" | cut -d "\"" -f 8 `

message="$1"

for i in $(seq 1 $((t+1)));
do
    echo "signing for client $i out of $((t+1))"
    ./target/release/examples/gg18_sign_client http://127.0.0.1:8000 keys$i.store $message &
    sleep 3
done > procedure.txt

info=$(cat procedure.txt|grep SecretKey|sort|uniq|grep -o "SecretKey(.*)"|sed s/SecretKey//|tr -d '('|tr -d ')')
 
r=$(echo $info|cut -d" " -f1)
s=$(echo $info|cut -d" " -f2)
# killall gg18_sm_manager 2> /dev/null

cat << EOF > signature.json
{
  "r": "$r",
  "s": "$s"
} 
