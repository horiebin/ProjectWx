from dao.server_config import ServerConfig
from basic import Basic

if __name__ == "__main__":
    sc = ServerConfig()
    accessToken = Basic().get_access_token()
    print(accessToken)
    sc.set_access_token(accessToken)