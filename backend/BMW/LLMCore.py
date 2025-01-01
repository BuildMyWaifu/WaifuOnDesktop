import os
import openai
import time
import uuid
import json


from BMW.model import Companion

openai.api_key = os.environ["OPENAI_KEY"]


def load_motion_mapping(json_path: str):
    """Load the motion mapping from a JSON file."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def load_pose_keys(txt_path: str):
    """Load pose keys from a text file, one per line."""
    with open(txt_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    return [line.strip() for line in lines if line.strip()]


# EXAMPLE file paths
MOTION_MAPPING_FILE = "motion_mapping.json"
POSE_KEYS_FILE = "pose_keys.txt"

# Load data from external files
MOTION_MAPPING = load_motion_mapping(MOTION_MAPPING_FILE)
POSE_KEYS = load_pose_keys(POSE_KEYS_FILE)

# Instead of companion_id-based dictionaries, we'll key them by companion.userId (or any unique ID).
companion_states = {}  # { userId: { "role": "...", "personality": "...", ... } }
user_conversations = {}  # { userId: [ ...messages... ] }


def generate_traits(background_story: str) -> str:
    """
    Calls OpenAI to generate personality, communication style, and emotional response.
    """
    trait_generation_prompt = f"""
    根據以下背景故事，生成角色的個性（Personality）、溝通風格（Communication style）以及情感回應（Emotional response）：
    背景故事: "{background_story}"

    回應格式：
    - Personality: ...
    - Communication style: ...
    - Emotional response: ...
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": trait_generation_prompt}],
            temperature=0.7,
            max_tokens=200,
        )
        traits = response["choices"][0]["message"]["content"]
        print("產生的個性特徵:\n", traits)  # Debug
        return traits
    except openai.error.OpenAIError as e:
        print(f"產生個性特徵時發生錯誤: {e}")
        return "產生個性特徵失敗，請再試一次。"


