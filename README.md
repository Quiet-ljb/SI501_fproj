# SI507 final project
## File Description
**fproj.py:** Load data from the cache (json file) and store it. Create user interface

**city_data.json:** Cache the data from the yelp api and website

**load_data.py:** Store data into the cache (It needs to be run if there is no file called city_data.json)

**test.ipynb:** It's used to debug

## Insturctions 
**Step 1:** Get an API key
 * Go to link https://www.yelp.com/developers/v3/manage_app  
 * In the create new app form, enter information about your app, then agree to Yelp API Terms of Use and Display Requirements. Then click the Submit button.  
 * Your API key is generated  
  
**Step 2:** Load data ((If city_data.json doesn't exist or needs to be refreshed)) 
 * Download the file `load\_data.py`
 * Replace the variable `api\_key` with your API key generated in the first step
 * Run command `python load\_data.py`
 * You will see file city\_data.json is generated or refreshed  
  
**Step 3:** Run the server
 * Download the file fproj.py
 * Run command `python fproj.py`
 * Open your web browser, enter url ''localhost:5000'' or''127.0.0.1:5000'' to enter the website

**Step 4:** Interact with the program
 * You will see four options after entering the website
 * Click on the options you want to choose  
 * For the first two options, enter the query you want to search and click the search button
 * For the last two options, click on the result you are interested at  

## Data Structure
All data was stored in a prefix tree, where all children of a node have common prefix stored in their parent node. Below shows an example about the prefix tree. Instead of storing those words in the figure, we store city name in the tree. Also, this tree is not case-sensitive and ignores the white space (e.g. ``Ann Arbor'' will be stored as ``annarbor'' in this tree  

![Prefix tree example](ex.PNG)
