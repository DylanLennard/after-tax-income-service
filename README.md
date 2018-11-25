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
* Provide the status as a parameter  
* Modify output object to give more information  
    * Make it into a JSON object rather than a simple string  
* Set up with a domain name  
* Create Scraper to Update the income brackets and tax rates  
  * For state (CA) and for federal and for SSI/medicare  
  * Expand to get rates for other states too  
* Load Scraper Results to DB  
* Make DB requests in backend to get proper values for tax rates  
* Up security a little to make it all good
* Set up CI/CD with Jenkins  
