import requests
from typing import Union, Dict

class Zlibrary:

    def __init__(self, email: str = None, password: str = None, remix_userid: Union[int, str] = None, remix_userkey: str = None):
        self.__email: str
        self.__name: str
        self.__kindle_email: str
        self.__remix_userid: Union[int, str]
        self.__remix_userkey: str
        self.__domain = "1lib.sk"
        self.__logged = False

        self.__headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        }
        self.__cookies = {
            "siteLanguageV2": "en",
        }

        if email is not None and password is not None:
            self.login(email, password)
        elif remix_userid is not None and remix_userkey is not None:
            self.loginWithToken(remix_userid, remix_userkey)

    def __setValues(self, response) -> Dict[str, str]:
        if not response["success"]:
            return response
        self.__email = response["user"]["email"]
        self.__name = response["user"]["name"]
        self.__kindle_email = response["user"]["kindle_email"]
        self.__remix_userid = str(response["user"]["id"])
        self.__remix_userkey = response["user"]["remix_userkey"]
        self.__cookies["remix_userid"] = self.__remix_userid
        self.__cookies["remix_userkey"] = self.__remix_userkey
        self.__logged = True
        return response

    def __login(self, email, password) -> Dict[str, str]:
        return self.__setValues(self.__makePostRequest('/eapi/user/login', data={
            "email": email,
            "password": password,
        }, override=True))

    def __checkIDandKey(self, remix_userid, remix_userkey) -> Dict[str, str]:
        return self.__setValues(self.__makeGetRequest('/eapi/user/profile', cookies={
            'siteLanguageV2': 'en',
            'remix_userid': str(remix_userid),
            'remix_userkey': remix_userkey,
        },))

    def login(self, email: str, password: str) -> Dict[str, str]:
        return self.__login(email, password)

    def loginWithToken(self, remix_userid: Union[int, str], remix_userkey: str) -> Dict[str, str]:
        return self.__checkIDandKey(remix_userid, remix_userkey)

    def __makePostRequest(self, url: str, data: dict = {}, override=False) -> Dict[str, str]:
        if not self.__logged and override is False:
            print("Not logged in")
            return
        response = requests.post(
            "https://" + self.__domain + url,
            data=data,
            cookies=self.__cookies,
            headers=self.__headers,
        ).json()
        if not response["success"]:
            print(response["error"])
        return response

    def __makeGetRequest(self, url: str, params: dict = {}, cookies=None) -> Dict[str, str]:
        if not self.__logged and cookies is None:
            print("Not logged in")
            return
        response = requests.get(
            "https://" + self.__domain + url,
            params=params,
            cookies=self.__cookies if cookies is None else cookies,
            headers=self.__headers,
        ).json()
        if not response["success"]:
            print(response["error"])
        return response

    def getProfile(self) -> Dict[str, str]:
        return self.__makeGetRequest('/eapi/user/profile')

    def getMostPopular(self, switch_language: str = None) -> Dict[str, str]:
        if switch_language is not None:
            return self.__makeGetRequest('/eapi/book/most-popular', {"switch-language": switch_language})
        return self.__makeGetRequest('/eapi/book/most-popular')

    def getRecently(self) -> Dict[str, str]:
        return self.__makeGetRequest('/eapi/book/recently')

    def getUserRecommended(self) -> Dict[str, str]:
        return self.__makeGetRequest('/eapi/user/book/recommended')

    def deleteUserBook(self, bookid: Union[int, str]) -> Dict[str, str]:
        return self.__makeGetRequest(f'/eapi/user/book/{bookid}/delete')

    def unsaveUserBook(self, bookid: Union[int, str]) -> Dict[str, str]:
        return self.__makeGetRequest(f'/eapi/user/book/{bookid}/unsave')

    def getBookForamt(self, bookid: Union[int, str], hashid: str) -> Dict[str, str]:
        return self.__makeGetRequest(f'/eapi/book/{bookid}/{hashid}/formats')

    def getDonations(self) -> Dict[str, str]:
        return self.__makeGetRequest('/eapi/user/donations')

    def getUserDownloaded(self, order: str = None, page: int = None, limit: int = None) -> Dict[str, str]:
        '''
        order takes one of the values\n
        ["year",...]
        '''
        params = {k: v for k, v in {"order": order, "page": page,
                                    "limit": limit}.items() if v is not None}
        return self.__makeGetRequest('/eapi/user/book/downloaded', params)

    def getExtensions(self) -> Dict[str, str]:
        return self.__makeGetRequest('/eapi/info/extensions')

    def getDomains(self) -> Dict[str, str]:
        return self.__makeGetRequest('/eapi/info/domains')

    def getLanguages(self) -> Dict[str, str]:
        return self.__makeGetRequest('/eapi/info/languages')

    def getPlans(self, switch_language: str = None) -> Dict[str, str]:
        if switch_language is not None:
            return self.__makeGetRequest('/eapi/info/plans', {"switch-language": switch_language})
        return self.__makeGetRequest('/eapi/info/plans')

    def getUserSaved(self, order: str = None, page: int = None, limit: int = None) -> Dict[str, str]:
        '''
        order takes one of the values\n
        ["year",...]
        '''
        params = {k: v for k, v in {"order": order, "page": page,
                                    "limit": limit}.items() if v is not None}
        return self.__makeGetRequest('/eapi/user/book/saved', params)

    def getInfo(self, switch_language: str = None) -> Dict[str, str]:
        if switch_language is not None:
            return self.__makeGetRequest('/eapi/info', {"switch-language": switch_language})
        return self.__makeGetRequest('/eapi/info')

    def hideBanner(self) -> Dict[str, str]:
        return self.__makeGetRequest('/eapi/user/hide-banner')

    def recoverPassword(self, email: str) -> Dict[str, str]:
        return self.__makePostRequest('/eapi/user/password-recovery', {"email": email}, override=True)

    def makeRegistration(self, email: str, password: str, name: str) -> Dict[str, str]:
        return self.__makePostRequest('/eapi/user/registration', {"email": email, "password": password, "name": name}, override=True)

    def resendConfirmation(self) -> Dict[str, str]:
        return self.__makePostRequest('/eapi/user/email/confirmation/resend')

    def saveBook(self, bookid: Union[int, str]) -> Dict[str, str]:
        return self.__makeGetRequest(f'/eapi/user/book/{bookid}/save')

    def sendTo(self, bookid: Union[int, str], hashid: str, totype: str) -> Dict[str, str]:
        return self.__makeGetRequest(f'/eapi/book/{bookid}/{hashid}/send-to-{totype}')

    def getBookInfo(self, bookid: Union[int, str], hashid: str, switch_language: str = None) -> Dict[str, str]:
        if switch_language is not None:
            return self.__makeGetRequest(f'/eapi/book/{bookid}/{hashid}', {"switch-language": switch_language})
        return self.__makeGetRequest(f'/eapi/book/{bookid}/{hashid}')

    def getSimilar(self, bookid: Union[int, str], hashid: str) -> Dict[str, str]:
        return self.__makeGetRequest(f'/eapi/book/{bookid}/{hashid}/similar')

    def makeTokenSigin(self, name: str, id_token: str) -> Dict[str, str]:
        return self.__makePostRequest('/eapi/user/token-sign-in', {"name": name, "id_token": id_token}, override=True)

    def updateInfo(self, email: str = None, password: str = None, name: str = None, kindle_email: str = None) -> Dict[str, str]:
        return self.__makePostRequest('/eapi/user/update',
                                      {k: v for k, v in {"email": email, "password": password,
                                                         "name": name, "kindle_email": kindle_email}.items() if v is not None})

    def search(self, message: str = None, yearFrom: int = None, yearTo: int = None, languages: str = None, extensions: str = None, order: str = None, page: int = None, limit: int = None) -> Dict[str, str]:
        return self.__makePostRequest('/eapi/book/search',
                                      {k: v for k, v in {"message": message, "yearFrom": yearFrom,
                                                         "yearTo": yearTo, "languages": languages,
                                                         "extensions": extensions, "order": order,
                                                         "page": page, "limit": limit,
                                                         }.items() if v is not None})

    def __getImageData(self, url: str) -> requests.Response.content:
        res = requests.get(url, headers=self.__headers)
        if res.status_code == 200:
            return res.content

    def getImage(self, book: Dict[str, str]) -> requests.Response.content:
        return self.__getImageData(book["cover"])

    def __getBookFile(self, bookid: Union[int, str], hashid: str):
        response = self.__makeGetRequest(f"/eapi/book/{bookid}/{hashid}/file")
        filename = response['file']['description']

        try:
            filename += " (" + response["file"]["author"] + ")"
        except:
            pass
        finally:
            filename += "." + response['file']['extension']

        ddl = response["file"]["downloadLink"]
        headers = self.__headers.copy()
        headers['authority'] = ddl.split("/")[2]

        res = requests.get(ddl, headers=headers)
        if res.status_code == 200:
                return filename, res.content

    def downloadBook(self, book: Dict[str, str]):
        return self.__getBookFile(book["id"], book["hash"])


    def isLogin(self) -> bool:
        return self.__logged


