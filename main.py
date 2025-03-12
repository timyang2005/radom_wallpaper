from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
import requests

@register("random_wallpaper", "Your Name", "随机壁纸插件", "1.0.0", "repo url")
class RandomWallpaperPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("随机壁纸")
    async def random_wallpaper(self, event: AstrMessageEvent):
        try:
            # 发送请求获取图片
            response = requests.get("https://uapis.cn/api/imgapi/acg/mb.php", timeout=10)
            response.raise_for_status()  # 检查请求是否成功
            image_url = response.url  # 获取图片的 URL

            # 发送图片给用户
            yield event.image_result(image_url)
        except Exception as e:
            # 如果出现异常，发送错误消息给用户
            error_message = f"获取壁纸失败，请稍后再试或检查链接是否有效。错误信息：{str(e)}"
            yield event.plain_result(error_message)
