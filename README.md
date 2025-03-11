# Tools

This is simple tool to crack encrypted PEM keys.

usage: python3 brute_pem_key.py [-h] -p PEM -w WORDLIST [-t THREADS]

for example:
python3 brute_pem_key.py -p private.key -w ~/tools/wordlists/SecLists/Passwords/xato-net-10-million-passwords-100000.txt


python3 brute_pem_key.py -p private.key -w ~/tools/wordlists/SecLists/Passwords/xato-net-10-million-passwords-100000.txt -t 6
[+] Attempting to brute-force private.key with 100000 passwords using 6 threads...


Progress:   1%|▊        | 1145/100000
[+] Password found: secret


Problems?
1) Test Key format: 
You should be able to dump the ASN.1 content directly from the PEM format using openssl asn1parse

% openssl asn1parse -inform pem -in private.key            
    0:d=0  hl=4 l=1316 cons: SEQUENCE          
    4:d=1  hl=2 l=  86 cons: SEQUENCE          
    6:d=2  hl=2 l=   9 prim: OBJECT            :PBES2
   17:d=2  hl=2 l=  73 cons: SEQUENCE          
   19:d=3  hl=2 l=  49 cons: SEQUENCE          
   21:d=4  hl=2 l=   9 prim: OBJECT            :PBKDF2
   32:d=4  hl=2 l=  36 cons: SEQUENCE          
   34:d=5  hl=2 l=  16 prim: OCTET STRING      [HEX DUMP]:DC4A3A932A01CB9CBA79A313FA6C8235
   52:d=5  hl=2 l=   2 prim: INTEGER           :0800
   56:d=5  hl=2 l=  12 cons: SEQUENCE          
   58:d=6  hl=2 l=   8 prim: OBJECT            :hmacWithSHA256
   68:d=6  hl=2 l=   0 prim: NULL              
   70:d=3  hl=2 l=  20 cons: SEQUENCE          
   72:d=4  hl=2 l=   8 prim: OBJECT            :des-ede3-cbc
   82:d=4  hl=2 l=   8 prim: OCTET STRING      [HEX DUMP]:7FF65648A65169F1
   92:d=1  hl=4 l=1224 prim: OCTET STRING      [HEX DUMP]:037BD567FE91B68852FF0F4.........
