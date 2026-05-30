<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.10+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
  <img src="https://img.shields.io/badge/languages-30+-purple.svg" alt="Languages">
</p>

<p align="center">
  <a href="#english">English</a> | 
  <a href="#简体中文">简体中文</a> | 
  <a href="#繁體中文">繁體中文</a>
</p>

---

<a name="english"></a>
# 🧹 StripComment

> **Intelligently strip comments from source code while preserving strings and supporting 30+ programming languages.**

StripComment is a powerful, lightweight CLI tool designed to remove comments from source code files with precision. It uses a state-machine parser to accurately identify and remove comments while preserving string literals, handling escape sequences, and offering flexible preservation options.

## 🎉 Why StripComment?

- **📦 Code Minification** - Prepare code for production by removing unnecessary comments
- **🔍 Code Analysis** - Clean code before processing with analysis tools
- **🔒 Privacy Protection** - Remove sensitive information hidden in comments
- **📊 Documentation Generation** - Extract clean code for documentation purposes
- **🚀 Build Optimization** - Reduce file size for faster loading

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🗑️ **Smart Comment Removal** | Accurately removes single-line and multi-line comments |
| 🔒 **String Preservation** | Intelligently preserves strings containing comment-like patterns |
| 📚 **30+ Languages** | Supports Python, JavaScript, TypeScript, Java, C/C++, Go, Rust, and more |
| 🎯 **Selective Preservation** | Keep docstrings, copyright notices, TODOs, and license headers |
| 📊 **Statistics** | Detailed reports on comments removed, lines saved, bytes reduced |
| 👀 **Dry Run Mode** | Preview changes without modifying files |
| 🔄 **Batch Processing** | Process entire directories recursively |
| ⚡ **Fast & Lightweight** | Pure Python, no external dependencies for core functionality |

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI
pip install stripcomment

# Or install with all optional dependencies
pip install "stripcomment[all]"
```

### Basic Usage

```bash
# Strip comments from a single file
stripcomment strip script.py

# Process a directory recursively
stripcomment strip ./src --recursive

# Preview changes without modifying files
stripcomment strip script.py --dry-run

# Preserve docstrings and TODOs
stripcomment strip script.py --preserve-docstrings --preserve-todos
```

## 📖 Detailed Usage Guide

### Command Reference

#### `stripcomment strip`

Strip comments from source code files.

```bash
stripcomment strip [OPTIONS] [PATH]
```

**Options:**

| Option | Description |
|--------|-------------|
| `-o, --output PATH` | Output file or directory |
| `-l, --language TEXT` | Force language (auto-detected by default) |
| `--preserve-docstrings` | Preserve docstrings |
| `--preserve-copyright` | Preserve copyright comments |
| `--preserve-todos` | Preserve TODO/FIXME comments |
| `--preserve-license` | Preserve license comments |
| `-p, --preserve PATTERN` | Preserve comments matching regex pattern |
| `--remove-blank-lines` | Remove blank lines after stripping |
| `--minify` | Minify output (remove extra whitespace) |
| `-d, --dry-run` | Preview changes without modifying files |
| `-b, --backup` | Create .bak backup files |
| `-r, --recursive` | Process directories recursively |
| `-e, --extensions TEXT` | Comma-separated list of extensions to process |
| `-V, --verbose` | Show detailed output |

#### `stripcomment languages`

List all supported programming languages.

```bash
stripcomment languages
```

#### `stripcomment stats`

Show comment statistics for a file.

```bash
stripcomment stats script.py
```

### Python API

```python
from stripcomment import StripComment
from stripcomment.languages import get_language_by_extension

# Initialize with language config
config = get_language_by_extension(".py")
stripper = StripComment(config)

# Strip comments from code string
code = '''
def hello():
    """Say hello."""
    # This is a comment
    print("Hello, World!")  # Inline comment
'''

result = stripper.strip(code)
print(result.stripped_code)
print(f"Comments removed: {result.comments_removed}")
print(f"Bytes saved: {result.bytes_saved}")
```

### Examples

#### Preserve Important Comments

```bash
# Keep copyright and license headers
stripcomment strip ./src --preserve-copyright --preserve-license