from io import BytesIO
from pyrogram.types import InputMediaPhoto, InputMediaDocument, CallbackQuery
from pyrogram import Client
from buttons import getButtons
from os import remove

def getZlibBooks(Z: Zlibrary, search: str):
    resp = Z.search(search)
    if not resp["success"]:
        return False, resp["error"]
    return True, resp["books"]

def getZlibText(books, choose=0, final=False):
    txt =  f'**{books[choose]["title"]}**\n\n__Author: {books[choose]["author"]}\nYear: {books[choose]["year"]}\nVolume: {books[choose]["volume"]}\nEdition: {books[choose]["edition"]}\nLanguage: {books[choose]["language"]}\nPublisher: {books[choose]["publisher"]}\nExtension: {books[choose]["extension"]}\nSize: {books[choose]["filesizeString"]}\npages: {books[choose]["pages"]}\nSeries: {books[choose]["series"]}__' \
    + "\n\n------[Zlibrary]------"
    if not final: txt += f"  [{choose+1}/{len(books)}]"
    return txt

def getImage(Z: Zlibrary, book):
    return BytesIO(Z.getImage(book))

def handleZlib(Z: Zlibrary, app:Client,call:CallbackQuery,books):
        
    # download
        if call.data[0] == "D":
            choose = int(call.data.replace("D",""))
            app.edit_message_text(call.message.chat.id, call.message.id, "__Downloading__")

            filename, Bcontent = Z.downloadBook(books[choose])
            with open(filename, "wb") as file:
                file.write(Bcontent)

            Icont = Z.getImage(books[choose])
            thumbfile = f"{books[choose]['title']}"
            thumbfile = "".join( x for x in thumbfile if (x.isalnum() or x in "_ ")) + ".jpg"
            with open(thumbfile, "wb") as file:
                file.write(Icont)
                
            app.edit_message_text(call.message.chat.id, call.message.id, "__Uploading__")
            app.edit_message_media(call.message.chat.id, call.message.id, InputMediaDocument(filename, thumb=thumbfile, caption=getZlibText(books,choose,True)))
            remove(filename)
            remove(thumbfile)
            return True

        #  next
        app.answer_callback_query(call.id,"dont click anything until it respond...")
        choose = int(call.data) % len(books)
        Icont = Z.getImage(books[choose])
        thumbfile = str(call.message.chat.id) + "_Z.jpg"
        with open(thumbfile, "wb") as file: file.write(Icont)
        app.edit_message_media(call.message.chat.id, call.message.id,
            InputMediaPhoto(thumbfile,getZlibText(books,choose)),
            reply_markup=getButtons(choose))
        remove(thumbfile)
        return False
