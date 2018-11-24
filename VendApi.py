import requests

class VendApi:

    __BASE_URL = "https://{0}.vendhq.com/"
    __ENDPOINTS = {
        "cust" : "api/2.0/customers",
        "search" : "api/2.0/search",
        "sales" : "api/2.0/sales"
    }

    __domain = ''
    __headers = {"Authorization" : ""}

    def __init__(self, prefix, token):
        self.__domain = self.__BASE_URL.format(prefix)
        self.__headers["Authorization"] = "Bearer " + token


    def getCustomers(self):
        return self.__getRequest__(self.__domain + self.__ENDPOINTS['cust'])

    def getVoidedSales(self):
        return self.__getRequest__(self.__domain + self.__ENDPOINTS['search'] + '?type=sales&status=voided')

    def getLaybySales(self):
        return self.__getRequest__(self.__domain + self.__ENDPOINTS['search'] + '?type=sales&status=layby')

    def __getRequest__(self, url):
        response = requests.request("GET", url, headers = self.__headers)

        if response.status_code != 200:
            return None

        return response.json()['data']
