from matplotlib import pyplot as plt
import json

how_many_countries = 15

### With opening csv file create list of tuples (country, big_mac_index_price) in how_many_countries number given
with open("bic_mac_index_all_countries.json") as f:
    data = json.load(f)
    sorted_bic_mac_index_all_countries = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))

list_of_countries_with_index = [(country, big_mac_index_price) for (country, big_mac_index_price) in sorted_bic_mac_index_all_countries.items()]

### Create data lists for matplotlib bar charts
country_list = []
index_price_list = []
for country, index_price in list_of_countries_with_index[0:how_many_countries]:
    country_list.append(country)
    index_price_list.append((index_price))
country_list.reverse()
index_price_list.reverse()

###Create Bar charts
plt.style.use("fivethirtyeight")
plt.barh(country_list, index_price_list, label="Country")
plt.title(f"Top {how_many_countries} countries Big Mac Index.")
plt.ylabel("Countries")
plt.xlabel("BIC MAC price in USD")
plt.tight_layout()

for index, value in enumerate(index_price_list):
    plt.text(value, index-0.25, str(value))

plt.show()