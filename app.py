import pandas as pd
import datetime
from rapidfuzz import process, fuzz
import streamlit as st

# 1. INITIALIZE DATABASE WITH GENDER & PROFILE PICTURES
if 'directory_df' not in st.session_state:
    data = {
        'id': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
        'photo': [
            'https://m.media-amazon.com/images/M/MV5BMjAzNzA1MzM4M15BMl5BanBnXkFtZTcwMjgzODgxNw@@._V1_.jpg', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-pEvonrkLzJKKFg5xc5KKX2XuNfkIApZK2w&s',
            'https://m.media-amazon.com/images/M/MV5BMjU4Mzc0YmQtYzlkNy00ZjJkLWE2NDktZmM1OWZmOTAyOTBlXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg', 'https://image.cdn2.seaart.me/temp-convert-webp/jpeg/static/28547a00a3740aafdd6ae8dd8a00e0de/1698515296963/c3cdbe72a65e35634318c289a1cf1019_low.webp',
            'https://upload.wikimedia.org/wikipedia/commons/8/8f/Danny_Dong_%28cropped%29.jpg', 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Lana_Rhoades_2-2017_%28cropped%29.jpg/960px-Lana_Rhoades_2-2017_%28cropped%29.jpg',
            'https://scontent.fmnl40-1.fna.fbcdn.net/v/t39.30808-6/614897441_4292996384348260_6618392344529007694_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=1d70fc&_nc_eui2=AeGqntBuz1sLQQ1GbjMRfGy-DJDz5QJROb4MkPPlAlE5vvGuDp48Aublxv54sA9kOicBYGdr5yPV96JGzz3HNaye&_nc_ohc=gklby9BdOXsQ7kNvwHGteEY&_nc_oc=AdpWsheKyIjQZ2sw_toHqye_0QJ8po2sWH45yqlcyewTwJb5OAHMV8tzd7DTzOJLLNI&_nc_zt=23&_nc_ht=scontent.fmnl40-1.fna&_nc_gid=XP_r2RlHljCVj1RX3QKDOw&_nc_ss=7b2a8&oh=00_Af6IKk5WdvSxj3UVz157hONNC0uFRHZjg7GSqRc4CqhgDQ&oe=6A063915', 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Jenna_Jameson_2_2008.jpg/250px-Jenna_Jameson_2_2008.jpg',
            'https://scontent.fmnl40-2.fna.fbcdn.net/v/t39.30808-6/678587392_3026550077699027_9085505371686294498_n.jpg?stp=cp6_dst-jpg_tt6&_nc_cat=110&ccb=1-7&_nc_sid=1d70fc&_nc_eui2=AeHQoXNEdxOJsxnLRGSJCG9h4FKk5Ghepl7gUqTkaF6mXp2POF579RIcpiw8dY_YfykQ1zh7t6FqMWGbURDjSfpA&_nc_ohc=9PAuY09SwPgQ7kNvwHiSgtN&_nc_oc=Adp2uii6ZI0ct8n_Z3Q7afQihD5BOYD_FeymW3nDWC5Vh-3Zb4D4Gpn6xOkVqZtYAyA&_nc_zt=23&_nc_ht=scontent.fmnl40-2.fna&_nc_gid=-1OXCBcyybc2j129_RbFFA&_nc_ss=7b2a8&oh=00_Af4oZiCTurLoWv7mDRL_JShfVdS10tdYY5PnCjN9pgHYSg&oe=6A0658B0', 'https://hips.hearstapps.com/hmg-prod/images/white-kiawentiio-shot-01-2189-65e8c9b2dd3c3.jpg?crop=1.00xw:0.668xh;0,0&resize=1200:*'
        ],
        'name': [
            'Sasha Grey', 'Johnny Sins', 'Jordi El Niño Pollo', 'Mia Khalifa', 
            'Danny Dela Cruz', 'Lana Rhoades', 'Yuri Maverick Ibasco', 'Elena Vizconde',
            'Jeffrey Castañeda', 'Kiawenti:io Tarbell'
        ],
        'gender': [
            'Female', 'Male', 'Male', 'Female', 
            'Male', 'Female', 'Male', 'Female', 
            'Male', 'Female'
        ],
        'role': [
            'Faculty', 'Student', 'Staff', 'Faculty', 'Student', 
            'Student', 'Faculty', 'Staff', 'Student', 'Faculty'
        ],
        'email': [
            'm.santos@school.edu.ph', 'm.rivera@student.edu.ph', 'j.doe@admin.edu.ph', 
            'j.smith@school.edu.ph', 'j.delacruz@student.edu.ph', 'a.guo@student.edu.ph',
            'r.reyes@school.edu.ph', 'e.vizconde@admin.edu.ph', 'c.garcia@student.edu.ph',
            'b.luna@school.edu.ph'
        ],
        'phone': [
            '+63 917 123 4567', '+63 918 999 8888', '+63 922 444 5555', 
            '+63 915 111 2222', '+63 905 333 4444', '+63 916 555 6666',
            '+63 919 777 8888', '+63 927 222 3333', '+63 908 444 9999',
            '+63 912 888 7777'
        ],
        'department': [
            'IT', 'Engineering', 'Registrar', 'IT', 'Arts', 
            'Engineering', 'Science', 'Finance', 'IT', 'Science'
        ],
        'last_updated': [
            '2026-01-10', '2026-02-15', '2026-03-20', '2026-04-01', 
            '2025-12-30', '2026-05-01', '2026-04-15', '2025-11-05',
            '2026-05-08', '2026-05-09'
        ],
        'search_count': [54, 12, 43, 88, 15, 22, 31, 9, 67, 45]
    }
    st.session_state.directory_df = pd.DataFrame(data)