# Keep TODOs for future reference
stripcomment strip ./src --preserve-todos

# Custom preservation pattern
stripcomment strip ./src --preserve "@author"
```

#### Batch Processing

```bash
# Process all Python files in a directory
stripcomment strip ./project --recursive --extensions .py

# Process multiple file types
stripcomment strip ./project --recursive --extensions .py,.js,.ts

# Create backups before processing
stripcomment strip ./project --recursive --backup
```

#### Piped Input

```bash
# Pipe input
cat script.py | stripcomment strip --language python

# Combine with other tools
cat script.py | stripcomment strip --language python > clean.py
```

## 💡 Supported Languages

| Category | Languages |
|----------|-----------|
| **Web** | JavaScript, TypeScript, HTML, CSS, PHP |
| **Systems** | C, C++, Go, Rust, Assembly |
| **Scripting** | Python, Ruby, Perl, Lua, R |
| **JVM** | Java, Kotlin, Scala |
| **Mobile** | Swift, Dart |
| **Shell** | Bash, PowerShell |
| **Data** | SQL, YAML, TOML, JSON5 |
| **Other** | Haskell, Elixir, Erlang, Fortran, MATLAB, Julia, Vim Script |

## 📦 Project Structure

```
stripcomment/
├── src/stripcomment/
│   ├── __init__.py      # Package initialization
│   ├── core.py          # Core stripping logic
│   ├── languages.py     # Language configurations
│   └── cli.py           # Command-line interface
├── tests/               # Test suite
├── pyproject.toml       # Project configuration
└── README.md            # Documentation
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="简体中文"></a>
# 🧹 StripComment

> **智能移除源代码中的注释，同时保护字符串内容，支持 30+ 编程语言。**

StripComment 是一个强大、轻量级的命令行工具，专为精确移除源代码注释而设计。它使用状态机解析器准确识别并移除注释，同时保护字符串字面量、处理转义序列，并提供灵活的保留选项。

## 🎉 为什么选择 StripComment？

- **📦 代码压缩** - 移除不必要的注释，准备生产环境代码
- **🔍 代码分析** - 在使用分析工具处理前清理代码
- **🔒 隐私保护** - 移除隐藏在注释中的敏感信息
- **📊 文档生成** - 提取干净的代码用于文档编写
- **🚀 构建优化** - 减少文件大小，加快加载速度

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🗑️ **智能注释移除** | 精准移除单行和多行注释 |
| 🔒 **字符串保护** | 智能保护包含注释模式的字符串 |
| 📚 **30+ 语言** | 支持 Python、JavaScript、TypeScript、Java、C/C++、Go、Rust 等 |
| 🎯 **选择性保留** | 保留文档字符串、版权声明、TODO 和许可证头 |
| 📊 **统计报告** | 详细报告移除的注释数、节省的行数和字节数 |
| 👀 **干运行模式** | 预览变更而不修改文件 |
| 🔄 **批量处理** | 递归处理整个目录 |
| ⚡ **快速轻量** | 纯 Python 实现，核心功能无外部依赖 |

## 🚀 快速开始

### 安装

```bash
# 从 PyPI 安装
pip install stripcomment

# 或安装所有可选依赖
pip install "stripcomment[all]"
```

### 基本用法

```bash
# 从单个文件移除注释
stripcomment strip script.py

# 递归处理目录
stripcomment strip ./src --recursive

# 预览变更而不修改文件
stripcomment strip script.py --dry-run

# 保留文档字符串和 TODO
stripcomment strip script.py --preserve-docstrings --preserve-todos
```

## 📖 详细使用指南

### 命令参考

#### `stripcomment strip`

从源代码文件移除注释。

```bash
stripcomment strip [选项] [路径]
```

**选项：**

