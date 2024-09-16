import ujson
from zhenxun.utils.http_utils import AsyncHttpx


async def get_today(today):
    url = 'https://api.bgm.tv/calendar'

    headers = {
        'User-Agent': 'menglyl/qqbot',
        'Accept': 'application/json'
    }

    out = []

    data = await AsyncHttpx.get(url, headers=headers)  # 主请求
    data.encoding = 'utf-8'
    data = ujson.loads(data.text)
    bgm = data[today]['items']
    for item in bgm:
        cn_name = item['name_cn'] if item['name_cn'] else item['name']
        rating = item['rating']['score'] if 'rating' in item and 'score' in item['rating'] else '暂无评分'
        out.append(f"#### {cn_name} &emsp; 评分：{rating}")

    return '\n'.join(out)