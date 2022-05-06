# Overview
Main File is 5.py
This file gets all metadata info like (TOKEN_METADATA) : 
1. Name 
2. Symbol
3. Decimals
4. Liquidity
5. Total Supply
6. Price of the token
7. MarketCap
8. Honeypot Status (for that we are using API)
9. Buy Tax
10. Sell Tax

Social Information for the token is not here, We don't even need that

## What needs to be done Further : 

models_tokenevent tables has new BSC coins with info : 
1. token0 (the contract address of the token)
2. token1 (Contract address or either WBNB/BUSD/USDT)
3. pair_address (Automated created wallet Address which saves token0 and token1 to create liquidity and price)
4. liquidity_pair (Symbol of token1 i.e Either - WBNB or BUSD or USDT)

for every token0 we can get TOKEN_METADATA information Which we will save in another table, with only metedata info and linking the models_tokenevent tables using id (uuid). Lets Call this new table as "models_tokenMetadata" which Contains all metadata fields mentioned above (10 columns) and 1 extra column i.e Updated_at which has the timestamp of when it was updated. For the first time when metedata is added it will contain timestamp at which it was added.

During Filling the data or Updating it, We follow the initial Criteria of classifying the tokens as - TOKENS or SPAM status. Update done every 2 hours and as per fresh data any coin can be turned from token to SPAM status or SPAM to TOKENS status if it fits the criteria. 

## CRITERIA :
1. if the liquidity_pair is WBNB, Liquidity should be atleast 25 and if the liquidity_pair is BUSD/USDT, Liquidity should be atleast 10,000 
2. Price should not be 0 ( can be 0.00000000000012 - just example, some coins have very low rate )
3. Honeypot should be False

If all above Criteria are passed the status is TOKENS else SPAM ((We dont Require POTENTIAL status since we are updating all token every 2 hours)

The models_token table can hold coins with status TOKENS which are updated (Reflected after every 2 hour update mentioned above). This Table is only used for BSC SIGNALS Compare and then continuing as it is now

# Few Concepts Used in File 5.py

## Understanding Pair Address, Liquidity & Price : 
Pair address is automatically created Wallet which stores 2 type of tokens. One is the newly minted token and other is more renowned token Like - WBNB (Which has a flutucating Price and is Main or Native token of BSC Blockchain) BUSD, USDT (Stable coins, price is always $1 per token ) and can be others too ( but are very less ). So a Pair Address has some number of token0 and token1.

So pair Address has 2 entities one newly created and one which is know. The Known Coins (WBNB/BUSD/USDT) provides Liquidity. <br>
so Basically Liquidity = Number of WBNB/BUSD/USDT or Number of token1 in Pair Address

and since it has 2 Token one know and other newly minted token which is token0 and token1 provides liquidity, <br>
Price of the Token (in USD ) is =  ((Number of token1 Coins * Price of token1 in USD ) / Number of token0 Coins) 

since BUSD and UDST are always $1, Price of token When token1 is BUSD or USDT = (Number of token1 Coins / Number of token0 Coins) <br>
and Price of Token when token1 is WBNB = (( Number of token1 Coins * Price of BNB in USD )/ Number of token0 Coins) 

## Understanding Market Cap : 
Market cap is Simply the total Value ot a token if its liquidated. so, <br>
Market Cap (in USD) = Total Supply * Price of Token in USD 
