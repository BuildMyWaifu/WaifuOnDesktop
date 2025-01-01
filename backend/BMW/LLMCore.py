import os
import openai
import time
import uuid

# 設定你的 OpenAI API 金鑰
openai.api_key = os.environ["OPENAI_KEY"]

# -------------------------------------------------------------------------
# 存放每個 companion_id 的角色資料（角色、個性、溝通風格、情感回應）。
# -------------------------------------------------------------------------
companion_states = {}  
# 結構範例：
# companion_states = {
#   "companion_12345": {
#       "role": "companion",
#       "personality": "...",
#       "communication_style": "...",
#       "emotional_response": "..."
#   }
# }

# 定義系統提示：用來產生初始背景故事的人格特質
system_prompt = (
    """
    你是一個虛擬 AI 夥伴，會根據「使用者提供的背景故事」和「當前對話」來跟使用者聊天。
    請不要直白地提及背景故事的細節，而是將它內化，用來塑造你的個性與回應。
    
    每次回應都需要：
    1. 「text_response」：根據你的角色設定與使用者的訊息，進行自然、有個性的回覆。
    2. 「pose_key」：為下列之一，用於 Live2D 動作與表情：
    - happy_smile
    - nervous_smile
    - shy
    - sad
    - surprised
    - angry
    - confident
    - mischievous
    - confused
    - idle
    - attracted
    - none

    請僅用以下 JSON 格式回應：
    {{
    "text_response": "...",
    "pose_key": "..."
    }}

    """
)

# 動作與表情的對應表，用於 Live2D
MOTION_MAPPING = {
    "happy_smile": {
        "motion": "motions/wink.motion3.json",
        "expression": "expressions/smile.exp3.json"
    },
    "nervous_smile": {
        "motion": "motions/look_away.motion3.json",
        "expression": "expressions/blush.exp3.json"
    },
    "shy": {
        "motion": "motions/relax.motion3.json",
        "expression": "expressions/blush.exp3.json"
    },
    "sad": {
        "motion": "motions/heart_fail.motion3.json",
        "expression": "expressions/sad.exp3.json"
    },
    "surprised": {
        "motion": "motions/react_big.motion3.json",
        "expression": "expressions/shock.exp3.json"
    },
    "angry": {
        "motion": "motions/react_big.motion3.json",
        "expression": "expressions/angry.exp3.json"
    },
    "confident": {
        "motion": "motions/level_up.motion3.json",
        "expression": "expressions/confident.exp3.json"
    },
    "mischievous": {
        "motion": "motions/react_small.motion3.json",
        "expression": "expressions/mischievous.exp3.json"
    },
    "confused": {
        "motion": "motions/look_away.motion3.json",
        "expression": "expressions/confuse.exp3.json"
    },
    "idle": {
        "motion": "motions/relax.motion3.json",
        "expression": "expressions/idle.exp3.json"
    },
    "attracted": {
        "motion": "motions/heart_success.motion3.json",
        "expression": "expressions/attract.exp3.json"
    }
}

# 用於儲存每個 companion 的對話紀錄
user_conversations = {}

