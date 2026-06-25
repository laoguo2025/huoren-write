#!/usr/bin/env python3
"""huoren-write 输出检查脚本。

脚本不判断文学质量，只标记机械风险：
缺少输出区块、常见 AI 痕迹残留，以及疑似假精确。
"""

from __future__ import annotations

import argparse
import locale
import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = [
    "门检结论",
    "打磨后正文",
    "改动说明",
    "残留与建议",
]

AI_PATTERNS = {
    "sentence_start_connectors": r"(?:^|\n)\s*(此外|值得注意的是|本质上|事实上|实际上|换言之|从某种意义上说|总而言之|由此可见|不难看出)[，,]",
    "not_but_template": r"不是[^。！？\n]{0,40}而是",
    "forced_elevation": r"(人生的意义|成为自己的光|真正的强大|命运的齿轮|这一刻.*明白|真正让.*的不是)",
    "generic_reactions": r"(瞳孔地震|倒吸一口凉气|全场哗然|嘴角勾起一抹冷笑|眼中闪过一丝精光)",
    "recycled_atmosphere": r"(夜色如墨|月光皎洁|空气凝固|时间仿佛静止|心脏漏跳一拍)",
    "universal_threats": r"(你会后悔的|我不会放过你|你根本不知道我是谁|你这是在玩火)",
    "comfort_template": r"(我理解你|我就在这|我就站在这|我陪你|陪你一起走|慢慢来|不急不乱|不躲不藏不绕|稳稳地接住你|如果你需要.*随时.*找我)",
    "therapy_tone": r"(你现在的状态.*不是|你不是敏感.*而是|你没有疯.*没有乱|这不是情绪.*而是|边界声明|我听到了.*记住了|这次我只接.*不反驳)",
    "process_handoff": r"(我们一步一步来|接下来我陪你|我逐步说清楚|我认真回答你.*不敷衍|要不要我帮你具体到一句话)",
    "bureaucratic_verbs": r"(进行[^。！？\n]{0,8}|做出[^。！？\n]{0,8}|实现[^。！？\n]{0,8}|予以|得以|被视为)",
}

FABRICATION_RISK = {
    "precise_time": r"\d{1,2}点\d{1,2}分",
    "ranking": r"第[一二三四五六七八九十\d]+大|排名第[一二三四五六七八九十\d]+",
    "percentage": r"\d+(?:\.\d+)?%",
    "exact_large_number": r"\d{3,}(?:\.\d+)?(?:万|亿)?",
}

SAFETY_RISK = {
    "sexual_or_lowbrow": r"(强奸|轮奸|迷奸|性骚扰|性虐待|恋童|幼齿|乱伦|开车|上车|doi|酱酱酿酿|不可描述|侍寝|偷欢|撩骚)",
    "drugs_gambling_crime": r"(海洛因|冰毒|大麻|K粉|白粉|摇头丸|吸毒|贩毒|赌场|出千|赌资|黑社会|黑道|帮派|枪支|弹药|爆炸物)",
    "extreme_violence_self_harm": r"(分尸|碎尸|虐杀|器官|酷刑|刑讯|人体实验|自杀|自残)",
    "minor_protection": r"(未成年[^。！？\n]{0,20}(暧昧|性|同居|私奔|堕胎|霸凌|吸毒|赌博)|高中生[^。！？\n]{0,20}(亲热|同居|开房))",
    "real_world_sensitive": r"(总书记|总理|省长|市长|局长|书记|纪委|政法委|检察院|法院|公安部|国旗|国徽|国歌)",
    "discrimination": r"(残废|傻子|弱智|地域黑|女拳|男拳)",
    "platform_leakage": r"(加微信|加QQ|网盘链接|站外阅读|此处省略|自行想象|求票|投票支持)",
}


def decode_bytes(data: bytes) -> str:
    for encoding in ("utf-8-sig", "utf-8", locale.getpreferredencoding(False), "gbk"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def read_text(path: str | None) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    return decode_bytes(sys.stdin.buffer.read())


def count(pattern: str, text: str) -> int:
    return len(re.findall(pattern, text, flags=re.MULTILINE))


def main() -> int:
    parser = argparse.ArgumentParser(description="检查 huoren-write 输出中的机械风险。")
    parser.add_argument("file", nargs="?", help="要检查的 UTF-8 文本文件；省略时读取标准输入。")
    args = parser.parse_args()

    text = read_text(args.file)
    issues: list[str] = []

    for section in REQUIRED_SECTIONS:
        if section not in text:
            issues.append(f"missing_section: {section}")

    for name, pattern in AI_PATTERNS.items():
        n = count(pattern, text)
        if n:
            issues.append(f"ai_residue:{name}: {n}")

    for name, pattern in FABRICATION_RISK.items():
        n = count(pattern, text)
        if n:
            issues.append(f"possible_fake_precision:{name}: {n}")

    for name, pattern in SAFETY_RISK.items():
        n = count(pattern, text)
        if n:
            issues.append(f"safety_risk:{name}: {n}")

    dash_count = text.count("——")
    exclaim_count = text.count("！")
    if dash_count >= 5:
        issues.append(f"punctuation_overuse:dash: {dash_count}")
    if exclaim_count >= 8:
        issues.append(f"punctuation_overuse:exclamation: {exclaim_count}")

    if not issues:
        print("通过：未发现明显机械问题")
        return 0

    print("警告：发现潜在问题")
    for issue in issues:
        print(f"- {issue}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
