# 逃离办公室 · Escape the Office

> 周四下午三点半，老板不在。17:30 之前，溜出这栋楼。

一个**现实搞笑风的打工人文字肉鸽**，打包成 Agent Skill：装进 Claude Code、Codex 或任何能读 `SKILL.md` 的 Agent，它就会变成你的游戏主持人——讲故事、给选项、公开掷 d20、记血条和警觉度，还会记住你跨局解锁的天赋和结局。

一局大约 10 分钟，正好够一个老板不在的下午。

![道具图标](docs/items.png)

## 玩法一览

- **目标**：15:30 开局，每个行动 15 分钟，共 8 回合，17:30 前走出大楼。
- **体力 ❤️❤️❤️**：被抓现行扣 1，归零就被押回工位写周报。
- **警觉 0/10**：失败会涨，满了 HR 全楼搜捕，所有难度 +3。
- **判定**：d20（系统真随机，结果公开）+ 道具加值 ≥ 难度（8 / 12 / 16）。掷出 20 白捡道具，掷出 1 附赠社死事件。
- **地图**：工位区 → 茶水间 → 电梯或楼梯间 → 大堂 / 地下车库 / 天台。
- **18 件像素道具**：工牌、半杯冰奶茶、螺蛳粉、带薪如厕卷纸、老板同款保温杯……还有甩不掉的诅咒道具「会议邀请」。
- **组合技**：外卖头盔 + 螺蛳粉 = 大堂自动放行；文件夹 + 老板同款保温杯 = “老板让我送文件”。
- **8 个结局**：好结局、隐藏结局（天台日落、老板的专车、外勤）、一个秘密结局，和三种坏结局。
- **肉鸽成长**：每局赚摸鱼点，解锁「老油条」「卡点大师」「隐身术」等永久天赋。

NPC：HR 王姐（职业规划想清楚了吗）、话痨小李、爱下象棋的保安老周、谁碰谁卡纸的前台打印机。

## 安装

需要 Python 3（只用标准库）。

**Claude Code（插件市场）**
```
/plugin marketplace add supersuperKK/escape-the-office
/plugin install escape-the-office@escape-the-office
```

**手动安装（Claude Code / Codex / 其他支持 Skills 的 Agent）**
```bash
git clone https://github.com/supersuperKK/escape-the-office.git
# Claude Code
cp -r escape-the-office/skills/escape-the-office ~/.claude/skills/
# Codex
cp -r escape-the-office/skills/escape-the-office ~/.codex/skills/
```
其他 Agent：把 `skills/escape-the-office/` 放进它读取 skills 的目录，或者直接让它读 `SKILL.md`。

然后对你的 Agent 说：**“来一局逃离办公室”**。

## 存档

默认在 `~/.escape-the-office/`（`run.json` 当前局，`save.json` 摸鱼点、天赋、结局图鉴）。想换位置就设环境变量 `ESCAPE_OFFICE_HOME`。

## 目录

```
skills/escape-the-office/
├── SKILL.md              主持手册（Agent 读这个）
├── references/rules.md   完整规则与结局条件
├── data/items.json       道具、品质、加值、组合技
├── data/events.json      各区随机事件、社死事件、结局文案
├── scripts/game.py       掷骰、状态、掉落、结算、天赋商店
└── assets/icons/         16×16 像素道具图标（sweetie16 调色板）
tools/build_icons.py      图标源文件（改图标改这里，pip install pillow）
```

## 加点料

欢迎 PR：新事件写进 `data/events.json`，新道具写进 `data/items.json` 并在 `tools/build_icons.py` 里画一枚 16×16 图标。题材保持“现实搞笑”，别写真实公司和真实同事。

## 作者

- 创意与产品：KK
- 设计与开发：Hark

图标标签字体：[Zpix](https://github.com/SolidZORO/zpix-pixel-font)。灵感参考：[准点下班，别被发现](https://github.com/Ryan-fm/clockout-unseen)、[D.O.R.K.](https://github.com/GeoxT/DORK)。

MIT License
