#!/usr/bin/env python3
"""逃离办公室 · 主持人工具（只用标准库）。

所有随机都来自 secrets（系统真随机），结果会打印出来，主持人必须原样公开给玩家。
存档默认在 ~/.escape-the-office/，可用环境变量 ESCAPE_OFFICE_HOME 改位置。

常用：
  game.py new                      开新局（读取永久天赋）
  game.py status                   当前局 + 永久进度
  game.py roll --dc 12 --mod 2     掷 d20（警觉满 10 自动难度 +3）
  game.py event pantry             从某区抽一个本局没出现过的事件
  game.py loot [--min rare]        掉落一件道具（背包满会提示）
  game.py tick                     时间 +15 分钟、回合 +1，检查 17:30 / 巡逻
  game.py set hp=-1 alert=+2 zone=lobby    改数值（+/- 为增减）
  game.py bag add folder | bag rm milktea
  game.py end good_front           结算结局，发摸鱼点，写图鉴
  game.py shop | buy slacker       看/买永久天赋
  game.py pause | resume
"""
import argparse, json, os, secrets, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
HOME = os.environ.get("ESCAPE_OFFICE_HOME", os.path.expanduser("~/.escape-the-office"))
RUN = os.path.join(HOME, "run.json")
SAVE = os.path.join(HOME, "save.json")

TALENTS = {
    "toilet": {"name": "带薪如厕", "cost": 3, "effect": "每局 1 次免罚躲藏"},
    "slacker": {"name": "老油条", "cost": 4, "effect": "说谎/演技判定 +2"},
    "early": {"name": "卡点大师", "cost": 5, "effect": "开局时钟 15:15（多一回合）"},
    "chessmate": {"name": "象棋搭子", "cost": 5, "effect": "老周好感拉满，大堂放行难度 -4"},
    "ghost": {"name": "隐身术", "cost": 6, "effect": "本局第一次警觉上涨无效"},
    "pocket": {"name": "多带一件", "cost": 2, "effect": "下一局开局多带一件随机普通道具（一次性）"},
}
ENDING_BONUS = {"good": 3, "hidden": 5, "secret": 8, "bad": 0}


def load(path, default=None):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return default


