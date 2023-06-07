from requests import get
import sp365_authentication

spAuthData = {
    #OAuth 2.0 Values
    'tenant_id': '',
    'client_id': '',
    'client_secret': '',
    'sp_siteName': '',
}

class sp365Rest:
    #Importing Auth Data
    auth = sp365_authentication.sp_api(spAData=spAuthData)
    site_api = auth.get_site_api_url()
    site_list_api = None
    site_auth_token = auth.token_type + ' ' + auth.access_token
    site_accept = 'application/json;odata=verbose'
    site_auth_header = {'Authorization':site_auth_token,'accept': site_accept, 'content-type': site_accept} 

    #Grab the List of Items
    def getListsReturn(self):
        #Building the list API Call
        site_list_api = self.site_api + '/web/lists'
        lists_return = None
        lists_api_return = get(
            site_list_api,
            headers = self.site_auth_header   
        )
        #If the Return was successfull
        if lists_api_return.status_code == 200:    
            lists_return = lists_api_return.json()
            lists_return = lists_return['d']['results']
            #Check if the Return has items
            if len(lists_return) > 0:
                return lists_return
            else:
                lists_return = {'No Results'}
        else:
            lists_return = {'No Results'}
        return lists_return

    def getListItems(self, listName):
        #Building the List Items API Call
        site_items_api = self.site_api + "/web/lists/GetByTitle('"+ listName + "')/items?$top=1000"
        items_return = None
        items_api_return = get(
            site_items_api,
            headers= self.site_auth_header
        )
        if items_api_return.status_code == 200:
            items_return = items_api_return.json()
            items_return = items_return['d']['results']
            #Check if the Return has items
            if len(items_return) > 0:
                return items_return
            else:
                items_return = {'No Results'}
        else:
            items_return = {'No Results'}
        return items_return

    def makeAPICall(self,apiuri):
        api_return = None
        api_return_call = get(
            apiuri,
            headers=self.site_auth_header
        )
        if api_return_call.status_code == 200:
            #api_return = api_return_call.json()
            return api_return





