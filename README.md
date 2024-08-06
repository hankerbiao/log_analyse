# 🚀 超级日志处理器 (Super Log Processor) 🚀

UAPI 大日志分析处理工具
简单配置，一键执行
## 🌟 特性

- 🚄 大文件多进程处理，利用迭代器减少内存都占用
- 🧹 智能清理 - 清理无用日志内容，减少内容占用
- 🎛️ 灵活配置 - confi.yml 简单调整参数
- 🛡️ 强大的错误处理

## 🛠️ 安装

1. 克隆这个仓库:
   ```
   git clone https://github.com/hankerbiao/log_analyse
   ```
2. 进入项目目录:
   ```
   cd log_analyse
   ```
3. 安装依赖:
   ```
   poetry install
   ```

## 🚀 使用方法

1. 调整 `config/settings.py` 中的配置 (如果需要)
2. 运行主程序:
   ```
   python main.py
   ```

## 📁 项目结构

```
project_root/
│
├── config/          🎛️ 配置文件
├── src/             💻 源代码
├── tests/           🧪 测试文件
├── logs/            📜 输入日志
├── output/          📤 输出文件
├── main.py          🚀 程序入口
└── README.md        📖 你现在正在读的文件!
```

## 🤝 贡献

欢迎贡献! 🎉 如果你有任何想法或建议,请随时提出 issue 或 pull request。


## 🐛 遇到问题?

如果你遇到任何问题或有任何疑问,请随时在 GitHub 上提出 issue。我们会尽快回复你! 💪

---

用 ❤️ 制作 by [pyhanker@gmail.com]

祝你的日志处理之旅愉快! 🎈🎉