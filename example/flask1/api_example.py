import requests

res = requests.get("https://www.nbrb.by/api/ExRates/Rates?Periodicity=0&ondate=2026-01-19")


# print(res.text, type(res.text))

data = res.json()
print(type(data))


print(*data, sep="\n")





