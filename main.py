import random
import requests
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register

# 定义两个图片链接
image_urls = [
    "https://uapis.cn/api/imgapi/acg/pc.php",
    "https://uapis.cn/api/imgapi/acg/mb.php"
]

@register("random_wallpaper", "Your Name", "随机发送一张壁纸", "1.0.0", "repo url")
class RandomWallpaperPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    # 注册指令的装饰器。指令名为 random_wallpaper。注册成功后，发送 /随机壁纸 就会触发这个指令
    @filter.command("随机壁纸")
    async def random_wallpaper(self, event: AstrMessageEvent):
        '''随机发送一张壁纸'''
        # 随机选择一个图片链接
        selected_url = random.choice(image_urls)
        
        # 下载图片
        try:
            response = requests.get(selected_url, stream=True, timeout=10)
            response.raise_for_status()  # 检查请求是否成功
            image_data = response.content
            # 发送图片
            yield event.image_result(image_data)
        except Exception as e:
            # 如果下载失败，发送错误消息
            yield event.plain_result(f"无法获取壁纸，错误信息：{str(e)}")
