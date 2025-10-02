import streamlit as st
import pandas as pd
import io
import base64
import matplotlib.pyplot as plt

# ---------- App metadata ----------
st.set_page_config(page_title="Oops My GPA", page_icon="🤓", layout="wide", initial_sidebar_state="expanded")

# ---------- Styling (small, tasteful) ----------

st.markdown(
    """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.0/css/all.min.css" integrity="sha512-DxV+EoADOkOygM4IR9yXP8Sb2qwgidEmeqAEmDKIOfPRQZOWbXCzLC6vjbZyy0vPisbH2SyW27+ddLVCN+OMzQ==" crossorigin="anonymous" referrerpolicy="no-referrer"/>
""", unsafe_allow_html=True)

st.markdown("""
<style>
body {background: linear-gradient(180deg,#ffffff,#f7fbff);} 
.header {display:flex; font-size: 22px; align-items:center; gap:8px}
.app-title {font-size:28px; font-weight:700}
.feature-card {
    background: white;
    padding: 15px;
    margin-top: -3rem;
    text-align: center;
    color: black;
    border-radius: 15px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    border: 1px solid #e1e8ed;
    margin-bottom: 1.5rem;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
            
.feature-card:hover {
    transform: translateY(-5px);
    transform: scale(1.05);
    z-index: 1;
    box-shadow: 0 15px 45px rgba(0,0,0,0.15);
}
    
.social-links {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin: 2rem 0;
    flex-wrap: wrap;
}
        
.social-btn {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    height: 50px;
    width: 50px;
    padding: 0.75rem 0.75rem;
    border-radius: 50%;
    text-decoration: none !important;
    font-weight: 600;
    background: linear-gradient(135deg, #2d3748, #4a5568);
    color: white !important;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    box-shadow: 0 2px 5px rgba(0,0,0,0.5);
    white-space: nowrap;
    animation: socialsAnimation 2s ease-in-out infinite;
}
        
.social-btn::before {
    content: "";
    position: absolute;
    color: #fff;
    top: 0;
    left: -100%;
    width: 200%;
    height: 100%;
    background: linear-gradient(120deg, rgba(255,255,255,0.2), rgba(255,255,255,0));
    transition: left 0.5s ease;
}


.social-btn:hover::before {
    left: 100%;
}

.social-btn:hover {
    transform: scale(1.1) !important;
    text-decoration: none;
    color: black !important;
}
.card {background: #ffffff; padding:18px; border-radius:12px; box-shadow: 0 6px 20px rgba(31, 41, 55, 0.06);}
.small-muted {color: #6b7280; font-size:13px}
</style>
""", unsafe_allow_html=True)

# ---------- Constants & core logic (kept identical to your CLI logic) ----------
PU_SEMESTER_CREDITS = [16, 16, 17, 18, 17, 17, 16, 18]


def calculate_current_gpa_from_cgpas(prev_cgpa, prev_credits, new_cgpa, current_credits):
    numerator = (new_cgpa * (prev_credits + current_credits)) - (prev_cgpa * prev_credits)
    return numerator / current_credits


# ---------- Utility helpers ----------

def dataframe_from_session():
    if "sem_table" not in st.session_state:
        st.session_state.sem_table = pd.DataFrame(columns=["Semester", "GPA", "Credits"])
    return st.session_state.sem_table


def download_link(df, filename="cgpa_report.csv"):
    towrite = io.BytesIO()
    df.to_csv(towrite, index=False)
    towrite.seek(0)
    return towrite


