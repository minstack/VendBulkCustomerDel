import requests

class VendApi:

    __BASE_URL = "https://{0}.vendhq.com/"
    __ENDPOINTS = {
        "cust" : "api/2.0/customers",
        "search" : "api/2.0/search",
        "sales" : "api/2.0/sales"
    }

    __domain = ''
    __headers = {"Authorization" : "", "User-Agent" : "Python 2.7 Vend Support Tool"}

    def __init__(self, prefix, token):
        self.__domain = self.__BASE_URL.format(prefix)
        self.__headers["Authorization"] = "Bearer " + token

    def deleteCustomer(self, id):
        return requests.request("DELETE", "{0}{1}{2}".format(self.__domain, self.__ENDPOINTS['cust'], id), headers=self.__headers).status_code

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

        # gotta check if the url already has params for search
        # no ternary in python?
        if "?" in url:
            cursorParam = "&after={0}"
        else:
            cursorParam = "?after={0}"

        tempDataList = []
        tempJson = response.json()
        version = tempJson['version']['min']

        while version is not None:
            tempDataList.extend(tempJson['data'])

            if tempJson['version']['max'] is None:
                break;

            version = tempJson['version']['max']

            tempJson = request.request("GET", url + cursorParam.format(version), headers = self.__headers).json()


        return tempDataList
