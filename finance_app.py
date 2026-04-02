import streamlit as st

st.set_page_config(page_title="Universal Student Debt Forecaster", page_icon="📈")

# --- APP TITLE ---
st.title("🚀 Universal Student Debt & Budget Forecaster")
st.markdown("Designed for Grade 12s and University/College Students in Canada.")

# --- MAIN NAVIGATION ---
app_mode = st.sidebar.selectbox("Choose Your Current Stage:", ["Grade 12 Student", "Current Uni/College Student"])

# --- SHARED DATA (2026 ESTIMATES) ---
black_excellence_awards = {
    "BlackNorth Future Leaders": 2000,
    "BBPA Harry Jerome Award": 5000,
    "Deloitte Bloom Scholarship": 5000,
    "BFCN Scholarship": 1500
}

# ---------------------------------------------------------
# MODE 1: GRADE 12 STUDENT (PLANNING)
# ---------------------------------------------------------
if app_mode == "Grade 12 Student":
    st.header("📍 High School Planning Mode")
    
    col1, col2 = st.columns(2)
    with col1:
        target_uni = st.text_input("Which University/College are you aiming for?", "Waterloo")
        study_area = st.text_input("What do you want to study?", "Computer Science & Accounting")
        living_choice = st.radio("Living Situation:", ["On-Campus Residence", "Living at Home"])
    
    with col2:
        est_tuition = st.number_input("Estimated Annual Tuition ($)", value=15000)
        target_debt = st.number_input("Max Debt Goal at Graduation ($)", value=20000)
        hs_savings = st.number_input("How much have you saved so far? ($)", value=2000)

    st.subheader("🏆 Scholarship & Income Planning")
    selected_awards = st.multiselect("Select Black Initiative Awards you're applying for:", list(black_excellence_awards.keys()))
    total_schols = sum([black_excellence_awards[a] for a in selected_awards])
    
    monthly_save = st.slider("Target monthly savings during uni ($)", 0, 500, 100)
    
    # Logic
    res_cost = 12000 if living_choice == "On-Campus Residence" else 0
    total_4yr_cost = (est_tuition + res_cost) * 4
    total_4yr_income = hs_savings + total_schols + (monthly_save * 12 * 4)
    forecast_debt = total_4yr_cost - total_4yr_income

    st.divider()
    st.subheader(f"📊 Forecast for {target_uni}")
    st.metric("Estimated Graduation Debt", f"${forecast_debt:,}", delta=f"{target_debt - forecast_debt:,} from goal")
# The gap between your forecast and your goal
    gap = forecast_debt - target_debt

    if forecast_debt > target_debt:
        st.info(f"⚠️ To graduate with only ${target_debt:,} in debt, you need an extra ${gap:,} from other sources.")
    else:
        st.success(f"✅ Amazing! You are projected to be ${abs(gap):,} BELOW your debt limit of ${target_debt:,}.")
# ---------------------------------------------------------
# MODE 2: CURRENT STUDENT (TRACKING)
# ---------------------------------------------------------
else:
    st.header("🎒 University/College Tracking Mode")
    
    st.info("Input your actual numbers below to track your real-time debt progress.")
    
    c1, c2 = st.columns(2)
    with c1:
        current_tuition = st.number_input("Actual Tuition per Term ($)", value=8000)
        num_terms = st.number_input("Terms remaining in your degree?", value=8)
    with c2:
        current_savings = st.number_input("Current Bank Balance ($)", value=1500)
        coop_pay = st.number_input("Average Co-op/Job pay per term ($)", value=12000)
        total_coops = st.slider("Total Co-op terms remaining?", 0, 6, 4)

    # Logic
    future_costs = current_tuition * num_terms
    future_income = (coop_pay * total_coops) + current_savings
    remaining_debt = future_costs - future_income

    st.divider()
    st.subheader("📉 Your Financial Trajectory")
    st.write(f"Total remaining costs to graduate: **${future_costs:,}**")
    st.write(f"Total projected income from co-op: **${future_income:,}**")
    
    if remaining_debt > 0:
        st.warning(f"Projected Debt at Graduation: **${remaining_debt:,}**")
    else:
        st.success(f"You are projected to graduate with a SURPLUS of **${abs(remaining_debt):,}**!")
        # 1. Define the "Filing Cabinet" of data
uni_data = {
    "Custom (Type your own)": 0,
    "U of Waterloo (CS/BBA)": 18100,
    "U of Toronto (CS)": 11420,
    "UBC (Computer Science)": 6100,
    "McGill (CS - Out of Province)": 12600,
    "McMaster (CS)": 10120
}

# 2. Create the Dropdown
selected_uni = st.selectbox("Quick Select University:", list(uni_data.keys()))

# 3. Logic: If they pick a school, use that price. If they pick Custom, let them type.
default_price = uni_data[selected_uni]

if selected_uni == "Custom (Type your own)":
    est_tuition = st.number_input("Estimated Annual Tuition ($)", value=10000)
else:
    # This shows the price but allows them to tweak it if they want
    est_tuition = st.number_input("Estimated Annual Tuition ($)", value=default_price)

    # --- ADVANCED ROI ENGINE ---
st.header("💼 Advanced ROI (Return on Investment) & Career Strategy")

col1, col2 = st.columns(2)
with col1:
    starting_salary = st.number_input("Expected Starting Salary ($)", value=85000)
    # Average salary for a high school grad (no degree) in 2026 is approx $35,000
    baseline_salary = 35000 
with col2:
    years_to_calculate = st.slider("Forecast ROI over how many years?", 1, 20, 10)

# 1. Calculate Net Profit (Gains - Costs)
annual_gain = starting_salary - baseline_salary
total_gain_over_time = annual_gain * years_to_calculate
net_profit = total_gain_over_time - total_4yr_cost

# 2. Calculate ROI %
roi_percent = (net_profit / total_4yr_cost) * 100

# 3. Calculate Payback Period (Break-even)
payback_years = total_4yr_cost / annual_gain

# --- VISUAL DISPLAY ---
st.divider()
c1, c2 = st.columns(2)
c1.metric(f"{years_to_calculate}-Year ROI", f"{roi_percent:,.0f}%")
c2.metric("Break-even Point", f"{payback_years:.1f} Years")

st.write(f"💡 **Insight:** After graduating, it will take you roughly **{payback_years:.1f} years** of working to fully 'pay back' the cost of your degree through your increased earnings.")
# --- SIMPLIFIED ROI FOR USERS ---
st.header("⏳ The 'Payback' Timeline")

# We assume a standard 'No-Degree' job pays $35k
extra_annual_income = starting_salary - 35000 

if extra_annual_income > 0:
    years_to_break_even = total_4yr_cost / extra_annual_income
    
    st.write(f"If you graduate with **${forecast_debt:,}** in debt:")
    st.info(f"🚀 With your expected salary, you'll earn enough *extra* money to have 'paid off' the total cost of your degree in **{years_to_break_even:.1f} years**.")
    
    # Progress bar to show the 'Payback'
    progress = min(100, int((years_to_calculate / years_to_break_even) * 100))
    st.write(f"Progress toward full ROI over {years_to_calculate} years:")
    st.progress(progress)
else:
    st.error("⚠️ Your expected salary isn't higher than a non-degree job. The ROI is negative.")