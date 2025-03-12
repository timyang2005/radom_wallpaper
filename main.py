from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
import requests
import random

@register("random_wallpaper", "Your Name", "随机壁纸插件", "1.0.0", "repo url")
class RandomWallpaperPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("随机壁纸")
    async def random_wallpaper(self, event: AstrMessageEvent):
        try:
            # 定义两个图片链接
            image_urls = [
                "https://uapis.cn/api/imgapi/acg/pc.php",
                "https://uapis.cn/api/imgapi/acg/mb.php"
            ]
            # 随机选择一个链接
            selected_url = random.choice(image_urls)

            # 发送请求获取图片
            response = requests.get(selected_url, timeout=10)
            response.raise_for_status()  # 检查请求是否成功

            # 获取图片的 URL
            image_url = response.url if hasattr(response, 'url') else selected_url

            # 发送图片给用户
            yield event.image_result(image_url)

        except requests.exceptions.RequestException as e:
            # 处理请求异常
            error_message = f"获取壁纸失败，可能是网络问题或链接无效。请稍后再试。错误信息：{str(e)}"
            yield event.plain_result(error_message)
        except Exception as e:
            # 处理其他异常
            error_message = f"获取壁纸时发生错误：{str(e)}"
            yield event.plain_result(error_message)
