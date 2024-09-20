import ujson
from zhenxun.utils.http_utils import AsyncHttpx


async def fetch_data():
    url = 'https://api.bgm.tv/calendar'
    headers = {
        'User-Agent': 'menglyl/qqbot',
        'Accept': 'application/json'
    }

    try:
        data = await AsyncHttpx.get(url, headers=headers)
        data.encoding = 'utf-8'
        return ujson.loads(data.text)
    except Exception as e:
        print(f"获取数据失败: {e}")
        return None


async def get_today(today):
    data = await fetch_data()
    if data is None:
        print("获取数据失败")
        return None

    bgm = data[today]['items']
    out = []
    for item in bgm:
        cn_name = item['name_cn'] if item['name_cn'] else item['name']
        rating = item['rating']['score'] if 'rating' in item and 'score' in item['rating'] else '暂无评分'
        out.append(f"#### {cn_name} &emsp; 评分：{rating}")

    return '\n'.join(out)


async def get_all():

    data = await fetch_data()
    if data is None:
        print("Failed to fetch data")
        return None

    out = []
    for day in range(7):
        bgm = data[day]['items']
        out.append(f"## 周{day+1}新番\n")
        for item in bgm:
            cn_name = item['name_cn'] if item['name_cn'] else item['name']
            rating = item['rating']['score'] if 'rating' in item and 'score' in item['rating'] else '暂无评分'
            out.append(f"#### {cn_name} &emsp; 评分：{rating}")

    return '\n'.join(out)
