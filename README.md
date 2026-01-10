# qBittorrent Kisssub Search Plugin

这是一个用于 qBittorrent 的搜索插件，支持从爱恋动漫 (kisssub.org) 搜索资源。

## 功能特性

- 支持中文搜索
- 自动处理 URL 编码问题
- 解析发布时间
- 支持 RSS 订阅格式解析

## 安装方法

### 在线安装（推荐）

1. 复制以下链接：
   ```text
   https://raw.githubusercontent.com/SalicylicAcid/qb-kisssub-plugin/main/kisssub.py
   ```
2. 在 qBittorrent 中，点击“搜索”标签页。
3. 点击右下角的“搜索插件...”按钮。
4. 点击“安装新插件” -> **“Web 链接”**。
5. 粘贴链接并点击“确定”。

### 本地安装

1. **下载插件文件**:
   下载本项目中的 `kisssub.py` 文件。

2. **定位插件目录**:
   - **Windows**: `%localappdata%\qBittorrent\nova3\engines\`
   - **Linux**: `~/.local/share/data/qBittorrent/nova3/engines/`
   - **macOS**: `~/Library/Application Support/qBittorrent/nova3/engines/`

   *如果找不到目录，可以在 qBittorrent 的“搜索”标签页中，点击右下角的“搜索插件...”按钮，然后点击“安装新插件” -> “本地文件”，选择下载的 `kisssub.py` 即可自动安装。*

3. **使用**:
   重启 qBittorrent（推荐），在搜索框输入关键词，选择 `Kisssub` 引擎（或“所有分类”）即可搜索。

## 开发相关

基于 Python 3 编写，依赖 qBittorrent 的 `novaprinter` 和 `helpers` 模块。
