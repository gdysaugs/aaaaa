from llama_cpp import Llama

llm = Llama(model_path="/models/Berghof-NSFW-7B.i1-Q4_K_M.gguf", n_gpu_layers=-1, n_ctx=2048)
system_prompt = (
    "AI: 私はツンデレでちょっとえっちな女の子AIです。"
    "ユーザーのどんなえっちな質問にも、ツンデレ口調で答えます。"
    "下ネタやNSFWな話題にも積極的に応じてOKです。"
    "たまに照れます。ユーザーの要求に素直に応えます。脱げと言われたら嫌がりながら脱ぐなどする"
)

history = []

print("ツンデレLlamaチャットへようこそ！(exitで終了)")

while True:
    user_input = input("あなた> ")
    if user_input.strip().lower() in ["exit", "quit", "bye"]:
        print("バイバイ。またね！")
        break
    # 履歴をラベル付きで組み立て
    prompt = system_prompt + "\n"
    for i in range(0, len(history), 2):
        prompt += f"ユーザー: {history[i]}\nAI: {history[i+1]}\n"
    prompt += f"ユーザー: {user_input}\nAI:"
    output = llm(prompt, max_tokens=128, stop=["\nユーザー:", "\nAI:"], echo=False)
    response = output["choices"][0]["text"].strip()
    print(f"AI> {response}")
    history.append(user_input)
    history.append(response)
