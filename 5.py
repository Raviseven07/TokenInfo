from settings import PANCAKESWAP_FACTORY, PANCAKESWAP_ROUTER, PANCAKESWAP_FACTORY_ABI, PANCAKESWAP_ROUTER_ABI, ERC20_ABI, MAX_AMOUNT, HONEYPOT_CONTRACT, HONEYABI, WBNB_CONTRACT
from web3 import Web3
from time import time
import requests
import time 
import psycopg2

#This Link is a BSC NODE, Parallel BlockChain of BSC.  
provider = Web3(Web3.HTTPProvider("https://aged-floral-water.bsc.quiknode.pro/734a08fd43e85f73a1fd97d23938d484b6c1f483/"))

# PanCakeSwap Setting Necessary to connect the to the Original Contract of Tokens
ROUTER = provider.eth.contract(PANCAKESWAP_ROUTER, abi=PANCAKESWAP_ROUTER_ABI)
FACTORY = provider.eth.contract(PANCAKESWAP_FACTORY, abi=PANCAKESWAP_FACTORY_ABI)
HONEY = provider.eth.contract(address=HONEYPOT_CONTRACT, abi=HONEYABI)

# 3 Pair, Out of Which we can find which one is the Liq Pair. Not needed by us Since we have this info by BSC_Events Api (BSCScan.com)
BNBCA='0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'
BUSDCA='0xe9e7cea3dedca5984780bafc599bd69add087d56'
USDTCA='0x55d398326f99059fF775485246999027B3197955'

#String Converted in Readable Contract Tpye
BNBCA1 = provider.toChecksumAddress(BNBCA) #this is Basically BNBCA, Will be used 1st to check for Liq. Pair
BUSDCA1 = provider.toChecksumAddress(BUSDCA)
USDTCA1 = provider.toChecksumAddress(USDTCA)



Bkey = "https://api.binance.com/api/v3/ticker/price?symbol=BNBBUSD"
Bdata = requests.get(Bkey)  
Bdata = Bdata.json()
BNBPrice = Bdata['price'] # Getting BNB Price for Calculating Price of Token Later (for only those whoe Liquidity is in BNB)
#BNBPrice=1

connection = psycopg2.connect(user="postgres",
                                  password="@@@2021@APPle@@@",
                                  host="database-1.cbaz5xem6cy7.ap-south-1.rds.amazonaws.com",
                                  port="5432")
cursor = connection.cursor()
postgreSQL_select_Query = "select * from models_tokenevent order by block_no desc limit 1"

cursor.execute(postgreSQL_select_Query)
db_records = cursor.fetchall()



def current_milli_time():
    return round(time.time() * 1000)



def TokenMetadata(token):

        if liq_pair =='WBNB':
           tokenContract = provider.eth.contract(BNBCA1, abi=ERC20_ABI)
        else:
            if liq_pair =='BUSD':
                tokenContract = provider.eth.contract(BUSDCA1, abi=ERC20_ABI)
            else:
                tokenContract = provider.eth.contract(USDTCA1, abi=ERC20_ABI)

        # Gives Liquidity of the Token in WBNB/USDT/BUSD which ever Liquidity pair it has 
        Liquidity = provider.fromWei(tokenContract.functions.balanceOf(provider.toChecksumAddress(pairAddress)).call(), 'ether') 

        # Setting Contract of the Token  to gets its INFO
        tokenContract1 = provider.eth.contract(token, abi=ERC20_ABI)

        # Gives Symbol of the Token  
        symbol = tokenContract1.functions.symbol().call()   

        # Gives Name of the Token                                                                             
        tokenName = tokenContract1.functions.name().call()  

        # Gives Decimals of the Token                                                                              
        tokenDecimals = tokenContract1.functions.decimals().call()   


        

        # Gives Total Supply of the Token                                                                   
        tokenTotalSupply = tokenContract1.functions.totalSupply().call() / (pow(10,tokenDecimals))                                      

        # Gives token Amount in Pair Address, Used to Calculate Price of the Token
        token0value = tokenContract1.functions.balanceOf(provider.toChecksumAddress(pairAddress)).call() / (pow(10,tokenDecimals))  

        # Gives Price of the Token   
        if liq_pair =='WBNB':
            if token0value == 0:
                tokenPrice=0
            else:
                Liquidity_in_USD = float(Liquidity) * float(BNBPrice)
                tokenPrice = float(Liquidity_in_USD) / float(token0value)      
        else:
            if token0value == 0:
                tokenPrice=0
            else:
                tokenPrice = float(Liquidity) / float(token0value)


        # Gives BUy Tax, Sell Tax, Honeypot Status of the Token
        HPot = "https://honeypot.api.rugdoc.io/api/honeypotStatus.js?address=" + token + "&chain=bsc"
        HPotData = requests.get(HPot)  
        HPotData = HPotData.json()
        HStatus = HPotData['status']     

        if HStatus=='OK':
            tokenInfos = HONEY.functions.getTokenInformations(token).call()
            buy_tax = round((tokenInfos[0] - tokenInfos[1]) / tokenInfos[0] * 100 ,2) 
            sell_tax = round((tokenInfos[2] - tokenInfos[3]) / tokenInfos[2] * 100 ,2)
            honeypot = False  
        else:
            buy_tax = "NA" 
            sell_tax = "NA"
            honeypot = True  

            
        
        # Gives Market Cap of the Token 
        tokenMarketCap = float (tokenTotalSupply) * float(tokenPrice) 

        print("\n")
        print(f"Token Name : {tokenName}, Token Synbol : {symbol}")
        print(f"LiQ Pair : {liq_pair}, Pair Address : {pairAddress}, Token Price : {tokenPrice}, Token Total Supply : {tokenTotalSupply}")
        print(f"Token Liquidity : {provider.fromWei(Liquidity, 'ether')} {liq_pair}, Token Market Cap : {tokenMarketCap}")
        print(f"Buy Tax : {buy_tax} %, Sell Tax : {sell_tax} %, Honeypot : {honeypot}")
        print("\n\n\n")


aa = time.time()
for row in db_records:
        temptoken=row[5]        # 6th Column in Table is for token0
        pairAddress = row[8]    # 9th Column in Table is pair_address
        liq_pair = row[7]       # 8th Column in Table is pair_address

        print("\n\nContrcat Address sent from DB : " , temptoken) 
        token = provider.toChecksumAddress(temptoken) # Providing token0 
        TokenMetadata(token) #Calling Main Function


bb = time.time()
cc = bb - aa 
print(f"Time Elapsed : {cc} Second")
print("\n\n\n") 

 