# ---------- Sidebar: global settings & quick actions ----------
with st.sidebar:
    st.markdown("""<div class='header'><i class="fa-solid fa-calculator"></i><div class='app-title'>Oops My GPA 🤓</div></div>""", unsafe_allow_html=True)
    st.caption("A professional,  _user-first_ :blue[CGPA & GPA] and toolkit :sunglasses:")
    st.markdown("""
        <div class="social-links">
                <a href="https://linkedin.com/in/ch-hussain-ali" class="social-btn" style="font-size:1.5rem;" target="_blank">
                <i class="fab fa-linkedin"></i>
                </a>
                <a href="https://github.com/choudaryhussainali" class="social-btn" style="font-size:1.5rem;" target="_blank">        
                <i class="fab fa-github"></i>
                </a>
                <a href="mailto:choudaryhussainali@outlook.com" class="social-btn" style="font-size:1.5rem;" target="_blank">
                    <i class="fas fa-envelope"></i>
                </a>
                <a href="https://www.instagram.com/choudary_hussain_ali/" class="social-btn" style="font-size:1.5rem;" target="_blank">
                    <i class="fa-brands fa-instagram"></i>
                </a>
        </div>
    """, unsafe_allow_html=True)
    st.sidebar.subheader("Quick Presets")
    preset = st.sidebar.selectbox("Choose preset credit pattern:", ("BSFYP-IT (8 sem)", "Custom - manual"))
    st.sidebar.markdown("---")
    st.sidebar.subheader("Import / Export")
    upload = st.sidebar.file_uploader("Upload semester GPAs CSV", type=["csv"] )
    if upload is not None:
        try:
            df_in = pd.read_csv(upload)
            # Expecting columns: Semester, GPA, Credits (credits optional)
            if "Semester" in df_in.columns and "GPA" in df_in.columns:
                st.session_state.sem_table = df_in[ [c for c in ["Semester","GPA","Credits"] if c in df_in.columns] ]
                st.sidebar.success("✅ Imported semester GPAs")
            else:
                st.sidebar.error("CSV must include at least columns: Semester, GPA")
        except Exception as e:
            st.sidebar.error("Failed to parse CSV: " + str(e))

    if st.sidebar.button("Reset saved semesters"):
        st.session_state.sem_table = pd.DataFrame(columns=["Semester", "GPA", "Credits"])
        st.sidebar.info("Cleared saved semester table.")

    st.sidebar.markdown("\n---\nMade with ❤️ for accuracy and clarity")
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; padding: 0; margin-top: 0.5rem;">
            <p style="color: #999; font-size: 0.9rem; margin: 0.5rem 0 0 0;">
                © 2025 Hussain Ali . All rights reserved.
            </p>
        </div>
        """, unsafe_allow_html=True)



# ---------- Main layout ----------
col1, col2 = st.columns([1.6, 1])

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3 style="color: #667eea;"> Oops My GPA 🤓 </h3>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="padding: 10px 15px 10px 15px; text-align: center;">
        <span>A professional, user-friendly GPA & CGPA calculator — offering multiple calculation modes, smart credit handling, interactive semester tracking, CSV import/export, and GPA trend visualization for accurate performance management.</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Choose calculation mode")
    mode = st.selectbox("Mode:", [
        "Current semester GPA finder (CGPA based)",
        "Semester GPA — subject-level",
        "CGPA from semester GPAs",
        "One-step: Semester GPA then update CGPA"
    ])

    st.markdown("\n---\n")

    # ----------------- Mode 1: Semester GPA from subjects -----------------
    if mode == "Semester GPA — subject-level":
        st.subheader("Semester GPA — using Transcript ")
        st.markdown("👉 Enter grade points (GP) and credit hours for each subject. "
            "The app will calculate your semester GPA based on weighted average.")
        
        with st.form(key="form_subjects"):
            cur_sem = st.number_input("Current semester number", min_value=1, max_value=8, value=1)
            n = st.number_input("Number of subjects", min_value=1, value=5)
            cols = st.columns((2,1))
            subjects = []
            total_qp = 0.0
            total_cr = 0
            for i in range(int(n)):
                with st.expander(f"Subject {i+1}", expanded=False):
                    gp = st.number_input(f"  Grade Points — Subject {i+1}", min_value=0.0, value=3.0, step=0.1, key=f"gp_{i}")
                    cr = st.number_input(f"  Credit Hours — Subject {i+1}", min_value=0, value=3, step=1, key=f"cr_{i}")
                    total_qp += gp * cr
                    total_cr += cr
            submitted = st.form_submit_button("Calculate Semester GPA")
            if submitted:
                if total_cr == 0:
                    st.error("Total credit hours cannot be zero.")
                else:
                    sem_gpa = total_qp / total_cr
                    st.success(f"Semester GPA = {sem_gpa:.4f}  (Total credits = {total_cr})")
                    # store in session table
                    df = dataframe_from_session()
                    new_row = {"Semester": int(cur_sem), "GPA": round(sem_gpa,4), "Credits": int(total_cr)}
                    st.session_state.sem_table = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    st.info("Saved semester GPA to session table — view it in the right panel.")

    # ----------------- Mode 2: CGPA from semester GPAs -----------------
    elif mode == "CGPA from semester GPAs":
        st.subheader("CGPA from semester GPAs")
        st.markdown("👉 Enter GPA for each completed semester. Default credit hours are taken from PU scheme "
                "(editable). The app calculates overall CGPA using all entered semesters.")
        max_sem = len(PU_SEMESTER_CREDITS)
        completed = st.number_input(f"Number of semesters completed", min_value=1, max_value=max_sem, value=1)

        st.markdown("Enter each semester GPA below (credits will default to PU scheme but you can edit):")
        gpas = []
        crs = []
        for sem in range(1, int(completed)+1):
            cols = st.columns([2,1,1])
            gpa = cols[0].number_input(f"GPA Sem {sem}", min_value=0.0, value=3.0, step=0.01, key=f"gpa_sem_{sem}")
            default_credit = PU_SEMESTER_CREDITS[sem-1]
            credit = cols[1].number_input(f"Credits Sem {sem}", min_value=0, value=default_credit, key=f"cred_sem_{sem}")
            gpas.append(gpa)
            crs.append(credit)
        if st.button("Compute CGPA"):
            total_qp = sum([g*c for g,c in zip(gpas, crs)])
            total_cr = sum(crs)
            if total_cr == 0:
                st.error("Total credits cannot be zero.")
            else:
                cgpa = total_qp / total_cr
                st.success(f"CGPA after {completed} semesters = {cgpa:.4f} (Total credits = {total_cr})")
                # save to session
                rows = [{"Semester": i+1, "GPA": round(gpas[i],4), "Credits": int(crs[i])} for i in range(len(gpas))]
                st.session_state.sem_table = pd.DataFrame(rows)

    # ----------------- Mode 3: Current semester GPA finder -----------------
    elif mode == "Current semester GPA finder (CGPA based)":
        st.subheader("Current semester GPA finder — two modes")
        st.markdown("👉 Estimate your current semester GPA in two ways:\n"
                "- Mode A: Enter previous CGPA and new CGPA.\n"
                "- Mode B: Enter all previous semester GPAs, then new CGPA. "
                "The app will back-calculate your semester GPA.")
        cur_sem = st.number_input("Current semester number", min_value=1, max_value=8, value=2)
        if cur_sem == 1:
            st.info("First semester — GPA will equal CGPA once results are announced.")
        else:
            finder_mode = st.radio("Use mode:", ("From previous & new CGPA", "By entering all previous semester GPAs"))
            if finder_mode == "From previous & new CGPA":
                prev_cgpa = st.number_input("Previous CGPA (till last semester)", min_value=0.0, value=3.0)
                new_cgpa = st.number_input("New CGPA (after this semester)", min_value=0.0, value=3.0)
                if st.button("Calculate current semester GPA"):
                    prev_credits = sum(PU_SEMESTER_CREDITS[:int(cur_sem)-1])
                    current_credits = PU_SEMESTER_CREDITS[int(cur_sem)-1]
                    current_gpa = calculate_current_gpa_from_cgpas(prev_cgpa, prev_credits, new_cgpa, current_credits)
                    st.success(f"Estimated GPA for semester {int(cur_sem)} = {current_gpa:.4f}")
            else:
                st.markdown("Enter previous semester GPAs — credits default to PU but editable")
                gpas = []
                crs = []
                for sem in range(1, int(cur_sem)):
                    cols = st.columns([2,1])
                    gpa = cols[0].number_input(f"GPA Sem {sem}", min_value=0.0, value=3.0, step=0.01, key=f"prev_gpa_{sem}")
                    credit = cols[1].number_input(f"Credits Sem {sem}", min_value=0, value=PU_SEMESTER_CREDITS[sem-1], key=f"prev_cr_{sem}")
                    gpas.append(gpa)
                    crs.append(credit)
                new_cgpa = st.number_input("New CGPA (after this semester)", min_value=0.0, value=3.0)
                if st.button("Compute current GPA (mode: previous GPAs)"):
                    total_qp = sum([g*c for g,c in zip(gpas, crs)])
                    total_cr = sum(crs)
                    if total_cr == 0:
                        st.error("Previous total credits cannot be zero.")
                    else:
                        prev_cgpa = total_qp / total_cr
                        st.write(f"Calculated previous CGPA = {prev_cgpa:.4f}")
                        current_credits = PU_SEMESTER_CREDITS[int(cur_sem)-1]
                        current_gpa = calculate_current_gpa_from_cgpas(prev_cgpa, total_cr, new_cgpa, current_credits)
                        st.success(f"Estimated GPA for semester {int(cur_sem)} = {current_gpa:.4f}")

    # ----------------- Mode 4: One-step -----------------
    elif mode == "One-step: Semester GPA then update CGPA":
        st.subheader("One-step: compute semester GPA and update CGPA")
        st.markdown("👉 Estimate your current semester GPA in two ways:\n"
                "- Mode A: Enter previous CGPA and new CGPA.\n"
                "- Mode B: Enter all previous semester GPAs, then new CGPA. "
                "The app will back-calculate your semester GPA.")
        cur_sem = st.number_input("Current semester number", min_value=1, max_value=8, value=1)
        with st.form(key="one_step_form"):
            n = st.number_input("Number of subjects in this semester", min_value=1, value=5)
            total_qp = 0.0
            total_cr = 0
            for i in range(int(n)):
                gp = st.number_input(f"GP - Subject {i+1}", min_value=0.0, value=3.0, key=f"one_gp_{i}")
                cr = st.number_input(f"CR - Subject {i+1}", min_value=0, value=3, key=f"one_cr_{i}")
                total_qp += gp*cr
                total_cr += cr
            prev_cgpa = None
            if cur_sem != 1:
                prev_cgpa = st.number_input("Previous CGPA (till last semester)", min_value=0.0, value=3.0)
            submitted = st.form_submit_button("Compute & Update CGPA")
            if submitted:
                if total_cr == 0:
                    st.error("Total credit hours cannot be zero.")
                else:
                    sem_gpa = total_qp / total_cr
                    if cur_sem == 1:
                        st.success(f"Semester 1 GPA = {sem_gpa:.4f}\nCGPA = {sem_gpa:.4f}")
                    else:
                        prev_credits = sum(PU_SEMESTER_CREDITS[:int(cur_sem)-1])
                        current_credits = PU_SEMESTER_CREDITS[int(cur_sem)-1]
                        new_cgpa = (prev_cgpa * prev_credits + sem_gpa * current_credits) / (prev_credits + current_credits)
                        st.success(f"Semester GPA = {sem_gpa:.4f}\nUpdated CGPA after sem {int(cur_sem)} = {new_cgpa:.4f}")
                        # save
                        df = dataframe_from_session()
                        new_row = {"Semester": int(cur_sem), "GPA": round(sem_gpa,4), "Credits": int(current_credits)}
                        st.session_state.sem_table = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Right column: session table, export, and visuals ----------
with col2:

    st.markdown("""
    <div class="feature-card">
        <h3 style="color: #667eea;"><i class="fa-solid fa-chart-line"></i> GPA Chart </h3>
    </div>
    """, unsafe_allow_html=True)
    df = dataframe_from_session()
    if df.empty:
        st.info("No semester data saved yet. Use the left side calculators to add results.")
    else:
        st.dataframe(df.sort_values(by="Semester"))
        # Quick stats
        if st.button("Compute CGPA from saved table"):
            if "GPA" in df.columns and "Credits" in df.columns and len(df) > 0:
                total_qp = (df['GPA']*df['Credits']).sum()
                total_cr = df['Credits'].sum()
                if total_cr == 0:
                    st.error("Saved credits sum to zero.")
                else:
                    cgpa = total_qp / total_cr
                    st.metric("Computed CGPA", f"{cgpa:.4f}")
                    st.write(f"Total Credits: {total_cr}")
            else:
                st.error("Saved table must include columns GPA and Credits.")

        # Download
        buf = download_link(df)
        st.download_button(label="Download CSV", data=buf, file_name="cgpa_report.csv", mime="text/csv")

        # Plot GPA trend
        if len(df) >= 1 and "GPA" in df.columns:
            fig, ax = plt.subplots()
            plotted = df.sort_values(by="Semester")
            ax.plot(plotted['Semester'], plotted['GPA'], marker='o')
            ax.set_xlabel('Semester')
            ax.set_ylabel('GPA')
            ax.set_title('GPA Trend')
            ax.grid(True, linestyle='--', alpha=0.4)
            st.pyplot(fig)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Footer help & tips ----------
st.markdown("---")
cols = st.columns(3)
cols[0].markdown("**Tips**\n- Use the one-step mode to compute semester GPA from subjects and auto-update CGPA.")
cols[1].markdown("**Accuracy**\n- App uses your provided credits. By default PU scheme is used for convenience.")
cols[2].markdown("**Share**\n- Download the CSV and share with peers or import back to continue.")

st.markdown("""
<div style="text-align: center; padding: 2rem 0; border-top: 1px solid #e2e8f0; margin-top: 2rem;">
    <p style="color: #666; margin: 0;">
        Crafted with ❣ by <strong style="color: #667eea;">CHOUDARY HUSSAIN ALI</strong> | 
         PU-Affiliated Colleges | Built with Advanced Technology 
    </p>
    <p style="color: #999; font-size: 0.9rem; margin: 0.5rem 0 0 0;">
        Copyright © 2025. All rights reserved. | 
        <a href="#" style="color: #667eea;">Privacy Policy</a> | 
        <a href="#" style="color: #667eea;">Terms of Service</a>
    </p>
    <p style="font-size: 0.8rem; margin: 0.5rem; text-decoration: none;">
        <span>E-mail | </span>
        <a href="mailto:choudaryhussainali@outlook.com" style="color: #667eea;text-decoration: none;">choudaryhussainali@outlook.com</a>   
    </p>
</div>
""", unsafe_allow_html=True)


# ---------- End of app ----------
