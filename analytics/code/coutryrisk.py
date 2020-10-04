import requests

headers={'Authorization':' apikey', 'kirillgerasimov':'a8baaabc767b040b282288400d4b8a404866c1c2'}

def get_riskScoreModels(hd):
    r = requests.get('https://countryrisk.io/api/v1/configuration/riskscoremodels/', auth=('kirillgerasimov', 'a8baaabc767b040b282288400d4b8a404866c1c2'))
    return r

if __name__ == "__main__":
    print(get_riskScoreModels(headers))