top100 = ['apple', 'saudi aramco']
rest100= ['microsoft', 'alphabet', 'amazon', 'tesla', 'berkshire hathaway', 'nvidia', 'meta', 'tsmc', 'tencent', 'unitedhealth', 'visa', 'johnson & johnson', 'samsung', 'jpmorgan chase', 'walmart', 'procter & gamble', 'kweichow moutai', 'nestle', 'exxon mobil', 'bank of america', 'lvmh', 'home depot', 'mastercard', 'roche', 'chevron', 'alibaba', 'coca-cola', 'pfizer', 'abbvie', 'walt disney', 'bhp group', 'icbc', 'asml', 'eli lilly', 'toyota', 'novo nordisk', 'broadcom', 'costco', 'cisco', 'verizon', 'pepsico', 'adobe', 'thermo fisher scientific', 'comcast', 'abbott laboratories', 'reliance industries', 'nike', 'oracle', "l'oreal", 'shell', 'salesforce', 'accenture', 'cm bank', 'danaher', 'wells fargo', 'intel', 'merck', 'novartis', 'catl', 'china construction bank', 'qualcomm', 'astrazeneca', 'united parcel service', 'amd', 'prosus', 'mcdonald', 'tata consultancy services', 'at&t', 'netflix', 'agricultural bank of china', 'union pacific corporation', 'petrochina', 'philip morris', 'texas instruments', 'morgan stanley', 'royal bank of canada', 't-mobile us', 'nextera energy', 'charles schwab', "lowe's companies", 'bristol-myers squibb', 'raytheon technologies', 'hermes', 'linde', 'china mobile', 'medtronic', 's&p global', 'toronto dominion bank', 'ping an insurance', 'bank of china', 'cvs health', 'american express', 'rio tinto', 'hsbc', 'intuit', 'totalenergies', 'meituan', 'amgen']
tickers=['AAPL','2222.SR']
LANGUAGES = ['en']
SOURCES = 'bloomberg'
rest=['MSFT', 'GOOG', 'AMZN', 'TSLA', 'BRK-A', 'NVDA', 'FB', 'TSM','TCEHY', 'UNH', 'V', 'JNJ', '005930.KS', 'JPM', 'WMT', 'PG', '600519.SS', 'NSRGY', 'XOM', 'BAC', 'LVMUY', 'HD', 'MA', 'RHHBF', 'CVX', 'BABA', 'KOF', 'PFE', 'ABBV', 'DIS', 'BHP', '1398.HK', 'ASML', 'LLY', 'TM', 'NVO', 'AVGO', 'COST', 'CSCO', 'VZ', 'PEP', 'ADBE', 'TMO', 'CMCSA', 'ABT', 'RELIANCE.NS', 'NKE', 'ORCL', 'OR.PA', 'SHLX', 'CRM', 'ACN', '3968.HK', 'DHR', 'WFC', 'INTC', 'MRK', 'NVS', '300750.SZ', 'CICHY', 'QCOM', 'AZN', 'UPS', 'AMD', 'PRX.AS', 'MCD', 'TCS.NS', 'T', 'NFLX', 'ACGBY', 'UNP', 'PTR', 'PM', 'TXN', 'MS', 'RY', 'TMUS', 'NEE', 'SCHW', 'LOW', 'BMY', 'RTX', 'HESAF', 'LIN', '0941.HK', 'MDT', 'SPGI', 'TD', 'PNGAY', 'BACHF', 'CVS', 'AXP', 'RIO', 'HSBC', 'INTU', 'TTE', 'MPNGF', 'AMGN']
map1={'apple': 'AAPL',
 'microsoft': 'MSFT',
 'amazon': 'AMZN',
 'tesla': 'TSLA',
 'nvidia': 'NVDA',
 'visa': 'V',
 'unitedhealth': 'UNH',
 'walmart': 'WMT',
 'mastercard': 'MA',
 'roche': 'RHHBF',
 'alibaba': 'BABA',
 'pfizer': 'PFE',
 'asml': 'ASML',
 'toyota': 'TM',
 'coca-cola': 'KOF',
 'cisco': 'CSCO',
 'broadcom': 'AVGO',
 'nike': 'NKE',
 'accenture': 'ACN',
 'adobe': 'ADBE',
 'chevron': 'CVX',
 'pepsico': 'PEP',
 'netflix': 'NFLX',
 'abbvie': 'ABBV',
 'oracle': 'ORCL',
 'comcast': 'CMCSA',
 'verizon': 'VZ',
 'intel': 'INTC',
 'danaher': 'DHR',
 'qualcomm': 'QCOM',
 'novartis': 'NVS',
 'shell': 'SHLX',
 'astrazeneca': 'AZN',
 'linde': 'LIN',
 'intuit': 'INTU',
 'petrochina': 'PTR',
 'medtronic': 'MDT',
 'hsbc': 'HSBC',
 'amgen': 'AMGN',
 'saudi aramco': '2222.SR',
 'alphabet': 'GOOG',
 'berkshire hathaway': 'BRK-A',
 'meta': 'FB',
 'tsmc': 'TSM',
 'tencent': 'TCEHY',
 'johnson & johnson': 'JNJ',
 'samsung': '005930.KS',
 'jpmorgan chase': 'JPM',
 'procter & gamble': 'PG',
 'kweichow moutai': '600519.SS',
 'nestle': 'NSRGY',
 'exxon mobil': 'XOM',
 'bank of america': 'BAC',
 'lvmh': 'LVMUY',
 'home depot': 'HD',
 'walt disney': 'DIS',
 'bhp group': 'BHP',
 'icbc': '1398.HK',
 'eli lilly': 'LLY',
 'novo nordisk': 'NVO',
 'costco': 'COST',
 'thermo fisher scientific': 'TMO',
 'abbott laboratories': 'ABT',
 'reliance industries': 'RELIANCE.NS',
 "l'oreal": 'OR.PA',
 'salesforce': 'CRM',
 'cm bank': '3968.HK',
 'wells fargo': 'WFC',
 'merck': 'MRK',
 'catl': '300750.SZ',
 'china construction bank': 'CICHY',
 'united parcel service': 'UPS',
 'amd': 'AMD',
 'prosus': 'PRX.AS',
 'mcdonald': 'MCD',
 'tata consultancy services': 'TCS.NS',
 'at&t': 'T',
 'agricultural bank of china': 'ACGBY',
 'union pacific corporation': 'UNP',
 'philip morris': 'PM',
 'texas instruments': 'TXN',
 'morgan stanley': 'MS',
 'royal bank of canada': 'RY',
 't-mobile us': 'TMUS',
 'nextera energy': 'NEE',
 'charles schwab': 'SCHW',
 "lowe's companies": 'LOW',
 'bristol-myers squibb': 'BMY',
 'raytheon technologies': 'RTX',
 'hermes': 'HESAF',
 'china mobile': '0941.HK',
 's&p global': 'SPGI',
 'toronto dominion bank': 'TD',
 'ping an insurance': 'PNGAY',
 'bank of china': 'BACHF',
 'cvs health': 'CVS',
 'american express': 'AXP',
 'rio tinto': 'RIO',
 'totalenergies': 'TTE',
 'meituan': 'MPNGF'}