| 选项 | 描述 |
|------|------|
| `-o, --output 路径` | 输出文件或目录 |
| `-l, --language 语言` | 强制指定语言（默认自动检测） |
| `--preserve-docstrings` | 保留文档字符串 |
| `--preserve-copyright` | 保留版权注释 |
| `--preserve-todos` | 保留 TODO/FIXME 注释 |
| `--preserve-license` | 保留许可证注释 |
| `-p, --preserve 模式` | 保留匹配正则表达式的注释 |
| `--remove-blank-lines` | 移除注释后删除空行 |
| `--minify` | 压缩输出（移除多余空白） |
| `-d, --dry-run` | 预览变更而不修改文件 |
| `-b, --backup` | 创建 .bak 备份文件 |
| `-r, --recursive` | 递归处理目录 |
| `-e, --extensions 扩展名` | 逗号分隔的扩展名列表 |
| `-V, --verbose` | 显示详细输出 |

#### `stripcomment languages`

列出所有支持的编程语言。

```bash
stripcomment languages
```

#### `stripcomment stats`

显示文件的注释统计信息。

```bash
stripcomment stats script.py
```

### Python API

```python
from stripcomment import StripComment
from stripcomment.languages import get_language_by_extension

# 使用语言配置初始化
config = get_language_by_extension(".py")
stripper = StripComment(config)

# 从代码字符串移除注释
code = '''
def hello():
    """打招呼。"""
    # 这是一个注释
    print("你好，世界！")  # 行内注释
'''

result = stripper.strip(code)
print(result.stripped_code)
print(f"移除的注释数: {result.comments_removed}")
print(f"节省的字节数: {result.bytes_saved}")
```

### 示例

#### 保留重要注释

```bash
# 保留版权和许可证头
stripcomment strip ./src --preserve-copyright --preserve-license

# 保留 TODO 以供后续参考
stripcomment strip ./src --preserve-todos

# 自定义保留模式
stripcomment strip ./src --preserve "@author"
```

#### 批量处理

```bash
# 处理目录中的所有 Python 文件
stripcomment strip ./project --recursive --extensions .py

# 处理多种文件类型
stripcomment strip ./project --recursive --extensions .py,.js,.ts

# 处理前创建备份
stripcomment strip ./project --recursive --backup
```

#### 管道输入

```bash
# 管道输入
cat script.py | stripcomment strip --language python

# 与其他工具组合
cat script.py | stripcomment strip --language python > clean.py
```

## 💡 支持的语言

| 类别 | 语言 |
|------|------|
| **Web** | JavaScript, TypeScript, HTML, CSS, PHP |
| **系统** | C, C++, Go, Rust, Assembly |
| **脚本** | Python, Ruby, Perl, Lua, R |
| **JVM** | Java, Kotlin, Scala |
| **移动** | Swift, Dart |
| **Shell** | Bash, PowerShell |
| **数据** | SQL, YAML, TOML, JSON5 |
| **其他** | Haskell, Elixir, Erlang, Fortran, MATLAB, Julia, Vim Script |

## 🤝 贡献指南

欢迎贡献代码！请随时提交 Pull Request。

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详情请见 [LICENSE](LICENSE) 文件。

---

<a name="繁體中文"></a>
# 🧹 StripComment

> **智慧移除原始碼中的註解，同時保護字串內容，支援 30+ 程式語言。**

StripComment 是一個強大、輕量級的命令列工具，專為精確移除原始碼註解而設計。它使用狀態機解析器準確識別並移除註解，同時保護字串字面量、處理轉義序列，並提供靈活的保留選項。

## 🎉 為什麼選擇 StripComment？

