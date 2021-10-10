from requests_html import HTMLSession
from requests_html import requests
from packages import api
from packages.translate import translate
import regex

def google_completion(string) -> list:
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "None",
        "Host": "www.google.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Referer": "https://www.google.com/",
        "Alt-Used": "www.google.com",
        "Connection": "keep-alive",
    }

    r = requests.get(f"https://www.google.com/complete/search?q={string}&cp=6&client=gws-wiz&xssi=t&gs_ri=gws-wiz&hl=pt-PT").text
    r = r.replace("\\u003c", "<").replace("\\u003e", ">").replace("\/", "/")
    rs = regex.findall(r"(?<=\<b>)(.*?)(?=\<\/b>)", r)
    rs = [ string+x for x in rs]
    return rs

def google_search(search:str):
    return api.search(search)

def synonms(search):
    session = HTMLSession()
    r = session.get(f"https://www.sinonimos.com.br/{search}/");     session.close()
    sins = "\n\n".join([ x.text for x in r.html.find(".s-wrapper")])
    return sins

def dicio(search) -> list:
    session = HTMLSession()
    r = session.get(f"https://www.dicio.com.br/{search}/");     session.close()

    data = r.html.find(".significado.textonovo")[0].text
    others = r.html.find(".wrap-section")
    print(others)
    sinos = others[0].text
    defin = others[1].text
    info = others[2].text
    rimas = others[1].text
    return f"{data}\n\n{sinos}\n{defin}\n\n{info}\n{rimas}"


def rimas(search) -> list:
    session = HTMLSession()
    r = session.get(f"https://www.dicio.com.br/disposicao/{search}/");     session.close()
    r.html.find(".tit-other")[1].text
    return r.html.find(".tit-other").text

#TODO
def image_search(search:str):
    return
    session = HTMLSession()
    headers = {
        "Host": "www.google.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive",
    }

    html = session.get('https://www.google.com/search?q=gooo&tbm=isch&ictx=1&tbs=rimg:CW-V3oiJ6K0WIghvld6IieitFioSCW-V3oiJ6K0WEeLH10uLm6-W&client=firefox-b-d&hl=pt-PT&sa=X&ved=2ahUKEwiz_v_czfrxAhWSo5UCHanLBewQiRx6BAgAEAQ&biw=1588&bih=384', headers=headers).html
    hrefs = html.find(".wXeWr.islib.nfEiy")
