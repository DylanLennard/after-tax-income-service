# After Tax Web Service  

## Summary  
Returns your after tax income assuming no write offs based on your income bracket.


## Currently (as of 11/15)  
* Processes via values from California State circa 2015.  
* Includes SSI and medicare.  

## How's It Work  
* Build the Docker Image  
* Load it to ECS  
* Deploy it via ECS on a cluster  

## TODO List  
* Set up with a domain name  
* Create Scraper to Update the income brackets and tax rates  
  * For state (CA) and for federal and for SSI/medicare  
  * Expand to get rates for other states too  
  * store data in JSON  
