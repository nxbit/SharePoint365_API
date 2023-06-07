"""      SharePoint 365 Custom Authenticator                    """
"""         Created By: Kevin.Hewitt@Charter.com                """
"""         Description: class will return the auth             """
"""             authentication header need to make              """
"""             REST SP API calls. The intention of             """
"""             this class is to establish and maintain         """
"""             the authentication header needed to make        """
"""             authenticated SP REST API calls                 """

from requests import post

class sp_api:
    #Sharepoint EndPoints
    ep_sites = 'sites'
    ep_api = '_api'
    #Custom EndPoints
    #Custome EndPoint to a Sharepoint List
    aat_instance = ''
    #Sharepoint Site Info
    sp_url = ''
    sp_siteName = ''
    #OAuth 2.0 TokenSites
    oAuth_token_url = 'https://accounts.accesscontrol.windows.net/'
    oAuth_OAuth2_ep = '/tokens/OAuth/2'
    #OAuth 2.0 Values
    #Update with Tenant, Client ID's and Client Secret
    tenant_id = ''
    client_id = ''
    client_secret = ''
    #Defaults
    resource_id = '00000003-0000-0ff1-ce00-000000000000'
    verf_token = True
    authObj = None
    #OAuth 2.0 Responce Values
    token_type = None
    expires_in = None
    not_before = None
    expires_on = None
    #Set Default Resource
    resource = None
    access_token = None

    #Grab the Compiled ResourceID
    def get_resource(self):
        return self.resource_id+'/'+self.sp_url+'@'+self.tenant_id
    #Grab the Sharepoint Site URL
    def get_site_url(self):
        return 'https://'+self.sp_url+'/'+self.ep_sites+'/'+self.sp_siteName+'/'+self.aat_instance
    #Grab the Sharepoint Site API
    def get_site_api_url(self):
        u = self.get_site_url()
        u = u + '/' + self.ep_api
        return u
    #Grab the oAuth2.0 Token URL
    def get_token_api_url(self):
        return self.oAuth_token_url + '/'+self.tenant_id + '/' + self.oAuth_OAuth2_ep
    #Grab the ClickId Token for oAuth
    def get_clientId_token(self):
        return self.client_id+'@'+self.tenant_id
    #Grab the Auth Responce
    def get_auth_response(self):
        #Create a Post Request and set it to the auth Obj in the class
        req = post(self.get_token_api_url(),
            headers={'content-type': 'application/x-www-form-urlencoded'},
            data={
                'grant_type': 'client_credentials',
                'client_id': self.get_clientId_token(),
                'client_secret': self.client_secret,
                'resource': self.get_resource(),
            },verify=self.verf_token)
        self.authObj = req
    #During Initilization, get the Request Request Responce
    def __init__(self, spAData) -> None:
        self.tenant_id = spAData['tenant_id']
        self.client_id = spAData['client_id']
        self.client_secret = spAData['client_secret']
        self.sp_siteName = spAData['sp_siteName']
        self.get_auth_response()
        #If the Responce was 'OK' then Set Variables
        if self.authObj.status_code == 200:
            authObjson = self.authObj.json()
            self.token_type = authObjson['token_type']
            self.expires_in = authObjson['expires_in']
            self.not_before = authObjson['not_before']
            self.expires_on = authObjson['expires_on']
            self.resource = authObjson['resource']
            self.access_token = authObjson['access_token']