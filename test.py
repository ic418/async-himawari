import curses
import time

def main(stdscr):
    # 清屏
    stdscr.clear()
    
    # 打印初始文本
    stdscr.addstr(0, 0, "Hello, world!")
    stdscr.refresh()
    
    # 等待一段时间
    time.sleep(1)
    
    # 移动光标到开始位置并更改文本
    stdscr.move(0, 0)
    stdscr.addstr("Goodbye, world!")
    stdscr.refresh()
    
    # 等待用户输入
    stdscr.getch()

# 使用curses包的wrapper方法启动main函数
curses.wrapper(main)