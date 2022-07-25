import json
import easyquotation


quotation = easyquotation.use('jsl')
# https://www.jisilu.cn/data/etf/#index
res = quotation.etfindex(
    index_id="", min_volume=0, max_discount=None, min_discount=None
)

# print(json.loads(res))

for k, v in res.items():
    print(k, v, "\n")
