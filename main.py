from zhu import ask

def main():
    print("=" * 50)
    print("游戏情报 Agent 已启动，输入 q 退出")
    print("=" * 50)

    while True:
        question = input("\n你: ").strip()
        if question.lower() in ("q", "quit", "exit"):
            print("再见 👋")
            break
        if not question:
            continue
        try:
            answer = ask(question)
            print(f"\nAgent: {answer}")
        except Exception as e:
            print(f"\n[错误] {type(e).__name__}: {e}")

if __name__ == "__main__":
    main()