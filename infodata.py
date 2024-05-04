indicators ={'demand':1775, 'wind':1777, 'solar': 1779, 'spot_price': 600, 'nuclear': 474}
url = "https://api.esios.ree.es/indicators/{}?start_date={}&end_date={}{}"
features = ['demand', 'wind', 'solar', 'spot_price', 'nuclear']
reference_day_esios = "2018-12-31"
reference_hour_esios = "23:00"