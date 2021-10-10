import discord, json, socket, os
import socket as socketlib
from socket import socket as new_socket
http = b"""HTTP/1.1 200 OK
Date: Sun, 10 Oct 2010 23:26:07 GMT
Server: Apache/2.2.8 (Ubuntu) mod_ssl/2.2.8 OpenSSL/0.9.8g
Last-Modified: Sun, 26 Sep 2010 22:04:35 GMT
ETag: "45b6-834-49130cc1182c0"
Accept-Ranges: bytes
Content-Length: 20
Connection: close
Content-Type: text/html

<h1>ONLINE PORR</h1>"""

def http_server():
  PORT = 80
  HOST = ""

  with new_socket(socketlib.AF_INET, socketlib.SOCK_STREAM) as s:
      s.setsockopt(socketlib.SOL_SOCKET, socketlib.SO_REUSEADDR, 1)
      s.bind((HOST,PORT))
      s.listen()
      
      while (True):
        conn, addr = s.accept()
        print(f"Connected By {addr}")
        conn.recv(1024, 0)
        conn.sendall(http)
        conn.close()

def load_data(path):
    if not path.endswith('.json'):
        path = f"{path}.json"

    with open(f'data/{path}','r') as f:
        data = json.load(f)
        return data

def save_data(path, data):
    if not path.endswith('.json'):
        path = f"{path}.json"

    with open(f'data/{path}','w') as f:
        json.dump(data,f,indent=4)

def get_prefix(client, msg):
    server_id = msg.guild.id
    default_prefix = "."

    config = load_data('config')
    servers = config['servers']
    
    for server in servers:
        if server['id'] == server_id:
            prefix = server['prefix']
            return prefix
    
    return default_prefix

def set_prefix(server_id:int, prefix:str):
    config = load_data('config')

    for server in config['servers']:
        if server['id'] == server_id:
            server['prefix'] = prefix
            save_data('config',config)
            return True
          
    config['servers'].append({'id':server_id,"prefix":prefix})
    save_data('config',config)


async def execute_async_functions(msg, args:list, *defs, correct:str=None):
    args_len = args.__len__()
    defs_len = defs.__len__()
    print(args)

    try:
        if args_len == 1:
            await defs[0](args[0])
    
        if args_len == 2:
            await defs[1](args[0], args[1])
        
        if args_len >= 3:
            await defs[2](args[0], args[1], args[2])
    except:
        if correct:
            await msg.send(f"{correct}")
