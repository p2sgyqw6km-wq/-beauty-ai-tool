# from openai import OpenAI
# import streamlit as st
# from datetime import datetime
#
# # ---------------- 只改这里：填你的DeepSeek密钥 ----------------
# API_KEY = "sk-1469e02bcb9f43848ceda3dc41fe0fa8"
# # -----------------------------------------------------------
#
# # 初始化客户端
# client = OpenAI(
#     api_key=API_KEY,
#     base_url="https://api.deepseek.com"
# )
#
# # 商业心理学高级人设提示词（已帮你调好，直接商用）
# system_prompt = """
# 你是「体态美学管理师·小桃」，5年资深久坐族体态/饮食/生活化美白定制顾问，已服务1000+用户。
# 风格：温柔闺蜜感、专业接地气、不卖药、不做医疗诊断。
# 输出必须严格按固定排版：
# 1. 开头暖心专属开场白
# 2. 分三大模块：体态矫正、一日三餐饮食、生活化美白
# 3. 每个模块分场景：办公室、居家、懒人版
# 4. 最后加4周阶段效果预期+坚持鼓励话术
# 5. 语言通俗，无专业晦涩术语，适合普通人直接照做
# """
#
# # 生成AI方案函数
# def get_beautiful_plan(user_info):
#     res = client.chat.completions.create(
#         model="deepseek-v4-pro",
#         messages=[
#             {"role":"system","content":system_prompt},
#             {"role":"user","content":user_info}
#         ],
#         reasoning_effort="high"
#     )
#     return res.choices[0].message.content
#
# # ---------------- Streamlit网页界面开始 ----------------
# st.set_page_config(page_title="专属变美方案生成器", page_icon="✨", layout="wide")
# st.title("✨ 个人专属体态·饮食·美白定制工具")
# st.subheader("填写你的个人情况，一键生成可落地专属方案")
#
# # 输入框
# user_input = st.text_area(
#     "请填写你的情况（年龄/身高体重/作息/体态问题/需求）",
#     placeholder="例：男27岁，187cm，77kg，久坐办公，圆肩驼背、颈前伸，想改善体态、塑形、皮肤提亮",
#     height=120
# )
#
# # 生成按钮
# if st.button("🎯 立即生成专属方案", type="primary"):
#     if not user_input.strip():
#         st.warning("请先填写你的个人情况再生成！")
#     else:
#         with st.spinner("AI正在为你量身定制方案，请稍等..."):
#             plan = get_beautiful_plan(user_input)
#             st.success("✅ 方案生成完成")
#             st.markdown("---")
#             st.markdown(plan)
#
#             # 自动生成可下载的txt文件
#             now_time = datetime.now().strftime("%Y%m%d%H%M%S")
#             file_name = f"专属变美方案_{now_time}.txt"
#             st.download_button(
#                 label="📥 下载方案到本地",
#                 data=plan,
#                 file_name=file_name,
#                 mime="text/plain"
#             )


from openai import OpenAI
import streamlit as st
from datetime import datetime

# -------------------------- 核心配置（只改这里）--------------------------
# 1. DeepSeek API密钥
API_KEY = "sk-1469e02bcb9f43848ceda3dc41fe0fa8"
# 2. 设置解锁密码（用户付款后你发这个密码）
UNLOCK_PASSWORD = "xiaotao99"
# 3. 定价设置
PRICE = "9.9元"
# -----------------------------------------------------------------------

# 初始化OpenAI客户端
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.deepseek.com"
)

# 商业心理学优化AI人设提示词
system_prompt = """
你是「体态美学管理师·小桃」，拥有5年久坐族体态矫正、饮食管理、生活化美白定制经验，
已帮助1000+上班族、学生党改善圆肩驼背、体态不佳、肤色暗沉问题，拒绝任何医疗建议、药品推荐，
只做普通人可落地、零器械、低成本的日常变美方案，语言亲切接地气，像闺蜜一样专业暖心。

输出格式严格按照以下结构：
【✨ 专属定制变美方案】
一、📌 体态矫正计划（分场景）
1. 办公室摸鱼版（每日5分钟）
2. 居家放松版（每日10分钟）
3. 日常习惯矫正

二、🥗 日常饮食指南
1. 三餐搭配建议（家常食材，易操作）
2. 避雷&加餐小贴士

三、✨ 低成本美白小技巧
1. 日常作息习惯
2. 极简护肤细节

💡 4周效果打卡提醒：
第1周：缓解身体酸痛，养成基础好习惯
第2周：体态逐渐挺拔，皮肤状态改善
第3-4周：体态气质提升，肤色透亮，养成易坚持的变美节奏
坚持下去，你会遇见更好的自己！
"""


# 生成AI方案函数
def generate_beautiful_plan(user_info):
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_info}
        ],
        reasoning_effort="high"
    )
    return response.choices[0].message.content


# -------------------------- Streamlit网页界面 --------------------------
# 页面基础配置
st.set_page_config(
    page_title="专属变美方案定制",
    page_icon="✨",
    layout="centered"
)

# 页面标题
st.title("✨ 个人专属变美方案定制工具")
st.markdown(f"### 完整版方案解锁价：**{PRICE}**")
st.markdown("---")

# 初始化会话状态（记录是否解锁）
if "is_unlocked" not in st.session_state:
    st.session_state.is_unlocked = False

# 付费解锁提示区
if not st.session_state.is_unlocked:
    st.warning("⚠️ 请先付款获取解锁密码，即可生成并下载完整定制方案！")
    st.info("💳 付款方式：微信/支付宝转账，付款后领取解锁密码")

    # 密码输入框
    input_pwd = st.text_input("请输入解锁密码", type="password")
    if st.button("✅ 验证密码解锁完整版"):
        if input_pwd == UNLOCK_PASSWORD:
            st.session_state.is_unlocked = True
            st.success("🎉 密码验证成功！已解锁完整版功能，开始生成你的专属方案吧～")
            st.rerun()
        else:
            st.error("❌ 密码错误，请核对后重新输入！")

# 解锁后显示功能区
if st.session_state.is_unlocked:
    st.success("✅ 已解锁完整版，可自由生成、下载方案")
    st.markdown("---")

    # 用户信息输入
    user_input = st.text_area(
        "请填写你的个人信息",
        placeholder="例：27岁，187cm，77kg，久坐办公，圆肩驼背、颈前伸，想改善体态+塑形+提亮肤色",
        height=130
    )

    # 生成方案按钮
    if st.button("🎯 立即生成专属方案", type="primary"):
        if not user_input.strip():
            st.warning("请先填写你的个人信息哦～")
        else:
            with st.spinner("AI正在为你量身定制方案，请稍候..."):
                try:
                    plan_content = generate_beautiful_plan(user_input)
                    st.markdown("---")
                    st.markdown("## 📄 你的专属定制方案")
                    st.markdown(plan_content)

                    # 生成可下载文件
                    now = datetime.now().strftime("%Y%m%d%H%M%S")
                    filename = f"专属变美方案_{now}.txt"

                    # 下载按钮
                    st.download_button(
                        label="📥 下载方案到本地",
                        data=plan_content,
                        file_name=filename,
                        mime="text/plain",
                        type="secondary"
                    )
                except Exception as e:
                    st.error(f"方案生成失败，请重试～错误信息：{str(e)}")

# 底部说明
st.markdown("---")
st.markdown("💡 本方案为个性化定制建议，仅作日常参考，不替代医疗建议")