- **📦 程式碼壓縮** - 移除不必要的註解，準備生產環境程式碼
- **🔍 程式碼分析** - 在使用分析工具處理前清理程式碼
- **🔒 隱私保護** - 移除隱藏在註解中的敏感資訊
- **📊 文件生成** - 提取乾淨的程式碼用於文件編寫
- **🚀 建置最佳化** - 減少檔案大小，加快載入速度

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🗑️ **智慧註解移除** | 精準移除單行和多行註解 |
| 🔒 **字串保護** | 智慧保護包含註解模式的字串 |
| 📚 **30+ 語言** | 支援 Python、JavaScript、TypeScript、Java、C/C++、Go、Rust 等 |
| 🎯 **選擇性保留** | 保留文件字串、版權宣告、TODO 和授權條款標頭 |
| 📊 **統計報告** | 詳細報告移除的註解數、節省的行數和位元組數 |
| 👀 **乾運行模式** | 預覽變更而不修改檔案 |
| 🔄 **批次處理** | 遞迴處理整個目錄 |
| ⚡ **快速輕量** | 純 Python 實作，核心功能無外部相依性 |

## 🚀 快速開始

### 安裝

```bash
# 從 PyPI 安裝
pip install stripcomment

# 或安裝所有可選相依性
pip install "stripcomment[all]"
```

### 基本用法

```bash
# 從單一檔案移除註解
stripcomment strip script.py

# 遞迴處理目錄
stripcomment strip ./src --recursive

# 預覽變更而不修改檔案
stripcomment strip script.py --dry-run

# 保留文件字串和 TODO
stripcomment strip script.py --preserve-docstrings --preserve-todos
```

## 📖 詳細使用指南

### 命令參考

#### `stripcomment strip`

從原始碼檔案移除註解。

```bash
stripcomment strip [選項] [路徑]
```

**選項：**

| 選項 | 描述 |
|------|------|
| `-o, --output 路徑` | 輸出檔案或目錄 |
| `-l, --language 語言` | 強制指定語言（預設自動偵測） |
| `--preserve-docstrings` | 保留文件字串 |
| `--preserve-copyright` | 保留版權註解 |
| `--preserve-todos` | 保留 TODO/FIXME 註解 |
| `--preserve-license` | 保留授權條款註解 |
| `-p, --preserve 模式` | 保留匹配正則表示式的註解 |
| `--remove-blank-lines` | 移除註解後刪除空行 |
| `--minify` | 壓縮輸出（移除多餘空白） |
| `-d, --dry-run` | 預覽變更而不修改檔案 |
| `-b, --backup` | 建立 .bak 備份檔案 |
| `-r, --recursive` | 遞迴處理目錄 |
| `-e, --extensions 副檔名` | 逗號分隔的副檔名列表 |
| `-V, --verbose` | 顯示詳細輸出 |

#### `stripcomment languages`

列出所有支援的程式語言。

```bash
stripcomment languages
```

#### `stripcomment stats`

顯示檔案的註解統計資訊。

```bash
stripcomment stats script.py
```

### Python API

```python
from stripcomment import StripComment
from stripcomment.languages import get_language_by_extension

# 使用語言設定初始化
config = get_language_by_extension(".py")
stripper = StripComment(config)

# 從程式碼字串移除註解
code = '''
def hello():
    """打招呼。"""
    # 這是一個註解
    print("你好，世界！")  # 行內註解
'''

result = stripper.strip(code)
print(result.stripped_code)
print(f"移除的註解數: {result.comments_removed}")
print(f"節省的位元組數: {result.bytes_saved}")
```

## 💡 支援的語言

| 類別 | 語言 |
|------|------|
| **Web** | JavaScript, TypeScript, HTML, CSS, PHP |
| **系統** | C, C++, Go, Rust, Assembly |
| **腳本** | Python, Ruby, Perl, Lua, R |
| **JVM** | Java, Kotlin, Scala |
| **行動** | Swift, Dart |
| **Shell** | Bash, PowerShell |
| **資料** | SQL, YAML, TOML, JSON5 |
| **其他** | Haskell, Elixir, Erlang, Fortran, MATLAB, Julia, Vim Script |

## 🤝 貢獻指南

歡迎貢獻程式碼！請隨時提交 Pull Request。

1. Fork 本儲存庫
2. 建立特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交變更 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 開啟 Pull Request

## 📄 授權條款

本專案採用 MIT 授權條款 - 詳情請見 [LICENSE](LICENSE) 檔案。