df = st.session_state.directory_df

# 2. UI STYLING & AVATAR CONFIG
st.set_page_config(page_title="School Portal | Directory", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #1a365d; color: white; }
    h1 { color: #1a365d; border-bottom: 2px solid #c53030; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; border-left: 5px solid #c53030; }
    
    [data-testid="stImage"] img {
        border-radius: 50%;
        border: 3px solid #1a365d;
        object-fit: cover;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. HELPER FUNCTIONS
def update_df(new_df):
    st.session_state.directory_df = new_df.reset_index(drop=True)
    st.rerun()

def intelligent_search(query, dataframe):
    if not query: return []
    names = dataframe['name'].tolist()
    matches = process.extract(query, names, scorer=fuzz.WRatio, limit=5)
    return [ {**dataframe.iloc[idx].to_dict(), 'confidence': round(score, 2)} for _, score, idx in matches if score > 45 ]

# 4. MAIN CONTENT
st.title("🏛️ University Information Directory")

tabs = st.tabs(["📊 Analytics Dashboard", "🔎 Smart Search", "📝 Record Entry", "🛠️ System Management"])

# --- TAB 1: DASHBOARD (Institutional Focus) ---
with tabs[0]:
    st.subheader("📈 Institutional Analytics")
    m1, m2, m3, m4 = st.columns(4)
    
    m1.metric("Total Population", len(df))
    m2.metric("Total Students", len(df[df['role'] == 'Student']))
    m3.metric("Total Faculty", len(df[df['role'] == 'Faculty']))
    m4.metric("Total Staff", len(df[df['role'] == 'Staff']))

    st.divider()
    
    st.write("### 🔍 Advanced Departmental Analysis")
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        role_filter = st.multiselect("Select Role(s):", options=df['role'].unique(), default=df['role'].unique())
    
    role_filtered_df = df[df['role'].isin(role_filter)]
    available_depts = role_filtered_df['department'].unique()

    with f_col2:
        dept_filter = st.multiselect("Filter by Department:", options=available_depts, default=available_depts)
    
    view_df = role_filtered_df[role_filtered_df['department'].isin(dept_filter)]

    col_chart1, col_chart2 = st.columns([2, 1])
    with col_chart1:
        st.write("#### 📊 Role Distribution")
        if not view_df.empty:
            st.bar_chart(view_df['role'].value_counts(), color="#1a365d")
    with col_chart2:
        st.write("#### 🏗️ Dept. Concentration")
        if not view_df.empty:
            dept_counts = view_df['department'].value_counts(normalize=True) * 100
            for dept, percent in dept_counts.items():
                st.write(f"**{dept}** ({percent:.1f}%)")
                st.progress(percent / 100)

    st.write("---")
    st.dataframe(view_df[['id', 'name', 'role', 'department', 'email', 'phone']], use_container_width=True, hide_index=True)

# --- TAB 2: SEARCH ENGINE (Profile View with Gender) ---
with tabs[1]:
    st.subheader("Intelligent Retrieval Engine")
    search_query = st.text_input("Search (Try typing names with typos or partials):")
    
    if search_query:
        results = intelligent_search(search_query, df)
        if results:
            for res in results:
                with st.container():
                    pic_col, info_col, match_col = st.columns([1, 4, 1])
                    with pic_col:
                        st.image(res['photo'], width=100)
                    with info_col:
                        st.markdown(f"#### {res['name']}")
                        # Gender included in Profile view
                        st.caption(f"👤 {res['gender']} | 📍 {res['department']} Dept | 🛡️ {res['role']}")
                        st.text(f"📧 {res['email']} | 📞 {res['phone']}")
                    with match_col:
                        st.progress(res['confidence'] / 100)
                        st.write(f"**Match: {res['confidence']}%**")
                    st.divider()
        else:
            st.warning("No records matched your search query.")

# --- TAB 3: REGISTRATION (Updated with Gender Selection) ---
with tabs[2]:
    st.subheader("New Entry Registration")
    with st.form("reg_form", clear_on_submit=True):
        f1, f2 = st.columns(2)
        with f1:
            name = st.text_input("Full Name")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            role = st.selectbox("Role", ["Student", "Faculty", "Staff"])
            dept = st.text_input("Department")
            uploaded_photo = st.file_uploader("Upload Profile Picture", type=['jpg', 'png'])
        with f2:
            email = st.text_input("Email Address")
            phone = st.text_input("Contact Number")
        
        if st.form_submit_button("Register Record"):
            if name and email and dept:
                photo = uploaded_photo if uploaded_photo else "https://i.pravatar.cc/150?u=default"
                new_row = {
                    'id': df['id'].max() + 1, 'photo': photo, 'name': name, 'gender': gender,
                    'role': role, 'email': email, 'phone': phone, 'department': dept, 
                    'last_updated': str(datetime.date.today()), 'search_count': 0
                }
                update_df(pd.concat([df, pd.DataFrame([new_row])], ignore_index=True))
                st.success(f"Record for {name} created!")
            else:
                st.error("Missing required fields.")

# --- TAB 4: MANAGEMENT (Updated with Gender Editing) ---
with tabs[3]:
    st.subheader("Administrative Control")
    pick = st.selectbox("Select Record to Edit:", [""] + df['name'].tolist())
    
    if pick:
        idx = df[df['name'] == pick].index[0]
        curr = df.iloc[idx]
        
        with st.form("edit_form"):
            e1, e2 = st.columns(2)
            with e1:
                u_name = st.text_input("Name", curr['name'])
                u_gender = st.selectbox("Gender", ["Male", "Female", "Other"], 
                                        index=["Male", "Female", "Other"].index(curr['gender']) if curr['gender'] in ["Male", "Female", "Other"] else 0)
                u_dept = st.text_input("Department", curr['department'])
            with e2:
                u_email = st.text_input("Email", curr['email'])
                u_phone = st.text_input("Phone", curr['phone'])
            
            if st.form_submit_button("Save Changes"):
                df.at[idx, 'name'] = u_name
                df.at[idx, 'gender'] = u_gender
                df.at[idx, 'department'] = u_dept
                df.at[idx, 'email'] = u_email
                df.at[idx, 'phone'] = u_phone
                update_df(df)
        
        if st.button("🚨 Purge Record"):
            update_df(df.drop(idx))

# SIDEBAR
with st.sidebar:
    st.title("Admin Portal")
    st.write(f"**Last Sync:** {datetime.datetime.now().strftime('%H:%M:%S')}")
    st.divider()
    st.write("Departmental Stats:")
    st.write(df['department'].value_counts())