from des import DesKey
from POE.key import key
def Response(status,msg):
    dict_resp = {
        "status": status,
        "message": msg
    }
    return dict_resp

#still to implement
def authenticate_client(data):
    if (data['username'] == "username" and data['password'] == 'password'):
        return True
    else :
        return False

#function to decode the inputs
def decode(data_dict):
    for x in data_dict:
        data_dict[x] = bytes(data_dict[x],'utf-8')
        data_dict[x] = key.decrypt(data_dict[x],padding = True)
        data_dict[x] = data_dict[x].decode('utf-8')
    return data_dict

