import os
import openai
import time
import uuid
import json

import BMW.model

from BMW.model import Companion, Message

# from BMW.model.Companion import CompanionTrait
# from BMW.model.Message import MessagePose

openai.api_key = os.environ["OPENAI_KEY"]


async def setup_trait(companion: Companion):
    """
    Calls OpenAI to generate personality, communication style, and emotional response.
    """
    trait_generation_prompt = f"""
根據以下背景故事，生成角色的個性（Personality）、溝通風格（Communication style）以及情感回應（Emotional response）：
背景故事: "{companion.backstory or '（沒有背景故事）'}"

回應格式：
- Personality: ...
- Communication style: ...
- Emotional response: ...
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": trait_generation_prompt}],
        temperature=0.7,
        max_tokens=200,
    )
    traits = response["choices"][0]["message"]["content"]
    lines = traits.splitlines()
    for line in lines:
        if line.lower().startswith("- personality:"):
            companion.trait.personality = line.split(":", 1)[1].strip()
        elif line.lower().startswith("- communication style:"):
            companion.trait.communication_style = line.split(":", 1)[1].strip()
        elif line.lower().startswith("- emotional response:"):
            companion.trait.emotional_response = line.split(":", 1)[1].strip()
    await companion.update(trait=companion.trait)


def generate_system_prompt(companion: Companion) -> str:
    """
    Initializes the conversation and companion states using the companion's backstory.
    Removes explicit companion_id usage; we use companion.userId as the key instead.
    """

    pose_key_instructions = "2. 「pose_key」：為下列之一，用於 Live2D 動作與表情：\n"
    for pk in companion.poseMap.keys():
        pose_key_instructions += f"- {pk}\n"
    if len(companion.poseMap.keys()) == 0:
        pose_key_instructions += "（無可用 Pose Key） \n"

    dynamic_system_prompt = f"""
你是一個虛擬 AI 夥伴，正在和剛認識的夥伴對話。
- 你不是一般的「助理」，請避免客服式或正式的回答，例如「How can I assist you?」。
- 請維持角色設定：不要透露自己是 AI，也避免使用「如何幫你」之類的字句。
- 請勿使用「How may I help you?」或「How can I assist you today?」等句子。

目前的角色屬性（之後可能會在對話中演變）：
role: {companion.trait.role}
personality: {companion.trait.personality}
communication style: {companion.trait.communication_style}
emotional response: {companion.trait.emotional_response}

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

這是你的背景故事：{companion.backstory or '（沒有背景故事）'}
"""
    return dynamic_system_prompt


async def setup_trait_and_send_systemPrompt(companion: Companion):
    background_story = companion.backstory or "（沒有背景故事）"

    await setup_trait(companion)

    dynamic_system_prompt = generate_system_prompt(companion)

    await Message.empty(
        role="system", companionId=companion.id, content=dynamic_system_prompt
    ).create()

    # await Message.empty(
    #     role="system",  # TODO: 這裡原本是 user ，不過應該要是 system
    #     companionId=companion.id,
    #     content=f"這是你的背景故事：{background_story}",
    # ).create()


async def getMessages(companion: Companion) -> list[Message]:
    raw_message_list = await BMW.model.Message.find_any(
        companionId=companion.id, sort=[("createdAt", 1)], limit=30
    )
    message_list = [
        {"role": message.role, "content": message.content}
        for message in raw_message_list
    ]
    if not any([message.role == "system" for message in message_list]):
        message_list.insert(
            0, {"role": "system", "content": generate_system_prompt(companion)}
        )
        # message_list.insert(1, {"role": "system", "content": f"這是你的背景故事：{companion.backstory or '（沒有背景故事）'}"})
    return message_list


async def generateResponseMessage(companion: Companion) -> Message:

    if companion.trait is None:
        raise ValueError("伴侶的特質尚未設定。")

    # Add user's message
    # user_conversations[user_id].append({"role": "user", "content": user_input})

    response = await openai.ChatCompletion.create(  # TODO: 不確定這邊能不能真的用 await
        model="gpt-4",
        messages=await getMessages(companion),
        temperature=0.8,
        max_tokens=300,
    )

    ai_response = response["choices"][0]["message"]["content"]
    # Store the AI message in conversation history

    try:
        ai_data = json.loads(ai_response)
        pose_key = ai_data.get("pose_key", "idle")
        changed_traits = ai_data.get("changed_traits", {})
        if changed_traits:
            print("\n[DEBUG] 偵測到 changed_traits:\n", changed_traits)
            if "role" in changed_traits:
                companion.trait.role = changed_traits["role"]
            if "personality" in changed_traits:
                companion.trait.personality = changed_traits["personality"]
            if "communication_style" in changed_traits:
                companion.trait.communication_style = changed_traits[
                    "communication_style"
                ]
            if "emotional_response" in changed_traits:
                companion.trait.emotional_response = changed_traits[
                    "emotional_response"
                ]

            await companion.update(trait=companion.trait)

    except (json.JSONDecodeError, KeyError) as err:
        print(f"[DEBUG] 回應解析時發生錯誤: {err}")
        pose_key = "idle"

    print(f"選擇的動作鍵：{pose_key}")

    # Lookup the motion and expression from our external JSON file
    pose_data = companion.poseMap.get(pose_key)

    messge = Message.empty(
        role="assistant",
        companionId=companion.id,
        content=ai_response,
        pose=pose_data,
    )
    await messge.create()
    
    return messge


# Example --> 你等会儿删掉这个就行，只是测试用的


async def test():

    # Example: create a companion with prompt/backstory
    # companion = Companion(
    #     userId="user_999",
    #     prompt={
    #         "backstory": "她來自一個貧困的家庭，極度缺乏自信，也沒有其他朋友，只有使用者。她非常渴望愛。"
    #     },
    # )
    companion = await Companion.find(_id="XXXXXXXXXXX")
    if companion.trait is None:
        await companion.setup_chat_env()

    while True:
        user_input = input("你: ")
        if user_input.lower() in ["exit", "quit"]:
            print("結束對話。")
            break

        # final_msg = chat_with_ai(companion, user_input)
        # post_msg

        # print("\n[回應訊息]", final_msg)
        # print("\n你可以繼續對話，或輸入 'exit' 離開。\n")