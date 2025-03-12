import random
import aiohttp
from astrbot import Bot

bot = Bot()
logger = bot.logger

WALLPAPER_APIS = [
    "https://uapis.cn/api/imgapi/acg/pc.php",
    "https://uapis.cn/api/imgapi/acg/mb.php"
]

@bot.register_hook("message")
async def handle_wallpaper_request(ctx):
    # 匹配指令关键词
    if ctx.command.lower() not in ["随机壁纸", "wallpaper"]:
        return
    
    try:
        # 随机选择API接口
        selected_api = random.choice(WALLPAPER_APIS)
        
        # 异步获取图片
        async with aiohttp.ClientSession() as session:
            async with session.get(selected_api, timeout=10) as response:
                if response.status == 200:
                    image_url = str(response.url)
                    logger.info(f"成功获取壁纸: {image_url}")
                    await ctx.reply(f"[图片]{image_url}")
                else:
                    await ctx.reply("🚧 图片服务暂时不可用，请稍后重试")
                    logger.warning(f"API异常响应: HTTP {response.status}")
                    
    except aiohttp.ClientError as e:
        await ctx.reply("⚠️ 网络连接异常，请检查网络后重试")
        logger.error(f"网络请求失败: {str(e)}")
    except Exception as e:
        await ctx.reply("🔧 服务暂时出错了，请联系管理员")
        logger.critical(f"未处理异常: {str(e)}", exc_info=True)

# 插件元数据
__plugin_name__ = "随机壁纸"
__plugin_version__ = "1.1.0"
__plugin_description__ = "通过随机API获取ACG风格壁纸"
__plugin_requirements__ = ["aiohttp>=3.8.0"]