def dump(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def out(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def items_db():
    return load(os.path.join(DATA, "items.json"))


def events_db():
    return load(os.path.join(DATA, "events.json"))


def item_name(iid):
    for it in items_db()["items"]:
        if it["id"] == iid:
            return it["name"]
    return iid


def meta():
    return load(SAVE, {"runs": 0, "moyu_points": 0, "talents": [], "consumables": [], "endings_unlocked": [], "history": []})


def need_run():
    r = load(RUN)
    if not r:
        sys.exit("没有进行中的对局，先运行 new")
    return r


def fmt_clock(minutes):
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def d(n):
    return secrets.randbelow(n) + 1


def cmd_new(a):
    m = meta()
    db = items_db()
    start = 15 * 60 + (15 if "early" in m["talents"] else 30)
    bag = list(db["starter"])
    if "pocket" in m.get("consumables", []):
        commons = [i["id"] for i in db["items"] if i["rarity"] == "common"]
        bag.append(commons[secrets.randbelow(len(commons))])
        m["consumables"].remove("pocket")
        dump(SAVE, m)
    run = {
        "run": m["runs"] + 1, "clock": start, "end": 17 * 60 + 30, "round": 1,
        "zone": "workstation", "zones_cleared": [], "hp": 3, "alert": 0, "bag": bag,
        "talents": m["talents"], "used_once": [], "seen_events": [],
        "hr_patrol_round": d(2), "paused": False, "log": [],
    }
    dump(RUN, run)
    show_status(run)


def show_status(r=None):
    r = r or load(RUN)
    m = meta()
    res = {"meta": {"摸鱼点": m["moyu_points"], "天赋": [TALENTS[t]["name"] for t in m["talents"]],
                    "结局图鉴": m["endings_unlocked"], "已玩局数": m["runs"]}}
    if r:
        rounds_total = (r["end"] - (15 * 60 + 15 if "early" in r["talents"] else 15 * 60 + 30)) // 15
        res["run"] = {
            "局": r["run"], "时间": fmt_clock(r["clock"]), "回合": f'{r["round"]}/{rounds_total}',
            "区域": events_db()["zones"].get(r["zone"], {}).get("name", r["zone"]),
            "体力": "❤️" * r["hp"] + "🖤" * (3 - r["hp"]), "警觉": f'{r["alert"]}/10',
            "背包": [item_name(i) for i in r["bag"]], "HR下次巡逻回合": r["hr_patrol_round"],
            "已过区域": r["zones_cleared"], "暂停": r["paused"],
        }
    out(res)


def cmd_status(a):
    show_status()


def cmd_roll(a):
    r = load(RUN)
    dc = a.dc
    if r and r["alert"] >= 10:
        dc += 3
    raw = d(20)
    total = raw + a.mod
    if raw == 20:
        result = "大成功"
    elif raw == 1:
        result = "大失败"
    else:
        result = "成功" if total >= dc else "失败"
    res = {"d20": raw, "加值": a.mod, "合计": total, "难度": dc, "结果": result}
    if raw == 1:
        f = events_db()["events"]["fumble"]
        res["社死事件"] = f[secrets.randbelow(len(f))]
    if r:
        r["log"].append(f'R{r["round"]} {a.note or ""} d20={raw}+{a.mod}={total} vs {dc} {result}')
        dump(RUN, r)
    out(res)


def cmd_event(a):
    r = need_run()
    pool = [e for e in events_db()["events"].get(a.zone, []) if e["id"] not in r["seen_events"]]
    if not pool:
        pool = events_db()["events"].get(a.zone, [])
    if not pool:
        sys.exit(f"未知区域：{a.zone}")
    e = pool[secrets.randbelow(len(pool))]
    r["seen_events"].append(e["id"])
    dump(RUN, r)
    out(e)


def cmd_loot(a):
    r = need_run()
    db = items_db()
    order = ["common", "rare", "legendary", "cursed"]
    allowed = order[order.index(a.min):] if a.min else order
    weights = {k: v for k, v in db["rarity_weights"].items() if k in allowed}
    roll = secrets.randbelow(sum(weights.values()))
    for rar, w in weights.items():
        if roll < w:
            break
        roll -= w
    pool = [i for i in db["items"] if i["rarity"] == rar and i["id"] not in r["bag"]]
    if not pool:
        out({"掉落": None, "说明": "这个品质的道具你都有了"})
        return
    it = pool[secrets.randbelow(len(pool))]
    full = len(r["bag"]) >= db["bag_limit"]
    if not full or it["rarity"] == "cursed":
        r["bag"].append(it["id"])
        dump(RUN, r)
    out({"掉落": it, "已放入背包": (not full) or it["rarity"] == "cursed",
         "背包满了": full and it["rarity"] != "cursed"})


def cmd_bag(a):
    r = need_run()
    db = items_db()
    ids = {i["id"] for i in db["items"]}
    if a.item not in ids:
        sys.exit(f"未知道具：{a.item}")
    if a.op == "add":
        if len(r["bag"]) >= db["bag_limit"]:
            sys.exit("背包满了（6 格），先丢一件")
        r["bag"].append(a.item)
    else:
        if a.item == "invite":
            sys.exit("会议邀请是诅咒道具，丢不掉")
        if a.item in r["bag"]:
            r["bag"].remove(a.item)
    dump(RUN, r)
    show_status(r)


def cmd_set(a):
    r = need_run()
    for kv in a.pairs:
        k, v = kv.split("=", 1)
        if k in ("hp", "alert"):
            cur = r[k]
            new = cur + int(v) if v[0] in "+-" else int(v)
            if k == "alert" and new > cur and "ghost" in r["talents"] and "ghost" not in r["used_once"]:
                r["used_once"].append("ghost")
                new = cur
            r[k] = max(0, min(3 if k == "hp" else 10, new))
        elif k == "zone":
            if r["zone"] not in r["zones_cleared"] and v != r["zone"]:
                r["zones_cleared"].append(r["zone"])
            r["zone"] = v
        elif k == "use_once":
            r["used_once"].append(v)
        else:
            r[k] = v
    dump(RUN, r)
    warn = []
    if r["hp"] == 0:
        warn.append("体力归零 → 结局 weekly_report")
    if r["alert"] >= 10:
        warn.append("警觉满 10 → HR 全楼搜捕，所有难度 +3；再被抓一次 → 结局 career_talk")
    show_status(r)
    if warn:
        out({"警告": warn})


def cmd_tick(a):
    r = need_run()
    r["clock"] += 15
    r["round"] += 1
    notes = []
    if r["clock"] >= r["end"]:
        notes.append("17:30 到了，还在楼里 → 结局 meeting")
    if r["round"] >= r["hr_patrol_round"]:
        notes.append("HR 王姐巡逻到你附近了，本回合要处理她")
        gap = 1 if r["alert"] >= 6 else 2
        r["hr_patrol_round"] = r["round"] + gap
    if "invite" in r["bag"] and "headphones" not in r["bag"] and r["round"] % 2 == 0:
        notes.append("会议邀请发作：“15 分钟同步一下”，本回合被拖住")
    dump(RUN, r)
    show_status(r)
    if notes:
        out({"提示": notes})


def cmd_end(a):
    r = need_run()
    ev = events_db()
    if a.ending not in ev["endings"]:
        sys.exit("未知结局：" + ", ".join(ev["endings"]))
    e = ev["endings"][a.ending]
    cleared = len(set(r["zones_cleared"]))
    gain = cleared + ENDING_BONUS[e["type"]]
    m = meta()
    m["runs"] += 1
    m["moyu_points"] += gain
    new_unlock = a.ending not in m["endings_unlocked"]
    if new_unlock:
        m["endings_unlocked"].append(a.ending)
    m["history"].append({"run": r["run"], "ending": a.ending, "clock": fmt_clock(r["clock"]), "gain": gain})
    dump(SAVE, m)
    os.replace(RUN, os.path.join(HOME, f"run_{r['run']}_done.json"))
    out({"结局": e, "新解锁": new_unlock, "过区": cleared, "本局摸鱼点": gain,
         "总摸鱼点": m["moyu_points"], "图鉴": f'{len(m["endings_unlocked"])}/{len(ev["endings"])}'})


def cmd_shop(a):
    m = meta()
    out({"摸鱼点": m["moyu_points"], "天赋": [
        {"id": k, **v, "已拥有": k in m["talents"]} for k, v in TALENTS.items()]})


def cmd_buy(a):
    m = meta()
    t = TALENTS.get(a.talent)
    if not t:
        sys.exit("未知天赋")
    if a.talent in m["talents"]:
        sys.exit("已经拥有")
    if m["moyu_points"] < t["cost"]:
        sys.exit(f'摸鱼点不够（需要 {t["cost"]}，有 {m["moyu_points"]}）')
    m["moyu_points"] -= t["cost"]
    if a.talent == "pocket":
        m.setdefault("consumables", []).append("pocket")
    else:
        m["talents"].append(a.talent)
    dump(SAVE, m)
    out({"购买": t["name"], "剩余摸鱼点": m["moyu_points"]})


def cmd_pause(a):
    r = need_run(); r["paused"] = True; dump(RUN, r); show_status(r)


def cmd_resume(a):
    r = need_run(); r["paused"] = False; dump(RUN, r); show_status(r)


def main():
    p = argparse.ArgumentParser(description="逃离办公室 主持工具")
    s = p.add_subparsers(dest="cmd", required=True)
    s.add_parser("new").set_defaults(f=cmd_new)
    s.add_parser("status").set_defaults(f=cmd_status)
    x = s.add_parser("roll"); x.add_argument("--dc", type=int, default=12); x.add_argument("--mod", type=int, default=0); x.add_argument("--note", default=""); x.set_defaults(f=cmd_roll)
    x = s.add_parser("event"); x.add_argument("zone"); x.set_defaults(f=cmd_event)
    x = s.add_parser("loot"); x.add_argument("--min", choices=["common", "rare", "legendary", "cursed"]); x.set_defaults(f=cmd_loot)
    x = s.add_parser("bag"); x.add_argument("op", choices=["add", "rm"]); x.add_argument("item"); x.set_defaults(f=cmd_bag)
    x = s.add_parser("set"); x.add_argument("pairs", nargs="+"); x.set_defaults(f=cmd_set)
    s.add_parser("tick").set_defaults(f=cmd_tick)
    x = s.add_parser("end"); x.add_argument("ending"); x.set_defaults(f=cmd_end)
    s.add_parser("shop").set_defaults(f=cmd_shop)
    x = s.add_parser("buy"); x.add_argument("talent"); x.set_defaults(f=cmd_buy)
    s.add_parser("pause").set_defaults(f=cmd_pause)
    s.add_parser("resume").set_defaults(f=cmd_resume)
    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
