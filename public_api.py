# ------------------------------------------------------------------------------
# Name:         PublicApi Class Implementation (Postman Hiring Challenge - 2021)
# Created By:   Pritthijit Nath
# Email:        pritthijit.nath@icloud.com
# Place:        Kolkata, India
# ------------------------------------------------------------------------------

import requests
import time

# Initializing the API endpoints
BASE_API_URL = "https://public-apis-api.herokuapp.com/api/v1/"
AUTH_ENDPOINT = BASE_API_URL + "auth/token"
LIST_OF_CATEGORIES_ENDPOINT = BASE_API_URL + "apis/categories"
API_DESCRIPTION_ENDPOINT = BASE_API_URL + "apis/entry"

# Initializing the sleep time duration
SLEEP_DURATION = 2  # in seconds
EXTENDED_SLEEP_DURATION = 60  # in seconds


class PublicApi():

    """
    PuplicApi class to extract data from https://public-apis-api.herokuapp.com/

    ...

    Attributes
    ----------
    auth_token : str
        Authentication token to query the public-apis api

    Methods
    -------
    Private:
        __get_auth_token()
            Extracts and sets the auth_token from the public-apis api auth endpoint

        __send_request(request_type, **kwargs)
            Helper method to extract data from different requests

    Public:
        get_list_of_all_categories()
            Extracts the list of all the categories served in the public-apis api

        get_data_for_a_category(category)
            Extracts the list of different apis for each category from the public-apis api

    """

    def __get_auth_token(self):
        """Extracts and sets the auth_token from the public-apis api auth endpoint"""
        endpoint = AUTH_ENDPOINT
        response = requests.request("GET", endpoint).json()
        self._auth_token = response['token']

    def __send_request(self, request_type, **kwargs):
        """Helper method to extract data from different requests

        Parameters
        ----------
        request_type : str
            Category of request to be made. 
                "catg_list" - Extract list of categories
                "api_desc"  - Extract the list of apis for a category
            Contains added functionality to handle token expiry and rate limit exceeded issues

        page : int, optional
            Page number to pass into the request

        category : str, optional
            Category for which to extract list of apis and their description

        """

        headers = {"Authorization": "Bearer " + self._auth_token}
        params = {}

        if request_type.lower() == "catg_list":
            endpoint = LIST_OF_CATEGORIES_ENDPOINT
            params = {"page": kwargs['page']}

        elif request_type.lower() == "api_desc":
            endpoint = API_DESCRIPTION_ENDPOINT
            params = {"category": kwargs['category'], "page": kwargs['page']}

        response = requests.request(
            "GET", endpoint, headers=headers, params=params)

        if response.status_code == 403:
            print("Token failure ... fetching new token")
            self.__get_auth_token()
            response = self.__send_request(request_type, **kwargs)

        if response.status_code == 429:
            print("Too many requests ... waiting for 1 minute")
            time.sleep(EXTENDED_SLEEP_DURATION)
            response = self.__send_request(request_type, **kwargs)

        return response

    def __init__(self):
        """Initializes the instance by setting the auth token"""
        self.__get_auth_token()

    def get_list_of_all_categories(self):
        """Extracts the list of all the categories served in the public-apis api"""
        break_flag = False
        category_list = []
        page = 1

        while (break_flag != True):
            data = self.__send_request(
                request_type="catg_list", page=page).json()

            if len(data['categories']) == 0:
                break_flag = True
            else:
                category_list += data['categories']
                page += 1
                time.sleep(SLEEP_DURATION)

        return category_list

    def get_data_for_a_category(self, category):
        """Extracts the list of different apis for each category from the public-apis api

        Parameters
        ----------
        category : str
            Category of request to be made. 

        """

        break_flag = False
        api_list = []
        page = 1

        while (break_flag != True):
            data = self.__send_request(
                request_type="api_desc", category=category, page=page).json()

            if len(data['categories']) == 0:
                break_flag = True
            else:
                api_list += data['categories']
                page += 1
                time.sleep(SLEEP_DURATION)

        return api_list