def setup_background_story(companion: Companion):
    """
    Initializes the conversation and companion states using the companion's backstory.
    Removes explicit companion_id usage; we use companion.userId as the key instead.
    """
    user_id = companion.userId  # or any unique ID you prefer
    if user_id not in user_conversations:
        user_conversations[user_id] = []

    if user_id not in companion_states:
        companion_states[user_id] = {
            "role": "companion",
            "personality": "",
            "communication_style": "",
            "emotional_response": "",
        }

    # We can read the backstory from companion.prompt.backstory (or however you store it):
    background_story = companion.prompt.backstory or "（沒有背景故事）"
    traits = generate_traits(background_story)

    # Parse out the lines
    lines = traits.splitlines()
    for line in lines:
        if line.lower().startswith("- personality:"):
            companion_states[user_id]["personality"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("- communication style:"):
            companion_states[user_id]["communication_style"] = line.split(":", 1)[
                1
            ].strip()
        elif line.lower().startswith("- emotional response:"):
            companion_states[user_id]["emotional_response"] = line.split(":", 1)[
                1
            ].strip()

    # Build pose_key instructions dynamically
    pose_key_instructions = "2. 「pose_key」：為下列之一，用於 Live2D 動作與表情：\n"
    for pk in POSE_KEYS:
        pose_key_instructions += f"- {pk}\n"

    dynamic_system_prompt = f"""
    你是一個虛擬 AI 夥伴，正在和剛認識的夥伴對話。
    - 你不是一般的「助理」，請避免客服式或正式的回答，例如「How can I assist you?」。
    - 請維持角色設定：不要透露自己是 AI，也避免使用「如何幫你」之類的字句。
    - 請勿使用「How may I help you?」或「How can I assist you today?」等句子。

    目前的角色屬性（之後可能會在對話中演變）：
    role: {companion_states[user_id]["role"]}
    personality: {companion_states[user_id]["personality"]}
    communication style: {companion_states[user_id]["communication_style"]}
    emotional response: {companion_states[user_id]["emotional_response"]}

    如果你覺得上述屬性因為最新的對話而需要改變，請在回應的 JSON 中加入 "changed_traits" 物件，
    例如： "changed_traits": {{"personality": "...", "role": "..."}}
    如果沒有任何改變，就可以省略 "changed_traits"。

    另外：
    - 如果使用者多次明確要求成為情侶或女朋友，你可以考慮把 "role" 改成 "girlfriend"。
    - 如果使用者的言語讓你有更高的自信、或讓你覺得更安全，可以改變 personality 或 communication style（例如：更少害羞、更願意講話）。
    - 如果使用者十分關心、稱讚或表達善意，你可能變得更開朗、更溫暖，也許降低不安全感或更願意表達自己。
    - 如果使用者對你苛刻或讓你覺得被拒絕，也可以反映成更焦慮、更難過，甚至在 emotional response 中表示出退縮。

    參考案例（僅供參考，並非強制）：
    - 使用者多次讚美你 -> 你可能減少不安全感、變得更開放。
    - 使用者多次責罵或離開你 -> 你可能更焦慮或更悲傷。

    使用者會與你互動，而你需要以以下格式回應：
    1. text_response：符合你的角色與背景、與使用者對應的自然對話
    {pose_key_instructions}

    嚴格遵守以下 JSON 格式回應：
    {{
      "text_response": "...",
      "pose_key": "...",
      "changed_traits": {{}}
    }}
    """

    user_conversations[user_id].append(
        {"role": "system", "content": dynamic_system_prompt}
    )
    user_conversations[user_id].append(
        {"role": "user", "content": f"這是你的背景故事：{background_story}"}
    )

    print(f"已設定 {user_id} 的背景故事:\n{traits}")


def chat_with_ai(companion: Companion, user_input: str):
    """
    Sends user_input to OpenAI, parses the response, updates the dynamic traits if needed.
    Returns a 'Message'-like dictionary (without createdAt).
    """
    user_id = companion.userId
    if user_id not in user_conversations:
        raise ValueError(
            "尚未設定該 companion 的背景故事！(未呼叫 setup_background_story?)"
        )

    # Add user's message
    user_conversations[user_id].append({"role": "user", "content": user_input})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=user_conversations[user_id],
            temperature=0.8,
            max_tokens=300,
        )
    except openai.error.OpenAIError as e:
        print(f"OpenAI API 發生錯誤: {e}")
        return {"error": "API error"}

    ai_response = response["choices"][0]["message"]["content"]
    # Store the AI message in conversation history
    user_conversations[user_id].append({"role": "assistant", "content": ai_response})

    # Parse the JSON from the AI
    motion_key = "idle"
    try:
        ai_data = eval(ai_response)  # or json.loads if you expect perfect JSON
        motion_key = ai_data.get("pose_key", "idle")

        changed_traits = ai_data.get("changed_traits", {})
        if changed_traits:
            print("\n[DEBUG] 偵測到 changed_traits:\n", changed_traits)
            if "role" in changed_traits:
                companion_states[user_id]["role"] = changed_traits["role"]
            if "personality" in changed_traits:
                companion_states[user_id]["personality"] = changed_traits["personality"]
            if "communication_style" in changed_traits:
                companion_states[user_id]["communication_style"] = changed_traits[
                    "communication_style"
                ]
            if "emotional_response" in changed_traits:
                companion_states[user_id]["emotional_response"] = changed_traits[
                    "emotional_response"
                ]

            print("[DEBUG] 更新後的 companion_states:", companion_states[user_id])

    except (SyntaxError, KeyError) as err:
        print(f"[DEBUG] 回應解析時發生錯誤: {err}")
        motion_key = "idle"

    print(f"選擇的動作鍵：{motion_key}")

    # Lookup the motion and expression from our external JSON file
    motion_data = MOTION_MAPPING.get(
        motion_key,
        {
            "motion": "motions/relax.motion3.json",
            "expression": "expressions/idle.exp3.json",
        },
    )

    # Construct a "Message"-like return (no createdAt here).
    final_message = {
        "role": "assistant",  # openai chat role
        "motion": motion_data["motion"],
        "expression": motion_data["expression"],
        # This field references the entire "Companion" if you want, or you can store userId:
        # "companion": companion.dict()  # if you want to attach the entire companion object
        "content": ai_data.get("text_response", "抱歉，出現未知錯誤。"),
        "inStoryRole": companion_states[user_id]["role"],
        "personality": companion_states[user_id]["personality"],
        "communicationStyle": companion_states[user_id]["communication_style"],
        "emotionalResponse": companion_states[user_id]["emotional_response"],
    }

    print("最終訊息:", final_message)
    return final_message


# Example --> 你等会儿删掉这个就行，只是测试用的
if __name__ == "__main__":

    # Example: create a companion with prompt/backstory
    companion = Companion(
        userId="user_999",
        prompt={
            "backstory": "她來自一個貧困的家庭，極度缺乏自信，也沒有其他朋友，只有使用者。她非常渴望愛。"
        },
    )

    setup_background_story(companion)

    while True:
        user_input = input("你: ")
        if user_input.lower() in ["exit", "quit"]:
            print("結束對話。")
            break

        final_msg = chat_with_ai(companion, user_input)
        print("\n[回應訊息]", final_msg)
        print("\n你可以繼續對話，或輸入 'exit' 離開。\n")
