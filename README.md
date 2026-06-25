# huoren-write

短剧剧本与网文小说专属的“活人感”打磨 Skill，用来清理 AI 写作痕迹、模板腔、假精确、万能安抚腔和过度升华，让文本更像真人写出来、说出来，同时保留原剧情事实、人设、人物关系、文本格式和表达意图。

当前版本：`0.1`

## 适用场景

- 短剧剧本对白、旁白、OS、动作提示的去 AI 味和口语化打磨
- 网文小说叙述、人物对话、心理活动、章节片段的活人感优化
- 清理机械连接词、工整排比、三连词、强行金句、伪文学收尾
- 处理“我理解你”“我陪你”“边界声明”等万能安抚式 AI 八股句
- 标注和降敏疑似平台红线、低俗违规、侵权或内容安全风险

## 不适用场景

- 不从零写剧情
- 不设计钩子、爽点、集尾悬念或故事节奏
- 不新增人物、关系、伏笔、反转、地点、时间线或设定
- 不替代平台审核、法律判断或事实核查
- 不用于绕过 AI 检测

## 核心原则

1. 不新增剧情事实。
2. 保留人物声口，不把所有角色都改成同一种随意口吻。
3. 只处理表达层问题，不擅自改剧情结构。
4. 保留剧本和小说各自的载体格式。
5. 宁可保留一点真人写作的粗糙，也不要改成过度光滑的标准答案。
6. 遇到红线风险时，只做表达降敏和风险提示，不编造替代剧情。

## 目录结构

```text
huoren-write/
  SKILL.md
  VERSION
  README.md
  references/
    ai-patterns.md
    human-texture.md
    character-voice.md
    format-preservation.md
    safety-and-banned-content.md
    scoring-and-output.md
    examples.md
  scripts/
    check_output.py
```

## 文件说明

- `SKILL.md`：Skill 主入口，定义触发范围、工作流程、边界和输出格式。
- `VERSION`：当前版本号。
- `references/ai-patterns.md`：AI 写作痕迹库，包括连接词、三连词、金句升华、万能安抚腔、短剧/网文专项痕迹等。
- `references/human-texture.md`：活人感打磨规则，指导如何保留自然、粗糙、迟疑和不完整感。
- `references/character-voice.md`：人物声口规则，防止角色被改成同一种 AI 式温柔、客服腔或心理咨询腔。
- `references/format-preservation.md`：格式保真规则，避免把剧本改成小说，或把小说改成剧本。
- `references/safety-and-banned-content.md`：内容安全与禁用表达风险规则，适用于网文和短剧的通用降敏。
- `references/scoring-and-output.md`：最终自检和输出格式规范。
- `references/examples.md`：少量改写示例，用于校准尺度。
- `scripts/check_output.py`：轻量检查脚本，用于提示输出区块缺失、AI 痕迹残留、假精确和内容安全风险。

## 使用方式

把整个目录作为 Skill 提供给支持 Skill 的 agent，或让 agent 读取 `SKILL.md` 后按规则处理文本。

示例提示：

```text
请使用 huoren-write 打磨下面这段短剧/网文文本：

[粘贴原文]
```

默认输出包含：

```text
### 门检结论
### 打磨后正文
### 改动说明
### 残留与建议
```

## 检查脚本

可以用脚本对输出做机械风险检查：

```bash
python scripts/check_output.py output.txt
```

也可以从标准输入读取：

```bash
cat output.txt | python scripts/check_output.py
```

脚本只做提示，不判断文学质量，也不替代人工审稿或平台审核。

## 版本记录

### 0.1

- 建立短剧剧本与网文小说通用的活人感打磨流程。
- 支持 AI 痕迹清理、人物声口校准、格式保真、内容安全降敏和结构化输出。
- 提供轻量检查脚本 `scripts/check_output.py`。

## License

未声明开源许可证前，默认保留所有权利。
