import requests

headers = {
    'Authorization': 'apikey kirillgerasimov:a8baaabc767b040b282288400d4b8a404866c1c2',
}

def riskScoreModels():
    response = requests.get('https://countryrisk.io/api/v1/configuration/riskscoremodels/', headers=headers)
    return response.text

def countries():
    response = requests.get('https://countryrisk.io/api/v1/configuration/countries/', headers=headers)
    return response.text

def riskscores(model):
    response = requests.get('https://countryrisk.io/api/v1/riskscores/'+model, headers=headers)
    return response.text

def riskByCountry(model,cntry):
    response = requests.get('https://countryrisk.io/api/v1/riskscores/'+model+'/'+cntry, headers=headers)
    return response.text

def countryRiskScores(cntry):
    response = requests.get('https://countryrisk.io/api/v1/riskscores/country/'+cntry, headers=headers)
    return response.text


if __name__ == "__main__":
    print(countryRiskScores('ZWE'))