# CAPSTONE_1_dateMeetApp_FULL_CRUD
dateMeet is a full CRUD app that allows users identify exciting businesses in their location matching their entered interest. This app makes use of the Google Geocode API to collect and verify acurate user location and uses the Yelp API to retrieve businesses matching the users interest and in a 10km radius.

# Documentation

1. dateMeet is a social media CRUD app built for the purpose of allowing it's users to find businesses for what ever kind of dates they are interested in withn 10km of their current location.
 Using the YELP API allows dateMeet to access different businesses based on interests which are displayed on the platform. dateMeet also allows users to enter business recommendations for different locations,
 and view business recommendations in their current location.
2. Details:  
a. The title of this website is dateMeet, [click the link to use]().  
b. dateMeet prompts you to enter your address which is verified using the Google Geocode API and saved to the PostgreSQL database, it then saves this enetered location in flask global environment,
and pulls it when the user searches for locations by interest. Once the search button is clicked, a client side request is made using AJAX to retrieve all businesses within a 10km radius matching 
the entered interest.  
c. Key features include:    
  i. Register.   
  ii. Login.   
 iii. Location Entry.   
 iv.Date location search.   
 v. Business recommendation entry.   
 vi. Business recommendation edit.    
 vii. Location edit.  
 viii. User edit.  
 ix. Recommendation like and unlike.  
 x. Recommendation delete.  
 xi. User delete.  
 
d. Standard User Flow:  
 - Starts on the anonymous homepage with the nav bar showing registration and login links.  
 - If user does not have an active account, user can go ahead and create one with the register link.  
 - Once an account is created, dateMeet takes user to the location form where the user is asked to enter their current location. 
 - Once user enters a valid location, they are taken to the date location search page where they can enter their interest.  
 - If user already has an account and has previously entered in a location before, when they log in, they are taken to the date location search page where they can enter their interests.  
 - Once an interest is entered and the search button is clicked, all businesses within a 10km radius matching the entered interest are displayed on the same page.  
 - If no businesses, a message is displayed.  
 - In the navbar, there is a search bar that allows the current user search other users.  
 - In the navbar there is also a link to Recommendations where logged in user can view recommendations. Based on the users current location, this link renders recommendations for that location.  
 - If no recommendations exist, a message is displayed.  
 - Also in the navbar, there is a link to view user profile, here the user can edit their account, add a recommendation, delete their account, view liked recommendations, followers, other users 
 they are following and their own recommendations.  
 
e. APIS used:  
 - [Google Geocode Api](https://developers.google.com/maps/documentation/geocoding/start). 
 - [YELP Fusion API](https://www.yelp.com/developers/documentation/v3/get_started). 

f. Technology stack and frameworks used to create dateMeet include:  
 - HTML5. 
 - CSS.  
 - Javascript.  
 - Bootstrap 4.5.  
 - Python.  
 - Fask.  
 - SQLAlchemy.  
 - PostgreSQL.  
 
