## simple_blockchain_server

# Test:
`make test`

# Prod:
`make prod`

A couple of sample requests in `web3.postman_collection.json`.

As curl:
```curl --location --request POST '127.0.0.1:8080/info/balance' \
--header 'Content-Type: application/json' \
--data-raw '{
    "network": "avalanche",
    "wallet": "0x416a7989a964C9ED60257B064Efc3a30FE6bF2eE",
    "block_num": "0x838388"
}'
```
```curl --location --request POST '127.0.0.1:8080/info/events' \
--header 'Content-Type: application/json' \
--data-raw '{
    "block_num": 22911056
}'
```