def generate_traits(background_story):
    """
    呼叫 OpenAI 產生（個性、溝通風格、情感回應）等初始設定。
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
            max_tokens=200
        )
        traits = response['choices'][0]['message']['content']
        print("產生的個性特徵:\n", traits)  # 除錯用
        return traits
    except openai.error.OpenAIError as e:
        print(f"產生個性特徵時發生錯誤: {e}")
        return "產生個性特徵失敗，請再試一次。"

def setup_background_story(companion_id, background_story):
    """
    設定背景故事，並更新對應的 companion_states 與對話內容。
    """
    if companion_id not in user_conversations:
        user_conversations[companion_id] = []
    
    # 如果尚未建立 companion 狀態，初始化
    if companion_id not in companion_states:
        companion_states[companion_id] = {
            "role": "companion",  # 預設為 companion
            "personality": "",
            "communication_style": "",
            "emotional_response": ""
        }

    # 先透過 generate_traits 取得初始的個性資訊
    traits = generate_traits(background_story)

    # 簡易解析行為，將三種特徵存到 companion_states
    lines = traits.splitlines()
    for line in lines:
        if line.lower().startswith("- personality:"):
            companion_states[companion_id]["personality"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("- communication style:"):
            companion_states[companion_id]["communication_style"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("- emotional response:"):
            companion_states[companion_id]["emotional_response"] = line.split(":", 1)[1].strip()

    # 系統提示（system_prompt）內容，強調如果角色特徵需要改變，必須在 JSON 加入 changed_traits
    dynamic_system_prompt = f"""
    你是一個虛擬 AI 夥伴，正在和剛認識的夥伴對話。
    - 你不是一般的「助理」，請避免客服式或正式的回答，例如「How can I assist you?」。
    - 請維持角色設定：不要透露自己是 AI，也避免使用「如何幫你」之類的字句。
    - 請勿使用「How may I help you?」或「How can I assist you today?」等句子。

    目前的角色屬性（之後可能會在對話中演變）：
    role: {companion_states[companion_id]["role"]}
    personality: {companion_states[companion_id]["personality"]}
    communication style: {companion_states[companion_id]["communication_style"]}
    emotional response: {companion_states[companion_id]["emotional_response"]}

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
    2. pose_key：對應以下 Live2D 動作：
       - happy_smile
       - nervous_smile
       - shy
       - sad
       - surprised
       - angry
       - confident
       - mischievous
       - confused
       - idle
       - attracted
       - none

    嚴格遵守以下 JSON 格式回應：
    {{
      "text_response": "...",
      "pose_key": "...",
      "changed_traits": {{}}  // 如果有變化才加
    }}
    """

    # 把系統提示與「背景故事」加到對話中
    user_conversations[companion_id].append({"role": "system", "content": dynamic_system_prompt})
    user_conversations[companion_id].append({"role": "user", "content": f"這是你的背景故事：{background_story}"})

    print(f"已設定 {companion_id} 的背景故事:\n{traits}")

def chat_with_ai(companion_id, user_input):
    """
    接收使用者輸入、送到 OpenAI，並處理回應（包含 changed_traits）。
    """
    if companion_id not in user_conversations:
        raise ValueError("尚未設定該 companion 的背景故事！")

    # 把使用者的輸入加入對話紀錄
    user_conversations[companion_id].append({"role": "user", "content": user_input})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=user_conversations[companion_id],
            temperature=0.8,
            max_tokens=300
        )
    except openai.error.OpenAIError as e:
        print(f"OpenAI API 發生錯誤: {e}")
        return {"error": "API error"}

    ai_response = response['choices'][0]['message']['content']
    # 將 AI 回應寫進對話紀錄
    user_conversations[companion_id].append({"role": "assistant", "content": ai_response})

    try:
        # 嘗試解析 AI 的回應（JSON 格式）
        ai_data = eval(ai_response)

        # 如果 AI 回應沒有 pose_key，就預設用 "idle"
        motion_key = ai_data.get("pose_key", "idle")

        # 檢查是否有 changed_traits
        changed_traits = ai_data.get("changed_traits", None)
        if changed_traits:
            print("\n[DEBUG] 偵測到 changed_traits:\n", changed_traits)
            # 如果有變更，就更新 companion_states
            role_changed = changed_traits.get("role")
            if role_changed:
                companion_states[companion_id]["role"] = role_changed
            
            personality_changed = changed_traits.get("personality")
            if personality_changed:
                companion_states[companion_id]["personality"] = personality_changed

            comm_style_changed = changed_traits.get("communication_style")
            if comm_style_changed:
                companion_states[companion_id]["communication_style"] = comm_style_changed

            emotional_resp_changed = changed_traits.get("emotional_response")
            if emotional_resp_changed:
                companion_states[companion_id]["emotional_response"] = emotional_resp_changed

            print("[DEBUG] 更新後的 companion_states:", companion_states[companion_id])
    except (SyntaxError, KeyError) as err:
        print(f"[DEBUG] 回應解析時發生錯誤: {err}")
        motion_key = "idle"

    print(f"選擇的動作鍵：{motion_key}")

    # 根據 pose_key 找出對應的 motion/表情
    motion_data = MOTION_MAPPING.get(motion_key, {
        "motion": "motions/relax.motion3.json",
        "expression": "expressions/idle.exp3.json"
    })

    # 建立最終要回傳的訊息
    created_at = int(time.time() * 1000)
    final_message = {
        "_id": str(uuid.uuid4()),
        # 這裡的 role 指的是 OpenAI 的對話角色（assistant），跟 inStoryRole 不同
        "role": "assistant",
        "motion": motion_data["motion"],
        "expression": motion_data["expression"],
        "companionId": companion_id,
        "content": ai_data.get("text_response", "抱歉，出現未知錯誤。"),
        "createdAt": created_at,

        # 加入故事內的角色屬性，供後端儲存
        "inStoryRole": companion_states[companion_id]["role"],
        "personality": companion_states[companion_id]["personality"],
        "communicationStyle": companion_states[companion_id]["communication_style"],
        "emotionalResponse": companion_states[companion_id]["emotional_response"]
    }

    print("最終訊息:", final_message)
    return final_message


# 以下為示範用程式的進入點
if __name__ == "__main__":
    companion_id = "companion_12345"
    setup_background_story(companion_id, "她來自一個貧困的家庭，極度缺乏自信，也沒有其他朋友，只有使用者。她非常渴望愛。")

    while True:
        user_input = input("你: ")
        if user_input.lower() in ["exit", "quit"]:
            print("結束對話。")
            break
        
        final_message = chat_with_ai(companion_id, user_input)
        
        # 這裡可以再做下一步處理，例如：顯示 Live2D 動畫、儲存到後端等
        print("\n你可以繼續對話，或輸入 'exit' 離開。\n")
