# 实验六

编写一个包含多个售票窗口的售票程序。假设有票的编号为 1-100，有 4 个窗口可以同 时售票，车票按顺序依次售出。1 号和 2 号窗口有 20 人排队，3 号和 4 号窗口有 30 人 排队，每售出一张票，显示售票的窗口号、票号以及余票数量。

---

运行：

```bash
# office
python -m office
# client
python client.py
```

> [!CAUTION]
> 由于最近精力有限，代码存在不少 Bug 暂时没有修复，不建议参考！
> 本实验预期解决方法为：使用多线程同步机制，实现多个窗口同时售票。一个可能的思路是售票厅作为一个线程，每个窗口作为一个线程，售票厅线程负责分配票号，窗口线程负责售票。若有人看到这里，你可以参考下面的一些链接：
>
> - [多线程同步的四种方式（史上最详细+用例） - Chilk - 博客园](https://www.cnblogs.com/Chlik/p/13556720.html)
> - [python 网口通讯 tcp/dcp 通信 和 时间同步机制 （重要） - L707 - 博客园](https://www.cnblogs.com/L707/p/16367160.html)
> - [selectors --- 高层级 I/O 复用 &#8212; Python 3.13.1 文档](https://docs.python.org/zh-cn/3/library/selectors.html)
