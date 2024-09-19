from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Match, Args, on_alconna

from zhenxun.configs.utils import PluginExtraData
from zhenxun.utils.message import MessageUtils
from nonebot_plugin_htmlrender import md_to_pic

from datetime import datetime
from .data_source import get_today


__plugin_meta__ = PluginMetadata(
    name="新番",
    description="获取新番信息和评分",
    usage="""
    指令：
        新番 星期X
        新番 周X
        新番 今日/明日
    """.strip(),
    extra=PluginExtraData(
        author="meng-luo",
        version="0.1",
    ).dict(),
)

_matcher = on_alconna(Alconna("新番", Args["text?", str]), priority=5, block=True)

def convert_weekday_to_number(weekday_str):
    weekdays_mapping = {
        "周一": 0, "星期一": 0,
        "周二": 1, "星期二": 1,
        "周三": 2, "星期三": 2,
        "周四": 3, "星期四": 3,
        "周五": 4, "星期五": 4,
        "周六": 5, "星期六": 5,
        "周日": 6, "星期日": 6,
        "今日": datetime.now().weekday(),
        "明日": datetime.now().weekday() + 1
    }
    return weekdays_mapping.get(weekday_str, -1)

async def handle_new_anime(weekday_str):
    day_id = convert_weekday_to_number(weekday_str)
    if day_id == -1:
        await MessageUtils.build_message('请正确输入查询的日期').finish()
        return

    out = await get_today(day_id)
    if out is None:
        await MessageUtils.build_message('查询失败').finish()
        return

    text = f"## {weekday_str}新番的新番有：\n{out}\n> #### 数据来源：bgm.tv"
    pic = await md_to_pic(md=text)
    await MessageUtils.build_message(pic).send()

@_matcher.handle()
async def _(text: Match[str]):
    if text.available:
        weekday_str = text.result
        await handle_new_anime(weekday_str)
    else:
        usage_text = """
## 新番查询
#### 查询番剧的每日放送和评分
#### 使用方法：
##### 新番 星期X（或新番 周X）
###### 数据来源 bgm.tv
"""
        pic = await md_to_pic(md=usage_text)
        await MessageUtils.build_message(pic).send()
