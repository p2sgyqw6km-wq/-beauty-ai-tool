import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

# ---------------------- 直接在这里填你的百度密钥，不用配置Secrets ----------------------
API_KEY = "KSD4YiH1a7CipcseQHwQmObH"
SECRET_KEY = "8JnJNnoXD7o9aZxlAL52rfyr6aRyelIx"
UNLOCK_PASSWORD = "123456"

# ---------------------- 获取Access Token ----------------------
@st.cache_resource(show_spinner=False)
def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    response = requests.post(url, params=params)
    return response.json()["access_token"]

# ---------------------- 人体关键点检测接口 ----------------------
def detect_pose(image_bytes):
    access_token = get_access_token()
    url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_analysis"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"image": base64.b64encode(image_bytes).decode("utf-8")}
    params = {"access_token": access_token}
    response = requests.post(url, headers=headers, params=params, data=data)
    return response.json()

# ---------------------- 人脸检测与属性分析接口 ----------------------
def detect_face(image_bytes):
    access_token = get_access_token()
    url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "image": base64.b64encode(image_bytes).decode("utf-8"),
        "image_type": "BASE64",
        "face_field": "age,gender,skin_status,quality,emotion,face_shape"
    }
    params = {"access_token": access_token}
    response = requests.post(url, headers=headers, params=params, data=data)
    return response.json()

# ---------------------- 页面配置与样式 ----------------------
st.set_page_config(
    page_title="AI体态&变美方案定制",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# ---------------------- 侧边栏导航 ----------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3204/3204123.png", width=100)
    st.title("AI体态&变美方案")
    page = st.radio("选择功能", ["首页", "🏋️ 健身动作AI纠错", "🧴 人脸美白方案", "💎 会员说明"])
    st.markdown("---")
    st.caption("© 2026 AI体态变美 | 仅作日常参考，不替代医疗建议")

# ---------------------- 解锁逻辑 ----------------------
if "unlocked" not in st.session_state:
    st.session_state.unlocked = False

def check_password():
    if st.session_state.password_input == UNLOCK_PASSWORD:
        st.session_state.unlocked = True
        st.success("✅ 解锁成功！")
        st.rerun()
    else:
        st.error("❌ 密码错误，请重试")

# ---------------------- 首页 ----------------------
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

# ---------------------- 健身动作AI纠错 ----------------------
elif page == "🏋️ 健身动作AI纠错":
    st.title("🏋️ 健身动作AI纠错")
    st.markdown("上传你的健身动作照片，AI帮你分析骨骼关键点，快速发现姿势问题")
    st.markdown("---")

    if not st.session_state.unlocked:
        st.warning("🔒 此功能需要解锁完整版方案")
        st.text_input("请输入解锁密码", type="password", key="password_input")
        st.button("验证密码解锁完整版", on_click=check_password)
    else:
        uploaded_file = st.file_uploader("上传你的健身动作照片", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image_bytes = uploaded_file.read()
            image = Image.open(BytesIO(image_bytes))
            col1, col2 = st.columns(2)
            with col1:
                st.image(image, caption="你的原始动作", width=300)
            with col2:
                with st.spinner("AI正在分析你的动作..."):
                    pose_result = detect_pose(image_bytes)
                    st.image(image, caption="AI骨骼分析结果（接口已对接，可在后台查看返回数据）", width=300)
                    st.success("✅ 动作分析完成！")
                    st.json(pose_result, expanded=False)

# ---------------------- 人脸美白方案 ----------------------
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
            image_bytes = uploaded_file.read()
            image = Image.open(BytesIO(image_bytes))
            st.image(image, caption="你的照片", width=400)
            with st.spinner("AI正在分析你的肤质..."):
                face_result = detect_face(image_bytes)
                st.success("✅ 肤质分析完成！")
                st.json(face_result, expanded=False)

# ---------------------- 会员说明 ----------------------
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
