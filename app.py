import streamlit as st

# 全局配置
st.set_page_config(
    page_title="AI体态&变美方案定制",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 隐藏默认控件 + 美化样式
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stButton>button {width:100%; background-color:#4a6cf7; color:white; border-radius:8px; padding:0.75rem; font-weight:bold;}
.stButton>button:hover {background-color:#3a5ce7;}
.card {padding:1.5rem; border-radius:1rem; background:#f8f9fa; box-shadow:0 4px 12px rgba(0,0,0,0.05); margin-bottom:1rem;}
</style>
""", unsafe_allow_html=True)

# 侧边栏导航
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3204/3204123.png", width=100)
    st.title("AI体态&变美方案")
    page = st.radio("选择功能", ["首页", "🏋️ 健身动作AI纠错", "🧴 人脸美白方案", "💎 会员说明"])
    st.markdown("---")
    st.caption("© 2026 AI体态变美 | 仅作日常参考，不替代医疗建议")

# 初始化session
if "step" not in st.session_state:
    st.session_state.step = 1
if "unlocked" not in st.session_state:
    st.session_state.unlocked = False

# 密码验证逻辑
def check_password():
    if st.session_state.password_input == st.secrets["UNLOCK_PASSWORD"]:
        st.session_state.unlocked = True
        st.success("✅ 解锁成功！")
        st.rerun()
    else:
        st.error("❌ 密码错误，请重试")

# 首页
if page == "首页":
    st.title("✨ 你的专属AI体态&变美方案")
    st.subheader("上传动作/自拍，AI为你定制专属指导")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="card">
            <h3>🏋️ 健身动作AI纠错</h3>
            <p>上传深蹲/硬拉/体态照片，AI骨骼识别+标准动作对比，纠正姿势问题</p >
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card">
            <h3>🧴 人脸美白方案定制</h3>
            <p>上传自拍，AI分析肤质/痘痘/暗沉，生成专属美白+护肤计划</p >
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h3>💎 解锁完整服务</h3>
        <p>一次性解锁价：9.9元，即可获取：</p >
        <ul>
            <li>✅ 健身动作高清对比纠错</li>
            <li>✅ 人脸肤质详细报告+美白方案</li>
            <li>✅ 可下载的完整PDF报告</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# 健身动作AI纠错页面
elif page == "🏋️ 健身动作AI纠错":
    st.title("🏋️ 健身动作AI纠错")
    st.markdown("上传你的健身动作照片，AI帮你对比标准动作，找出姿势问题")
    st.markdown("---")

    if not st.session_state.unlocked:
        st.warning("🔒 此功能需要解锁完整版方案")
        st.text_input("请输入解锁密码", type="password", key="password_input")
        st.button("验证密码解锁完整版", on_click=check_password)
    else:
        uploaded_file = st.file_uploader("上传你的健身动作照片", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            st.image(uploaded_file, caption="你的动作", width=400)
            st.info("AI姿态识别功能正在开发中，解锁后将生成骨骼对比图和纠错指导")

# 人脸美白方案定制页面
elif page == "🧴 人脸美白方案":
    st.title("🧴 人脸美白方案定制")
    st.markdown("上传你的正面自拍，AI分析肤质，生成专属美白护肤计划")
    st.markdown("---")

    if not st.session_state.unlocked:
        st.warning("🔒 此功能需要解锁完整版方案")
        st.text_input("请输入解锁密码", type="password", key="password_input")
        st.button("验证密码解锁完整版", on_click=check_password)
    else:
        uploaded_file = st.file_uploader("上传你的正面自拍", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            st.image(uploaded_file, caption="你的照片", width=400)
            st.info("AI肤质分析功能正在开发中，解锁后将生成肤质报告和美白方案")

# 会员说明页面
elif page == "💎 会员说明":
    st.title("💎 会员服务说明")
    st.markdown("---")
    st.markdown("""
    <div class="card">
        <h3>一次性解锁服务</h3>
        <p>解锁价：9.9元</p >
        <ul>
            <li>✅ 健身动作AI骨骼识别+标准动作对比纠错</li>
            <li>✅ 人脸自拍肤质检测+美白护肤方案</li>
            <li>✅ 可下载的完整PDF报告</li>
            <li>✅ 无广告，永久使用当前版本功能</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
