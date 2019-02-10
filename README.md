# web-map

Program, built with the use of HTML & Python technologies, that shows movies  
 on the map according to the choice of the user.
 
 ### Getting started:
 
 #### contents of the project
 * main.py - main program that generates an HTML script with map
 * get_info.py - gets data from the user
 * parser.py - reads and processes csv file
 * requirements.txt - all the needed packages & their versions
 * README.md - detailed information about project
 
 #### packages, needed to be installed
 * folium - package that creates the HTML map, and add markers based on the year, entered by the user.
 * geopy - package, that converts locations from file *locations.csv* to coordinates in format (latitude, longtitude).
 * tqdm - package, that is decided to be used to add more user-friendly functionality.
 
 ### installation guide
 + download web-map repository
 + install packages listed above with following commands:
 ```
pip install -r  requirements.txt
 ```
 *In case of problems with package installation, try*
 ```
 pip install --upgrade pip
 ```
 + run ```python main.py``` and follow instructions, given in the command line
 
 P.S: In recent years, the amount of films, has grew rapidly, so in case you choose year in range from 1910 to 2024,
 get ready to wait some time, till program will end running.
 
 Advice: if ```Too Many Requests 429 error``` keeps occuring, enter year less than 1910 or try encreasing ```min_delay_seconds```
 int the ```RateLimiter``` settings.
 
#### Purpose:
- learn about new HTML tags and their attributes
- get acquinted with new developing tools, such as folium, geopy
 
#### Description of the HTML structure

``` <!DOCTYPE html> ``` - document type declaration
``` <html> ``` - container for the document
``` <head> ``` - the container for technical information
``` <script> ``` -  used to describe scripts
``` <link> ``` - sets the connection with external document
``` <style> ``` - sets style for the web page
``` <meta> ``` - save important information for browsers
``` <div> ``` - defines a section/part in an HTML document.

#### Conclusion
 Map has three layers, that serves a great source for different kind of information. **First layer** shows the density of
 the movies: that is, depending on the amount of movies, filmed in one place, the color of the circle will be different.
 **Second layer** is responsible for adding markers to the places where movies were filmed in the year, entered by the user.
 **Third layer** gives information about the poplation in countries. In the left bottom corner there is a legend, that helps
 to understand, what each color means.
 
