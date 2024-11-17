from httpx import AsyncClient
from openai import AsyncOpenAI
from nonebot.plugin import PluginMetadata
from nonebot.internal.adapter import Message
from nonebot.exception import MatcherException
from nonebot import on_command, get_plugin_config
from nonebot.params import CommandArg, ArgPlainText

from .config import Config


plugin_config = get_plugin_config(Config)


__plugin_meta__ = PluginMetadata(
    name="恩情课文",
    description="一句话生成恩情课文",
    usage="恩情课文 <主题>",
    type="application",
    homepage="https://github.com/zhaomaoniu/nonebot-plugin-kindness-lesson",
    supported_adapters=None,
    config=Config,
)


client = AsyncOpenAI(
    api_key=plugin_config.kindness_lesson_api_key,
    base_url=plugin_config.kindness_lesson_base_url,
    http_client=AsyncClient(proxy=plugin_config.kindness_lesson_proxy),
)

prompt = """按照给定主题改写下面的故事，只替换地点和人物，但保留故事文本。

以下是改写故事时的一些注意事项：

1. **保留故事结构和关键情节**：
   - 尽量保持原故事的情节结构不变，例如开头的访问情节、与人物的交流、故事中的小冲突或事件、结尾的反思等。即使需要调整细节，仍应保留故事的核心事件和递进关系。

2. **替换人物和地点**：
   - 根据需要替换成符合改写主题的地点和人物，同时确保新人物的身份、个性与故事中表现出来的特点相符。
   
3. **调整细节以符合新主题**：
   - 对事件中的具体细节做适当修改，使其符合新主题的背景。例如，若原情节涉及军事背景，而新主题是和平活动，则可将“击落卫星”改为“展示科学实验”或“提出新观点”，以保持符合主题的情节逻辑。

4. **保持对话的情感基调**：
   - 对话中的用词应符合人物身份，保持亲切、敬意、激励等情感。也可以根据新人物的特点调整语言风格，比如将语气调整得更加严谨、亲切或鼓舞人心，以适应新角色。

5. **反思部分的处理**：
   - 原文的反思部分具有深刻的教育意义，可以保留故事结尾处人物对事件的反思，适当调整内容，使其符合新主题的价值观或道德内涵。例如，可以让人物反思在行动中有无“考虑全面”或“做得足够妥当”。

6. **用词的适当修改**：
   - 保持原文的语言风格，避免过于现代或不合时宜的表达。同时，可以根据新主题加入专业词汇或情境词汇，使改写后的故事在内容上更具连贯性。

7. **保持叙事的亲切感**：
   - 原故事传递了一种尊敬和崇敬的情感。改写时应保留这种亲切感，尤其是对于长辈或领导人物的描写，使故事具有温情或激励的效果。


主题：{theme}

从中国访问回来金正日爷爷全然不顾身体的疲惫，连夜找我们几个小标兵商量儿童日的安排。谈得晚了，便送我们出门，要司机送我们回家。在去大门口的路上，我们说：“金爷爷，您回去休息吧。您刚从中国回来。” 

金爷爷摇摇头，“不碍事，你们知道现在国际上有很多人把社会主义当作敌人，不断给我们制造麻烦，你们是祖国的未来，你们的事情便是国家的事情，是头等大事。”我们都激动了，眼里噙着泪花。多好的金爷爷呀。 

金爷爷抬头看看天空说：“如果世界真像这天空这么安静就好了，但是就有一些国家，像美国，要搞乱这个世界，他们是罪人。” 

说着，金爷爷弯下腰，从花池里捡出一颗石子，然后看着天空说：“该死的美国佬。” 

说着他把石子奋力向上一掷。很快就见空中一颗卫星突然爆发出耀眼的强光，然后就坠落下来。“这是美国的间谍卫星，他们一直在平壤上空盘旋，侵犯我们的主权，我已经忍了很久了。”金爷爷愤愤地说。小朋友们都鼓起掌来，为祖国有这样的领导人感到自豪。 

一会金爷爷叫来秘书问：“那个卫星落到什么地方了？”“好像是龙川一带。”秘书说。 

金爷爷一怔，说：“赶紧派人去查，看有什么问题没有。”之后爷爷送我们到大门口， 一直挥手到看不见我们。 

第四天我们听说龙川那边出事了，我们很紧张。而这时金爷爷叫我们过去。 

他依然那么慈祥，让我们坐下说：“战争总是要有牺牲的。为民族独立事业牺牲的人是伟大的。”他这时低下头说：“但我必须承认，我当时击落敌人卫星的行为太鲁莽了， 我在这里向全国人们道歉。我将向全国人民说明情况。” 

我们顿时热泪盈眶，多好的爷爷呀，他在跟敌人斗争过程中的小失误竟然被他记在心里，还道了歉，我们在将来的学习中一定要向金爷爷学，学他老人家那宽广的胸怀，和不耻下问的精神。"""


matcher = on_command("恩情课文", priority=10, block=True)


@matcher.handle()
async def _(args: Message = CommandArg()):
    if theme := args.extract_plain_text():
        try:
            resp = await client.chat.completions.create(
                messages=[{"role": "user", "content": prompt.format(theme=theme)}],
                model=plugin_config.kindness_lesson_model,
            )
            await matcher.finish(resp.choices[0].message.content)
        except MatcherException:
            raise
        except Exception as e:
            await matcher.finish(f"生成恩情课文时出现错误：{e}")


@matcher.got(
    "theme",
    prompt="请输入主题！完整的句子或关键词皆可\n示例：\n	桐谷和人用超越系统限制的一击击落茅场晶彦\n	Python爷爷",
)
async def got_theme(theme: str = ArgPlainText()):
    try:
        resp = await client.chat.completions.create(
            messages=[{"role": "user", "content": prompt.format(theme=theme)}],
            model=plugin_config.kindness_lesson_model,
        )
        await matcher.finish(resp.choices[0].message.content)
    except MatcherException:
        raise
    except Exception as e:
        await matcher.finish(f"生成恩情课文时出现错误：{e}")
