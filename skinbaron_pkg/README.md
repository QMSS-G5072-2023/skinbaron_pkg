# skinbaron_pkg

A package for getting CSGO market data and perform analysis on the skinbaron website through its API

## Installation

```bash
$ pip install skinbaron_pkg
```

## Usage

```bash
token = 'apikey'
appID = 'appID'
```

### fetch data using the functionalities in the SkinBaronAPI class:
```bash
api = SkinBaronAPI(api_key = token, app_id = appID)
pricelist = api.get_price_list()
newitems = api.newest_items(size=100) # size max limit 100
bestdeals = api.best_deals(size=100) # size max limit 100
```

### Parse the JSON data into panda dataframe using the functionalities in the DataProcessor class
```bash
pricelist_df = DataProcessor.json_to_dataframe(pricelist)
newitems_df = DataProcessor.json_to_dataframe(newitems)
bestdeals_df = DataProcessor.json_to_dataframe(bestdeals)
```

### cutomize items search about the CSGO market with more params like how many stickers, exteriorName and so on for both 100 new items listed and top 100 best deals using the functionalities in the ItemFilter calss
```bash
item_filter = ItemFilter(newitems_df, bestdeals_df)
filtered_items = item_filter.filter_items() # output more market info without filter anything
filtered_items = item_filter.filter_items(itemName = 'M249 | Humidor', 
                                          rarityName= 'Mil-Spec Grade', 
                                    exteriorName= 'Battle-Scarred', sticker_count= 4) # output market info with filter
```

### improve GetNewestSales30Days endpoint with more structured data and generates a report, enable buyer to customize more when searching such as exteriorname, price using the Report_generator class
this also enables vague search: itemName do not need to be detailed in this case
first use regex to further improve the newestsales_df parsed from newestsales using GetNewestSales30Days endpoint, seperate item details so that it matches with other dataset
and then find items with its historical price and its current lowest market listing price and generates a report, this is called inside newestsales_df_pipeline so that it supports vague search and so on
the final function(newestsales_df_pipeline) that user should call which generates a report with a structured dataset
```bash
report_generator = Report_generator(api_key = token, app_id = appID)
merged_df = report_generator.newestsales_df_pipeline(SkinBaronAPI, DataProcessor.json_to_dataframe, report_generator.cheapest,
                                        report_generator.separate_item_and_condition, token,appID, '★ Butterfly Knife | Gamma Doppler', False,
                                        False)

#example with vague search, generates all results containing keyword butterfly
merged_df_vague = report_generator.newestsales_df_pipeline(SkinBaronAPI, DataProcessor.json_to_dataframe, report_generator.cheapest,
                                        report_generator.separate_item_and_condition, token,appID, '★ Butterfly', False,
                                        False)
```

### provide more structured data that shows the price trend based on the buyer’s input search on newestsales_df_pipeline, also generates line plot for better visualization using the MarketTrends class
```bash
market_price_trend = MarketTrends.price_trend(merged_df)
```

### predict products future prices based on data from (price_trend) based on buyer input search. this function only predicts item price 7 days after today’s date since csgo market restriction on selling latest purchased products only after 7 days
```bash
market_price_prediction = PricePrediction.price_prediction(market_price_trend)
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`skinbaron_pkg` was created by Qingxuan Guo. It is licensed under the terms of the MIT license.

## Credits

`skinbaron_pkg` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
