# importing pytest module because we are doing a pytest to test functions in python
import pytest

# importing functions related to our "bp" variable from our routes.py file 
from routes import bp 

# creating a function to test the app's functions: the user popup function for logging in 
def user_popup(username):

        # putting the bp variable/function into test mode
        bp.testing = True 

        # creating temporary client to make a request to test the user popup function 
        client = bp.test_client()

        # HTTP Get request to the user_popup path  
        response = client.get('/user/<username>/popup') #here we are using the client with the .get method --
        # -- and the user popup URL/endpoint which is in our routes.py fille

        # we rely on status codes to check if we connected to the site right
        # if response == 200; then we are good to go

        print(response) # Would print <WrapperTestResponse streamed [200 OK]
        print(response.status_code) # This only prints 200

        # So we can instead write: 
        assert response.status_code == 200 #assert is testing a condition and will return nothing if the
        # condition is true 


        # now checking that the actual content of the popup page is correct
        # response.data outputs raw data from connecting to the site but in byte form: "b'string'"
        #print(response.data)
        # From the user_popup.html file, I tested the string and added a 'b' to format it as a byte
        assert b"Last seen on" in response.data
