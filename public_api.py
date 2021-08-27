import requests
import time

BASE_API_URL = "https://public-apis-api.herokuapp.com/api/v1/"
AUTH_ENDPOINT = BASE_API_URL + "auth/token"
LIST_OF_CATEGORIES_ENDPOINT = BASE_API_URL + "apis/categories"
API_DESCRIPTION_ENDPOINT = BASE_API_URL + "apis/entry"

SLEEP_DURATION = 2 # in seconds
EXTENDED_SLEEP_DURATION = 60  # in seconds

class PublicApi():
    
    def __get_auth_token(self):
        endpoint = AUTH_ENDPOINT
        response = requests.request("GET", endpoint).json()
        self._auth_token = response['token']

    def __send_request(self, request_type, **kwargs):
        
        headers  = {"Authorization": "Bearer " + self._auth_token}
        params = {}
        
        if request_type.lower() == "catg_list":
            endpoint = LIST_OF_CATEGORIES_ENDPOINT       
            params  = {"page": kwargs['page']}
            
        elif request_type.lower() == "api_desc":
            endpoint = API_DESCRIPTION_ENDPOINT       
            params  = {"category": kwargs['category'], "page": kwargs['page']}
            
        response = requests.request("GET", endpoint, headers=headers, params=params) 
        
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
        self.__get_auth_token()
    
    def get_list_of_all_categories(self):        
        break_flag = False
        category_list = []
        page = 1
        
        while (break_flag != True):            
            data = self.__send_request(request_type="catg_list", page=page).json()
            
            if len(data['categories']) == 0:
                break_flag = True
            else:
                category_list += data['categories']
                page += 1
                time.sleep(SLEEP_DURATION)
                
        return category_list
    
    def get_data_for_a_category(self, category):
        break_flag = False
        api_list = []
        page = 1
        
        while (break_flag != True):            
            data = self.__send_request(request_type="api_desc", category=category, page=page).json()
            
            if len(data['categories']) == 0:
                break_flag = True
            else:
                api_list += data['categories']
                page += 1
                time.sleep(SLEEP_DURATION)
                
        return api_list
    