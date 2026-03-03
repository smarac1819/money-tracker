# Contributing / 贡献指南

Thank you for your interest in improving **Smart Finance Tracker Pro**!  
感谢您有兴趣为**智能财务记账管家 Pro** 做出贡献！

All contributions are welcome via **Pull Request** and require review before merging.  
所有贡献均通过 **Pull Request** 提交，需经审核后方可合并。

---

## How to Contribute / 如何贡献

### 1. Fork & Clone

```bash
git clone https://github.com/TRYuuu233/money-tracker.git
cd money-tracker
```

### 2. Create a Branch / 创建分支

```bash
git checkout -b feature/your-feature-name
# e.g.: git checkout -b i18n/japanese
```

### 3. Make Changes & Commit / 修改并提交

Follow the existing code style. Run the app to verify your changes work.  
遵循现有代码风格。运行应用确认修改正确。

```bash
python main.py
git add -A
git commit -m "feat: describe your change"
```

### 4. Open a Pull Request / 提交 PR

Push to your fork and open a PR against `main`.  
推送到您的 Fork，并向 `main` 分支提交 PR。

---

## 🌐 Adding a New Language / 添加新语言

The i18n system lives in `common/locale.py`. Adding a new language (e.g. Japanese) is straightforward:  
多语言系统在 `common/locale.py`，添加新语言（如日语）非常简单：

### Step 1 — Add language code to `STRINGS`

Open `common/locale.py`. For every entry in `STRINGS`, add your language code:

```python
STRINGS = {
    "app_title": {
        "zh": "智能财务记账管家",
        "en": "Smart Finance Tracker",
        "ja": "スマート家計簿"          # ← add your language here
    },
    ...
}
```

### Step 2 — Add the language option to Settings

In `ui/settings_dialog.py`, find the `_build_language_section()` method and add your language to the radio button group:

```python
# Example: add Japanese option
lang_ja = QRadioButton(L("lang_ja"))
lang_ja.setChecked(get_lang() == "ja")
lang_ja.toggled.connect(lambda checked: set_lang("ja") if checked else None)
lang_group.addButton(lang_ja)
lang_layout.addWidget(lang_ja)
```

And add the string key:

```python
"lang_ja": {"zh": "日本語", "en": "Japanese", "ja": "日本語"},
```

### Step 3 — Test / 测试

Run the app in both the new language and existing languages. Ensure all strings are translated and no `KeyError` occurs.  
分别用新语言和已有语言运行应用。确认所有字符串均已翻译，无 `KeyError`。

### Step 4 — Submit PR / 提交 PR

Include in your PR description:

- Language name and code used
- Screenshot of the app running in the new language
- Any untranslated strings and why

---

## Types of Contributions Welcome / 欢迎的贡献类型

| Type | Description |
|---|---|
| 🌐 New language | Add a new locale to `common/locale.py` |
| 🐛 Bug fix | Fix a bug — please describe the expected vs actual behavior |
| ✨ New feature | Discuss in an Issue first before implementing |
| 📖 Documentation | Improve README, CONTRIBUTING, or code comments |
| 🎨 UI improvement | Refinements to the visual design |

---

## Code Style / 代码风格

- Python 3.11+ compatible
- PyQt6 only (no PySide6/PyQt5 compatibility needed)
- All UI strings must go through `L("key")` from `common/locale.py`
- No hard-coded Chinese or English strings in UI code

---

## Questions? / 有问题？

Open a GitHub Issue or start a Discussion.  
欢迎开 Issue 或发起 Discussion。
