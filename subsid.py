import pandas as pd
# ============================== IMPORTS ===============================
import pandas as pd
import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from streamlit_option_menu import option_menu
from sklearn.preprocessing import StandardScaler
import base64
from pyvis.network import Network
import streamlit.components.v1 as components
import altair as alt
from fpdf import FPDF
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

# ============================== DATA LOADING ===============================
@st.cache_data
def load_iran_data():
    df_Iran = pd.read_excel("Iran_Fuel_Subsidy_Reform_2005_2022.xlsx")
    return df_Iran

def load_indonisa_data():
    df_indo=pd.read_excel("Indonesia_Fuel_Subsidy_Reform_2005_2022.xlsx")
    return df_indo

def load_Mexico_data():
    df_Mx=pd.read_excel("Mexico_Fuel_Subsidy_Reform.xlsx")
    return df_Mx
def load_Nigeria_data():
    
    df_Ng=pd.read_excel("Nigeria_Fuel_Subsidy_Data.xlsx")
    return df_Ng
def load_Egypt_data():
    
    df_Eg=pd.read_excel("Nigeria_Fuel_Subsidy_Data.xlsx")
    return df_Eg

# ============================== SIDEBAR ===============================
with st.sidebar:
    country = option_menu("🌍 Select Country",
        ["Iran", "Indonesia", "Mexico", "Nigeria", "Egypt"],
        icons=["flag"] * 5,
        menu_icon="globe", default_index=0)

    if country == "Iran":
        iran_page = option_menu("📊 Iran Dashboard",
            ["Overview", "Correlation", "Causal Diagram", "Cost-Benefit", "Elasticity", "Presidents and Policy Map", "Download"],
            icons=["graph-up", "bar-chart", "diagram-2", "file-earmark-text", "speedometer", "person-lines-fill", "download"],
            menu_icon='cast', default_index=0)
    if country=="Indonesia":
        indo_page=option_menu("📊 Indonesia Dashboard",
        ["Overview", "Correlation", "Causal Diagram", "Cost-Benefit", "Elasticity", "Presidents and Policy Map", "Download"],
        icons=["graph-up", "bar-chart", "diagram-2", "file-earmark-text", "speedometer", "person-lines-fill", "download"],
        menu_icon='cast', default_index=0)

    if country=="Mexico":
        Mx_page=option_menu("📊 Indonesia Dashboard",
        ["Overview", "Correlation", "Causal Diagram", "Cost-Benefit", "Elasticity", "Presidents and Policy Map", "Download"],
        icons=["graph-up", "bar-chart", "diagram-2", "file-earmark-text", "speedometer", "person-lines-fill", "download"],
        menu_icon='cast', default_index=0)

    if country=="Nigeria":
        Ng_page=option_menu("📊 Indonesia Dashboard",
        ["Overview", "Correlation", "Causal Diagram", "Cost-Benefit", "Elasticity", "Presidents and Policy Map", "Download"],
        icons=["graph-up", "bar-chart", "diagram-2", "file-earmark-text", "speedometer", "person-lines-fill", "download"],
        menu_icon='cast', default_index=0)

    if country=="Egypt":
        Eg_page=option_menu("📊 Indonesia Dashboard",
        ["Overview", "Correlation", "Causal Diagram", "Cost-Benefit", "Elasticity", "Presidents and Policy Map", "Download"],
        icons=["graph-up", "bar-chart", "diagram-2", "file-earmark-text", "speedometer", "person-lines-fill", "download"],
        menu_icon='cast', default_index=0)
    





# ============================== PAGE CONTENT IRAN ===============================
df_Iran = load_iran_data()
st.dataframe(df_Iran)

if country == "Iran":

    if iran_page == "Overview":
        st.title("Iran Fuel Subsidy Reform Dashboard (2005-2022) - Overview")
        year_min, year_max = int(df_Iran['Year'].min()), int(df_Iran['Year'].max())
        selected_years = st.slider("Select Year Range", year_min, year_max, (year_min, year_max))
        df_filtered = df_Iran[(df_Iran['Year'] >= selected_years[0]) & (df_Iran['Year'] <= selected_years[1])]

        trend_vars = ["Fuel_Price_USD_per_Liter", "Fuel_Consumption_Liter_per_HH", "Gini_Index", "Cash_Transfer_USD_per_person_per_month"]
        fig = px.line(df_filtered, x="Year", y=trend_vars, markers=True,
                      labels={"value": "Value", "variable": "Variable"},
                      title="Trends of Key Variables in Iran")
        st.plotly_chart(fig, use_container_width=True)
        with st.expander("Show Raw Data"):
            st.dataframe(df_filtered)

    elif iran_page == "Correlation":
        st.title("Correlation Matrix of Key Variables (Iran)")
        vars_corr = ["Fuel_Price_USD_per_Liter", "Fuel_Subsidy_perc_GDP", "Fuel_Consumption_Liter_per_HH",
                     "Consumption_Change_pct", "Gini_Index", "Poverty_Rate_pct", "Cash_Transfer_USD_per_person_per_month"]
        df_corr = df_Iran[vars_corr].dropna()
        scaler = StandardScaler()
        df_scaled = pd.DataFrame(scaler.fit_transform(df_corr), columns=vars_corr)
        corr = df_scaled.corr().round(2)
        z = corr.values
        fig = ff.create_annotated_heatmap(z, x=corr.columns.tolist(), y=corr.index.tolist(), colorscale='RdBu')
        st.plotly_chart(fig, use_container_width=True)

    elif iran_page == "Causal Diagram":
        st.title("Causal Diagram of Fuel Subsidy Reform (Iran)")
        edges = [("President", "Reform_Type"), ("Reform_Type", "Fuel_Price"), ("Reform_Type", "Cash_Transfer"),
                 ("Fuel_Price", "Fuel_Subsidy"), ("Fuel_Price", "Fuel_Consumption"), ("Fuel_Price", "Cash_Transfer"),
                 ("Fuel_Price", "Gini_Index"), ("Fuel_Price", "Poverty_Rate"), ("Cash_Transfer", "Fuel_Consumption"),
                 ("Cash_Transfer", "Gini_Index"), ("Cash_Transfer", "Poverty_Rate"),
                 ("Fuel_Consumption", "Consumption_Change"), ("Fuel_Consumption", "Gini_Index")]

        net = Network(height='600px', width='100%', directed=True)
        for edge in edges:
            net.add_node(edge[0], label=edge[0])
            net.add_node(edge[1], label=edge[1])
            net.add_edge(edge[0], edge[1])
        net.save_graph('causal_graph.html')
        with open("causal_graph.html", 'r', encoding='utf-8') as f:
            html = f.read()
        components.html(html, height=650)

    elif iran_page == "Cost-Benefit":
        st.title("Cost-Benefit Analysis Summary")
        df_cb = df_Iran.dropna(subset=["Fuel_Subsidy_perc_GDP", "Cash_Transfer_USD_per_person_per_month", "Gini_Index"])
        avg_subsidy = df_cb["Fuel_Subsidy_perc_GDP"].mean()
        avg_transfer = df_cb["Cash_Transfer_USD_per_person_per_month"].mean()
        gini_change = df_cb["Gini_Index"].iloc[-1] - df_cb["Gini_Index"].iloc[0]
        st.markdown(f"- 🧾 **Avg Subsidy (% of GDP):** `{avg_subsidy:.2f}`")
        st.markdown(f"- 💸 **Avg Cash Transfer:** `{avg_transfer:.2f} USD`")
        st.markdown(f"- 📉 **Change in Gini Index:** `{gini_change:.3f}`")

    elif iran_page == "Elasticity":
        st.title("Fuel Price Elasticity by President")
        st.markdown("Elasticity = %Δ Consumption / %Δ Price")
        presidents_list = df_Iran["President"].dropna().unique()

        results = []
        for p in presidents_list:
            df_pres = df_Iran[df_Iran["President"] == p].dropna(subset=["Fuel_Price_USD_per_Liter", "Fuel_Consumption_Liter_per_HH"])
            if len(df_pres) >= 2:
                price_change = (df_pres["Fuel_Price_USD_per_Liter"].iloc[-1] - df_pres["Fuel_Price_USD_per_Liter"].iloc[0]) / df_pres["Fuel_Price_USD_per_Liter"].iloc[0]
                cons_change = (df_pres["Fuel_Consumption_Liter_per_HH"].iloc[-1] - df_pres["Fuel_Consumption_Liter_per_HH"].iloc[0]) / df_pres["Fuel_Consumption_Liter_per_HH"].iloc[0]
                elasticity = cons_change / price_change if price_change != 0 else None
                results.append({"President": p, "Elasticity": round(elasticity, 2)})

        df_elas = pd.DataFrame(results)
        st.dataframe(df_elas)

        fig = px.bar(df_elas, x="President", y="Elasticity", color="President",
                    text="Elasticity",
                    title="Elasticity of Fuel Demand under Each President",
                    labels={"Elasticity": "Elasticity (Consumption/Price)"})
        st.plotly_chart(fig, use_container_width=True)


    elif iran_page == "Presidents and Policy Map":
        tab1, tab2 ,tab3 = st.tabs(["President Trends", "🗺 Reform Policy Map",
                                    "Future Research Directions"])

        with tab1:
            st.subheader("📊 Trends by President")
            president_options = ["All"] + sorted(df_Iran["President"].dropna().unique())
            selected_president = st.selectbox("Select President", president_options)
            selected_var = st.selectbox("Select Variable",
                                        ["Fuel_Price_USD_per_Liter",
                                         "Fuel_Consumption_Liter_per_HH",
                                         "Fuel_Subsidy_perc_GDP",
                                         "Cash_Transfer_USD_per_person_per_month",
                                         "Gini_Index", "Poverty_Rate_pct"])

            if selected_president != "All":
                df_president = df_Iran[df_Iran["President"] == selected_president]
                
            else:
                df_president = df_Iran.copy()

            filtered_summary=df_Iran[
                    ['Fuel_Price_USD_per_Liter',
                     'Fuel_Consumption_Liter_per_HH',
                     'Fuel_Subsidy_perc_GDP','Gini_Index']]

            summary_df = filtered_summary.describe()
            avg_price = summary_df.loc["mean", "Fuel_Price_USD_per_Liter"]
            avg_cons = summary_df.loc["mean", "Fuel_Consumption_Liter_per_HH"]
            avg_subsidy = summary_df.loc["mean", "Fuel_Subsidy_perc_GDP"]
            avg_gini = summary_df.loc["mean", "Gini_Index"]
            st.markdown(f"""### 🧾 Summary for President **{selected_president}**:
    - 🛢️ Avg Fuel Price: `{avg_price:.2f} USD/L`
    - ⛽ Avg Fuel Consumption: `{avg_cons:.2f} L/HH`
    - 💰 Avg Fuel Subsidy: `{avg_subsidy:.2f}% of GDP`
    - 📉 Avg Gini Index: `{avg_gini:.3f}`
    """)
            # Line chart for selected variable
            if "Year" in df_president.columns:
                chart = alt.Chart(df_president).mark_line(point=True).encode(
                    x='Year:O',y=alt.Y(f'{selected_var}:Q',
                                       title=selected_var.replace("_", " ")),
                    tooltip=['Year', selected_var]).properties(width=700,
                                                               height=400,
                                                               title=f"{selected_var.replace('_', ' ')} Trend under {selected_president}")
                st.altair_chart(chart, use_container_width=True)

        with tab2:
            st.subheader("🗺 Reform Policy Map")
            st.markdown("Select a Iranian president from the dropdown to view their fuel subsidy reform policies and broader economic agenda.")
            Iran_president = ["Mohammad Khatami (1997–2005)",
                              "Mahmoud Ahmadinejad (2005–2013)",
                                 "Hassan Rouhani (2013–2021)",
                                 "Ebrahim Raisi (2021–2022[data cutoff])"
]
            selected_president = st.selectbox("Choose President",
                                              Iran_president)
            if selected_president.startswith("Mohammad Khatami"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    Khatami_image_path = os.path.join("images", "Khatami.jpg")
                    st.image(Khatami_image_path, use_container_width=True)

                with col2:
                    st.markdown("### 🧾 President: Mohammad Khatami")
                    st.markdown("Maintained heavy fuel subsidies with no formal rationing system during his presidency.")
                    st.markdown("The government focused primarily on **political and social reforms**, while fuel policy remained largely unchanged.")
                    st.markdown("Rising consumption and smuggling pressures began to surface toward the end of his term.")

            if selected_president.startswith("Mahmoud Ahmadinejad"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    Ahmadinejad_image_path = os.path.join("images", "Ahmadinejad.jpg")
                    st.image(Ahmadinejad_image_path, use_container_width=True)

                with col2:
                    st.markdown("### 🧾 President: Mahmoud Ahmadinejad")
                    st.markdown("Introduced the **fuel rationing system using smart fuel cards** in 2007 as a major reform to curb excessive gasoline consumption and reduce fuel smuggling. Despite ongoing subsidies, this policy marked a shift toward more controlled fuel distribution.")
                    st.markdown("Launched Targeted Subsidy Reform Plan in 2010: sharply increased fuel prices and introduced universal cash transfers to compensate households.")
                    st.markdown("Sought to replace implicit energy subsidies with direct support.")
                    st.markdown("Initial phase successful in reducing fuel consumption temporarily, but inflationary effects and lack of targeted support weakened long-term impact.")
                    st.markdown("Maintained populist rhetoric, emphasizing economic justice and support for the poor.")

            if selected_president.startswith("Hassan Rouhani"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    Rouhani_image_path = os.path.join("images", "Rouhani.jpg")
                    st.image(Rouhani_image_path, use_container_width=True)

                with col2:
                    st.markdown("### 🧾 President: Hassan Rouhani")
                    st.markdown("Adopted a more **technocratic and gradualist** approach to subsidy reform.")
                    st.markdown("Continued partial price adjustments but **reduced the scope of universal cash transfers** by tightening eligibility.")
                    st.markdown("Initially adopted a more **moderate approach** by **de-emphasizing the fuel card system**, allowing more flexible access to subsidized fuel.")
                    st.markdown("In 2019, the government reinstated the fuel rationing policy and significantly increased the gasoline price to **reduce smuggling** and alleviate **budgetary pressure**.The policy shift led to widespread protests but was positioned as a necessary fiscal measure.")
                    st.markdown("Sought international engagement (e.g., JCPOA) to ease economic pressure and create fiscal space for reforms.")
                    
                    

            if selected_president.startswith("Ebrahim Raisi"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    raisi_image_path = os.path.join("images", "raisi.jpg")
                    st.image(raisi_image_path, use_container_width=True)

                with col2:
                    st.markdown("### 🧾 President: Ebrahim Raisi")
                    st.markdown("Promised justice and continuation of support to low-income groups.")
                    st.markdown("Shifted toward more targeted cash assistance, with a focus on vulnerable populations rather than universal payments.")
                    st.markdown("Early phase marked by hesitance to raise fuel prices, due to inflation and political sensitivity.")
                    st.markdown("No major subsidy overhaul occurred within the data period (until 2022).")
        with tab3:
            st.expander("🔬 Future Research Directions:")
            st.markdown("While this dashboard presents a foundational overview of fuel subsidy reforms and their macroeconomic implications, several key areas remain for future exploration:")
            st.markdown("- **Corruption and Governance**: Investigating how corruption levels and institutional quality influence the outcomes of subsidy reforms.")
            st.markdown("- **Price Stability and Inflation Control**: Analyzing how reforms affect long-term price stability and the credibility of monetary policy.")
            st.markdown("- **Equity and Social Impact**: Studying the distributional consequences of subsidy removal on different income groups.")
            st.markdown("- **Subnational Variations**: Exploring regional disparities in reform impacts within each country.")
            st.markdown("- **Data Gaps**: Filling missing time-series data and integrating more granular indicators such as fuel price pass-through, shadow economy effects, and enforcement mechanisms.")
            st.markdown("These aspects are currently under development and will be integrated into future updates of this dashboard.")

    elif iran_page == "Download":
        st.sidebar.markdown("---")
        st.sidebar.markdown("📥 Download Processed Data")

        def filedownload(df):
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="Iran_Reform_Filtered.csv">Download CSV</a>'
            return href

        st.markdown(filedownload(df_Iran), unsafe_allow_html=True)

st.markdown("---")
st.caption("Data: Real indicators from 2005–2022")

# ============================== PAGE CONTENT INDONISIA ===============================
df_indo=load_indonisa_data()
st.dataframe(df_indo)

if country == "Indonesia":

    if indo_page == "Overview":
        st.title("Indonisia Fuel Subsidy Reform Dashboard (2005-2022) - Overview")
        year_min, year_max = int(df_indo['Year'].min()), int(df_indo['Year'].max())
        selected_years = st.slider("Select Year Range", year_min, year_max, (year_min, year_max))
        df_filtered = df_indo[(df_indo['Year'] >= selected_years[0]) & (df_indo['Year'] <= selected_years[1])]

        trend_vars = ["Fuel_Price_USD_per_Liter", "Fuel_Consumption_Liter_per_HH", "Gini_Index", "Cash_Transfer_USD_per_person_per_month"]
        fig = px.line(df_filtered, x="Year", y=trend_vars, markers=True,
                      labels={"value": "Value", "variable": "Variable"},
                      title="Trends of Key Variables in Indonesia")
        st.plotly_chart(fig, use_container_width=True) 
        with st.expander("Show Raw Data"):
            st.dataframe(df_filtered)

    elif indo_page == "Correlation":
        st.title("Correlation Matrix of Key Variables (Indonisia)")
        vars_corr = ["Fuel_Price_USD_per_Liter", "Fuel_Subsidy_perc_GDP", "Fuel_Consumption_Liter_per_HH",
                     "Consumption_Change_pct", "Gini_Index", "Poverty_Rate_pct", "Cash_Transfer_USD_per_person_per_month"]
        df_corr = df_indo[vars_corr].dropna()
        scaler = StandardScaler()
        df_scaled = pd.DataFrame(scaler.fit_transform(df_corr), columns=vars_corr)
        corr = df_scaled.corr().round(2)
        z = corr.values
        fig = ff.create_annotated_heatmap(z, x=corr.columns.tolist(), y=corr.index.tolist(), colorscale='RdBu')
        st.plotly_chart(fig, use_container_width=True)

    elif indo_page == "Causal Diagram":
        G = nx.DiGraph()
        edges_id = [
            ("Fuel_Price", "Fuel_Subsidy", "-"),
            ("Fuel_Price", "Fuel_Consumption", "+"),
            ("Fuel_Price", "Gini_Index", "-"),
            ("Fuel_Price", "Poverty_Rate", "+"),
            ("Fuel_Price", "Cash_Transfer", "+"),
            ("Fuel_Subsidy", "Fuel_Consumption", "-"),
            ("Fuel_Subsidy", "Gini_Index", "+"),
            ("Fuel_Subsidy", "Poverty_Rate", "-"),
            ("Fuel_Subsidy", "Cash_Transfer", "-"),
            ("Fuel_Consumption", "Poverty_Rate", "+"),
            ("Fuel_Consumption", "Cash_Transfer", "+"),
            ("Gini_Index", "Poverty_Rate", "-"),
            ("Gini_Index", "Cash_Transfer", "-"),
            ("Poverty_Rate", "Cash_Transfer", "+")]

        for src, dst, sign in edges_id:
            G.add_edge(src, dst, sign=sign)

        pos_id = {
                "Fuel_Price": (-3, 1),"Fuel_Subsidy": (-1.5, 2),
                "Fuel_Consumption": (-1.5, 0),"Cash_Transfer": (-1.5, -2),
                "Consumption_Change": (0.5, 0.5),"Gini_Index": (2, 1),
                "Poverty_Rate": (3.5, 1)}
        plt.figure(figsize=(14, 8))
        nx.draw_networkx_nodes(G, pos_id, node_color="lightgreen",
                                   node_size=2200)
        nx.draw_networkx_labels(G, pos_id, font_size=9)
        edge_colors = ['green' if G[u][v]['sign'] == '+' else 'red' for u, v in G.edges()]
        nx.draw_networkx_edges(G, pos_id, edge_color=edge_colors, arrowsize=20)
        edge_labels = nx.get_edge_attributes(G, "sign")
        nx.draw_networkx_edge_labels(G, pos_id, edge_labels=edge_labels, font_color="red", font_size=10)
        plt.title("Causal Diagram based on Correlation Matrix – Indonesia", fontsize=15)
        plt.axis("off")
        plt.tight_layout()
        st.pyplot(plt)
        plt.clf()

    elif indo_page == "Cost-Benefit":
        st.title("Cost-Benefit Analysis Summary")
        df_cb = df_indo.dropna(subset=["Fuel_Subsidy_perc_GDP", "Cash_Transfer_USD_per_person_per_month", "Gini_Index"])
        avg_subsidy = df_cb["Fuel_Subsidy_perc_GDP"].mean()
        avg_transfer = df_cb["Cash_Transfer_USD_per_person_per_month"].mean()
        gini_change = df_cb["Gini_Index"].iloc[-1] - df_cb["Gini_Index"].iloc[0]
        st.markdown(f"- 🧾 **Avg Subsidy (% of GDP):** `{avg_subsidy:.2f}`")
        st.markdown(f"- 💸 **Avg Cash Transfer:** `{avg_transfer:.2f} USD`")
        st.markdown(f"- 📉 **Change in Gini Index:** `{gini_change:.3f}`")

    elif indo_page == "Elasticity":
        st.title("Fuel Price Elasticity by President")
        st.markdown("Elasticity = %Δ Consumption / %Δ Price")
        presidents_list = df_indo["Presidents"].dropna().unique()

        results = []
        for p in presidents_list:
            df_pres = df_indo[df_indo["Presidents"] == p].dropna(subset=["Fuel_Price_USD_per_Liter",
                                                                         "Fuel_Consumption_Liter_per_HH"])
            if len(df_pres) >= 2:
                price_change = (df_pres["Fuel_Price_USD_per_Liter"].iloc[-1] - df_pres["Fuel_Price_USD_per_Liter"].iloc[0]) / df_pres["Fuel_Price_USD_per_Liter"].iloc[0]
                cons_change = (df_pres["Fuel_Consumption_Liter_per_HH"].iloc[-1] - df_pres["Fuel_Consumption_Liter_per_HH"].iloc[0]) / df_pres["Fuel_Consumption_Liter_per_HH"].iloc[0]
                elasticity = cons_change / price_change if price_change != 0 else None
                results.append({"Presidents": p, "Elasticity": round(elasticity, 2)})

        df_elas = pd.DataFrame(results)
        st.dataframe(df_elas)

        fig = px.bar(df_elas, x="Presidents", y="Elasticity", color="Presidents",
                    text="Elasticity",
                    title="Elasticity of Fuel Demand under Each President",
                    labels={"Elasticity": "Elasticity (Consumption/Price)"})
        st.plotly_chart(fig, use_container_width=True)


    elif indo_page == "Presidents and Policy Map":
        tab1, tab2, tab3 = st.tabs(["President Trends", "Static Policy Map",
                              "Future Research Directions"])

        with tab1:
            st.subheader("📊 Trends by President")
            president_options = ["All"] + sorted(df_indo["Presidents"].dropna().unique())
            selected_president = st.selectbox("Select President", president_options)
            selected_var = st.selectbox("Select Variable",
                                        ["Fuel_Price_USD_per_Liter",
                                         "Fuel_Consumption_Liter_per_HH",
                                         "Fuel_Subsidy_perc_GDP",
                                         "Cash_Transfer_USD_per_person_per_month",
                                         "Gini_Index", "Poverty_Rate_pct"])

            if selected_president != "All":
                df_president = df_indo[df_indo["Presidents"] == selected_president]
                df_president = df_indo[df_indo["Presidents"] == selected_president]
            else:
                df_president = df_indo.copy()

            filtered_summary=df_indo[
                    ['Fuel_Price_USD_per_Liter',
                     'Fuel_Consumption_Liter_per_HH',
                     'Fuel_Subsidy_perc_GDP','Gini_Index']]

            summary_df = filtered_summary.describe()
            avg_price = summary_df.loc["mean", "Fuel_Price_USD_per_Liter"]
            avg_cons = summary_df.loc["mean", "Fuel_Consumption_Liter_per_HH"]
            avg_subsidy = summary_df.loc["mean", "Fuel_Subsidy_perc_GDP"]
            avg_gini = summary_df.loc["mean", "Gini_Index"]
            st.markdown(f"""### 🧾 Summary for President **{selected_president}**:
    - 🛢️ Avg Fuel Price: `{avg_price:.2f} USD/L`
    - ⛽ Avg Fuel Consumption: `{avg_cons:.2f} L/HH`
    - 💰 Avg Fuel Subsidy: `{avg_subsidy:.2f}% of GDP`
    - 📉 Avg Gini Index: `{avg_gini:.3f}`
    """)
            # Line chart for selected variable
            if "Year" in df_president.columns:
                chart = alt.Chart(df_president).mark_line(point=True).encode(
                    x='Year:O',y=alt.Y(f'{selected_var}:Q',
                                       title=selected_var.replace("_", " ")),
                    tooltip=['Year', selected_var]).properties(width=700,
                                                               height=400,
                                                               title=f"{selected_var.replace('_', ' ')} Trend under {selected_president}")
                st.altair_chart(chart, use_container_width=True)

        with tab2:
            st.subheader("🗺 Reform Policy Map")
            st.markdown("Select a Indonisian president from the dropdown to view their fuel subsidy reform policies and broader economic agenda.")
            Indo_president = ["Megawati Sukarnoputri (2001–2004)",
                              "Susilo Bambang Yudhoyono (2004–2014)",
                                 "Joko Widodo-First Term (Jokowi)(2014–2019))",
                                 "Joko Widodo–Second Term (2019–2022))"
]
            selected_president = st.selectbox("Choose President",
                                              Indo_president)
            if selected_president.startswith("Megawati Sukarnoputri"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    Sukarnoputri_image_path = os.path.join("images", "Sukarnoputri.jpg")
                    st.image(Sukarnoputri_image_path, use_container_width=True)

                with col2:
                    st.markdown("### 🧾 President: Megawati Sukarnoputri")
                    st.markdown("Continued **large fuel subsidies**, keeping domestic fuel prices low.")
                    st.markdown("High global oil prices increased fiscal pressure, but no major subsidy reforms were introduced.")
                    st.markdown("Fuel subsidies consumed a growing share of the national budget.")

            if selected_president.startswith("Susilo Bambang Yudhoyono"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    Yudhoyono_image_path = os.path.join("images", "Yudhoyono.jpg")
                    st.image(Yudhoyono_image_path, use_container_width=True)

                with col2:
                    st.markdown("### 🧾 President: Susilo Bambang Yudhoyono")
                    st.markdown("**Major steps to reform fuel subsidies** due to fiscal strain and rising oil prices.")
                    st.markdown("In 2005, the government significantly raised fuel prices (by up to 126%) and introduced **compensatory cash transfers (BLT)** to low-income households.")
                    st.markdown("Further price hikes occurred in 2008 and 2013, though some were rolled back due to political and public resistance.")
                    st.markdown("**Fuel subsidy costs dropped temporarily**, but consumption kept growing.")
                    st.markdown("Introduced early forms of **targeted social** protection linked to subsidy reform.")

            if selected_president.startswith("Joko Widodo (Jokowi)"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    Jokowi_image_path = os.path.join("images", "Jokowi.jpg")
                    st.image(Jokowi_image_path, use_container_width=True)

                with col2:
                    st.markdown("### 🧾 President: Joko Widodo (Jokowi) – First Term")
                    st.markdown("Launched **bold fuel subsidy reforms** shortly after taking office.")
                    st.markdown("In 2015, removed subsidies for **premium gasoline**, moving to a **floating price system** linked to global markets (except for diesel and some rural areas).")
                    st.markdown("Reallocated savings from subsidies to infrastructure and social welfare (health, education, village funds).")
                    st.markdown("Focused on building popular support through visible development projects rather than direct fuel support.")
                    

            if selected_president.startswith("Joko Widodo – Second Term"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    Jokowi_image_path = os.path.join("images", "Jokowi.jpg")
                    st.image(Jokowi_image_path, use_container_width=True)

                with col2:
                    st.markdown("### 🧾 President:Joko Widodo – Second Term (2019–2022)")
                    st.markdown("Maintained controlled pricing for some fuels (e.g., Pertalite and diesel), reintroducing **partial subsidies** due to global price hikes.")
                    st.markdown("Emphasized economic recovery post-COVID and supported energy affordability.")
                    st.markdown("Continued infrastructure investment, but **fiscal pressures increased** as global oil prices surged again in 2021–2022.")
                    st.markdown("Public discussions resumed on **targeting subsidies** more efficiently.")
           
 
        with tab3:
            st.expander("🔬 Future Research Directions:")
            st.markdown("While this dashboard presents a foundational overview of fuel subsidy reforms and their macroeconomic implications, several key areas remain for future exploration:")
            st.markdown("- **Corruption and Governance**: Investigating how corruption levels and institutional quality influence the outcomes of subsidy reforms.")
            st.markdown("- **Price Stability and Inflation Control**: Analyzing how reforms affect long-term price stability and the credibility of monetary policy.")
            st.markdown("- **Equity and Social Impact**: Studying the distributional consequences of subsidy removal on different income groups.")
            st.markdown("- **Subnational Variations**: Exploring regional disparities in reform impacts within each country.")
            st.markdown("- **Data Gaps**: Filling missing time-series data and integrating more granular indicators such as fuel price pass-through, shadow economy effects, and enforcement mechanisms.")
            st.markdown("These aspects are currently under development and will be integrated into future updates of this dashboard.")


    elif indo_page == "Download":
        st.sidebar.markdown("---")
        st.sidebar.markdown("📥 Download Processed Data")

        def filedownload(df):
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="Indonisa_Reform_Filtered.csv">Download CSV</a>'
            return href

        st.markdown(filedownload(df_indo), unsafe_allow_html=True)
        


# ============================== PAGE CONTENT Mexico ===============================
df_Mx=load_Mexico_data()
st.dataframe(df_Mx)

if country == "Mexico":

    if Mx_page == "Overview":
        st.title("Mexico Fuel Subsidy Reform Dashboard - Overview")
        year_min, year_max = int(df_Mx['Year'].min()), int(df_Mx['Year'].max())
        selected_years = st.slider("Select Year Range", year_min, year_max, (year_min, year_max))
        df_filtered = df_Mx[(df_Mx['Year'] >= selected_years[0]) & (df_Mx['Year'] <= selected_years[1])]

        trend_vars = ["Fuel_Price_USD_per_Liter", "Fuel_Consumption_Liter_per_HH", "Gini_Index", "Cash_Transfer_USD_per_person_per_month"]
        fig = px.line(df_filtered, x="Year", y=trend_vars, markers=True,
                      labels={"value": "Value", "variable": "Variable"},
                      title="Trends of Key Variables in Mexico")
        st.plotly_chart(fig, use_container_width=True)
        with st.expander("Show Raw Data"):
            st.dataframe(df_filtered)

    elif Mx_page == "Correlation":
        st.title("Correlation Matrix of Key Variables (df_Mx)")
        vars_corr = ["Fuel_Price_USD_per_Liter", "Fuel_Subsidy_perc_GDP", "Fuel_Consumption_Liter_per_HH",
                     "Consumption_Change_pct", "Gini_Index", "Poverty_Rate_pct", "Cash_Transfer_USD_per_person_per_month"]
        df_corr = df_Mx[vars_corr].dropna()
        scaler = StandardScaler()
        df_scaled = pd.DataFrame(scaler.fit_transform(df_corr), columns=vars_corr)
        corr = df_scaled.corr().round(2)
        z = corr.values
        fig = ff.create_annotated_heatmap(z, x=corr.columns.tolist(), y=corr.index.tolist(), colorscale='RdBu')
        st.plotly_chart(fig, use_container_width=True)

    elif Mx_page == "Causal Diagram":
        st.subheader("Causal Diagram Based on Correlation")
        G = nx.DiGraph()
        edges_mx = [("Fuel_Price", "Fuel_Subsidy", "-"),
                    ("Fuel_Price", "Fuel_Consumption", "-"),
                    ("Fuel_Price", "Cash_Transfer", "+"),
                    ("Fuel_Price", "Gini_Index", "+"),
                    ("Fuel_Price", "Poverty_Rate", "+"),
                    ("Fuel_Subsidy", "Consumption_Change", "+"),
                    ("Fuel_Subsidy", "Gini", "+"),
                    ("Fuel_Subsidy", "Poverty_Rate", "+"),
                    ("Fuel_Consumption", "Consumption_Change", "+"),
                    ("Cash_Transfer", "Gini", "-"),
                    ("Cash_Transfer", "Poverty_Rate", "-"),
                    ("Gini", "Poverty_Rate", "+")]

        for src, dst, sign in edges_mx:
            G.add_edge(src, dst, sign=sign)
        pos_mx = {"Fuel_Price": (-3, 1),"Fuel_Subsidy": (-1.5, 2),
                      "Fuel_Consumption": (-1.5, 0),
                      "Cash_Transfer": (-1.5, -2),
                      "Consumption_Change": (0.5, 0.5),"Gini": (2, 1),
                      "Gini_Index": (-0.5, 1.7),"Poverty_Rate": (3.5, 1)}
        plt.figure(figsize=(14, 8))
        nx.draw_networkx_nodes(G, pos_mx, node_color="lightblue", node_size=2200)
        nx.draw_networkx_labels(G, pos_mx, font_size=9)
        edge_colors = ['green' if G[u][v]['sign'] == '+' else 'red' for u, v in G.edges()]
        nx.draw_networkx_edges(G, pos_mx, edge_color=edge_colors, arrowsize=20)
        edge_labels = nx.get_edge_attributes(G, "sign")
        nx.draw_networkx_edge_labels(G, pos_mx, edge_labels=edge_labels, font_color="red", font_size=10)
        plt.title("Causal Diagram based on Correlation Matrix – Mexico", fontsize=15)
        plt.axis("off")
        plt.tight_layout()
        st.pyplot(plt)
        plt.clf()

    elif Mx_page == "Cost-Benefit":
        st.title("Cost-Benefit Analysis Summary")
        df_cb = df_Mx.dropna(subset=["Fuel_Subsidy_perc_GDP", "Cash_Transfer_USD_per_person_per_month", "Gini_Index"])
        avg_subsidy = df_cb["Fuel_Subsidy_perc_GDP"].mean()
        avg_transfer = df_cb["Cash_Transfer_USD_per_person_per_month"].mean()
        gini_change = df_cb["Gini_Index"].iloc[-1] - df_cb["Gini_Index"].iloc[0]
        st.markdown(f"- 🧾 **Avg Subsidy (% of GDP):** `{avg_subsidy:.2f}`")
        st.markdown(f"- 💸 **Avg Cash Transfer:** `{avg_transfer:.2f} USD`")
        st.markdown(f"- 📉 **Change in Gini Index:** `{gini_change:.3f}`")

    elif Mx_page == "Elasticity":
        st.title("Fuel Price Elasticity by President")
        st.markdown("Elasticity = %Δ Consumption / %Δ Price")
        presidents_list = df_Mx["president"].dropna().unique()

        results = []
        for p in presidents_list:
            df_pres = df_Mx[df_Mx["president"] == p].dropna(subset=["Fuel_Price_USD_per_Liter",
                                                                         "Fuel_Consumption_Liter_per_HH"])
            if len(df_pres) >= 2:
                price_change = (df_pres["Fuel_Price_USD_per_Liter"].iloc[-1] - df_pres["Fuel_Price_USD_per_Liter"].iloc[0]) / df_pres["Fuel_Price_USD_per_Liter"].iloc[0]
                cons_change = (df_pres["Fuel_Consumption_Liter_per_HH"].iloc[-1] - df_pres["Fuel_Consumption_Liter_per_HH"].iloc[0]) / df_pres["Fuel_Consumption_Liter_per_HH"].iloc[0]
                elasticity = cons_change / price_change if price_change != 0 else None
                results.append({"president": p, "Elasticity": round(elasticity, 2)})

        df_elas = pd.DataFrame(results)
        st.dataframe(df_elas)

        fig = px.bar(df_elas, x="president", y="Elasticity", color="president",
                    text="Elasticity",
                    title="Elasticity of Fuel Demand under Each President",
                    labels={"Elasticity": "Elasticity (Consumption/Price)"})
        st.plotly_chart(fig, use_container_width=True)


    elif Mx_page == "Presidents and Policy Map":
        tab1, tab2, tab3= st.tabs(["President Trends", "Static Policy Map","Future Research Directions"])

        with tab1:
            st.subheader("📊 Trends by President")
            president_options = ["All"] + sorted(df_Mx["president"].dropna().unique())
            selected_president = st.selectbox("Select President", president_options)
            selected_var = st.selectbox("Select Variable",
                                        ["Fuel_Price_USD_per_Liter",
                                         "Fuel_Consumption_Liter_per_HH",
                                         "Fuel_Subsidy_perc_GDP",
                                         "Cash_Transfer_USD_per_person_per_month",
                                         "Gini_Index", "Poverty_Rate_pct"])

            if selected_president != "All":
                df_president = df_Mx[df_Mx["president"] == selected_president]
                df_president = df_Mx[df_Mx["president"] == selected_president]
            else:
                df_president = df_Mx.copy()

            filtered_summary=df_president[
                    ['Fuel_Price_USD_per_Liter',
                     'Fuel_Consumption_Liter_per_HH',
                     'Fuel_Subsidy_perc_GDP','Gini_Index']]

            summary_df = filtered_summary.describe()
            avg_price = summary_df.loc["mean", "Fuel_Price_USD_per_Liter"]
            avg_cons = summary_df.loc["mean", "Fuel_Consumption_Liter_per_HH"]
            avg_subsidy = summary_df.loc["mean", "Fuel_Subsidy_perc_GDP"]
            avg_gini = summary_df.loc["mean", "Gini_Index"]
            st.markdown(f"""### 🧾 Summary for President **{selected_president}**:
    - 🛢️ Avg Fuel Price: `{avg_price:.2f} USD/L`
    - ⛽ Avg Fuel Consumption: `{avg_cons:.2f} L/HH`
    - 💰 Avg Fuel Subsidy: `{avg_subsidy:.2f}% of GDP`
    - 📉 Avg Gini Index: `{avg_gini:.3f}`
    """)
            # Line chart for selected variable
            if "Year" in df_president.columns:
                chart = alt.Chart(df_president).mark_line(point=True).encode(
                    x='Year:O',y=alt.Y(f'{selected_var}:Q',
                                       title=selected_var.replace("_", " ")),
                    tooltip=['Year', selected_var]).properties(width=700,
                                                               height=400,
                                                               title=f"{selected_var.replace('_', ' ')} Trend under {selected_president}")
                st.altair_chart(chart, use_container_width=True)

        with tab2:
            st.subheader("🗺 Reform Policy Map")
            st.markdown("Select a Mexican president from the dropdown to view their fuel subsidy reform policies and broader economic agenda.")
            president_options = ["Vicente Fox (2000–2006)",
                                 "Felipe Calderón (2006–2012)",
                                 "Enrique Peña Nieto (2012–2018)",
                                 "Andrés Manuel López Obrador (2018–present)"]
            selected_president = st.selectbox("Choose President",
                                              president_options)

            if selected_president.startswith("Vicente Fox"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    vicente_image_path = os.path.join("images", "vicente_fox.jpg")
                    st.image(vicente_image_path, use_container_width=True)

                with col2:
                    st.markdown("### 🧾 President: Vicente Fox (2000–2006)")
                    st.markdown("**General Economic Policy:** Market-oriented reforms, NAFTA-driven trade liberalization, and moderate macroeconomic stabilization.")
                    st.markdown("**Fuel Subsidy Reform:**")
                    st.markdown("- Reform Type: *Compensatory Fuel Subsidy Reform*")
                    st.markdown("- Implementation Period: **2005–2006**")
                    st.markdown("- Focused on protecting poor households from global oil price increases through direct transfers.")
                    st.markdown("- Transition support without fully liberalizing prices.")

            if selected_president.startswith("Felipe Calderón"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    Calderón_image_path = os.path.join("images", "Felipe Calderón.jpg")
                    st.image(Calderón_image_path, use_container_width=True)

                with col2:
                    st.markdown("### 🧾 President: Felipe Calderón (2006–2012)")
                    st.markdown("**President Calderón pursued an aggressive fuel subsidy reform focused on **reducing fiscal deficits** and promoting energy market efficiency.")
                    st.markdown("** Key aspects included:**")
                    st.markdown("- Gradual reduction of fuel subsidies with an emphasis on fiscal responsibility.")
                    st.markdown("- Introduction of **targeted cash transfer programs** to protect vulnerable populations Efforts to **increase transparency and reduce corruption** in energy pricing")
                    st.markdown("- Measures to encourage **private sector participation** and energy sector reforms **Managing inflationary pressures** amid global oil price volatility")
                    st.markdown("- The reforms contributed to improved **government budgets** but faced **social challenges** due to rising fuel costs.")
                    

            if selected_president.startswith("Enrique Peña Nieto"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    Nieto_image_path = os.path.join("images", "Nieto.jpg")
                    st.image(Nieto_image_path, use_container_width=True)

                with col2:
                    st.markdown("### 🧾 President: Enrique Peña Nieto (2012–2018)")
                    st.markdown("**Comprehensive Structural Reforms: Implemented major reforms in the energy sector, including **liberalizing fuel prices** and opening the market to **foreign investment**.")
                    st.markdown("Ending State Monopolies: Transitioned state-owned oil and gas companies (such as PEMEX) toward greater competition by **breaking government monopolies**.")
                    st.markdown("Focus on Energy Efficiency: Initiated programs aimed at reducing fuel wastage and promoting more efficient energy consumption.")
                    st.markdown("More Targeted Support: Shifted subsidies toward direct cash transfers for low-income households to better target assistance.")
                    st.markdown("Transparency and Anti-Corruption Efforts: Policies were designed to increase market transparency and reduce corruption in the fuel sector.")
                    st.markdown("Price Stabilization Efforts: Implemented mechanisms to prevent severe fuel price volatility and maintain market stability.")

            if selected_president.startswith("Andrés Manuel López Obrador"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    AMLO_image_path = os.path.join("images", "López.jpg")
                    st.image(AMLO_image_path, use_container_width=True)

                with col2:
                    st.markdown("### 🧾 President:AMLO(2018–Present)")
                    st.markdown("AMLO reversed the prior liberalization efforts by reasserting **state control over the energy sector**. He prioritized **energy sovereignty** and protecting household consumption from global price shocks.")
                    st.markdown("While he **froze fuel price** increases during his early years and **expanded subsidies** via Pemex.")
                    st.markdown("During global fuel price hikes (e.g., COVID-19 recovery and the Ukraine war), AMLO increased fuel subsidies to stabilize domestic prices, using oil export revenues to offset the fiscal burden.")
                    
                    
 
        with tab3:
            st.expander("🔬 Future Research Directions:")
            st.markdown("While this dashboard presents a foundational overview of fuel subsidy reforms and their macroeconomic implications, several key areas remain for future exploration:")
            st.markdown("- **Corruption and Governance**: Investigating how corruption levels and institutional quality influence the outcomes of subsidy reforms.")
            st.markdown("- **Price Stability and Inflation Control**: Analyzing how reforms affect long-term price stability and the credibility of monetary policy.")
            st.markdown("- **Equity and Social Impact**: Studying the distributional consequences of subsidy removal on different income groups.")
            st.markdown("- **Subnational Variations**: Exploring regional disparities in reform impacts within each country.")
            st.markdown("- **Data Gaps**: Filling missing time-series data and integrating more granular indicators such as fuel price pass-through, shadow economy effects, and enforcement mechanisms.")
            st.markdown("These aspects are currently under development and will be integrated into future updates of this dashboard.")
  

         

    elif Mx_page == "Download":
        def filedownload(df):
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="Indonesia_Reform_Filtered.csv">Download CSV</a>'
            return href
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("📥 Download Processed Data")
        
        st.download_button("📄 Download Summary  of Fox policy as PDF",
                           data=pdf_bytes,
                           file_name="fox_policy_summary.pdf",
                            mime="application/pdf")
        st.markdown(filedownload(df_indo), unsafe_allow_html=True)

        
#=======================================Nigeria=============================================================
df_Ng=load_Nigeria_data()
st.dataframe(df_Ng)
if country == "Nigeria":

    if Ng_page == "Overview":
        st.title("Nigeria Fuel Subsidy Reform Dashboard - Overview")
        year_min, year_max = int(df_Ng['Year'].min()), int(df_Ng['Year'].max())
        selected_years = st.slider("Select Year Range", year_min, year_max, (year_min, year_max))
        df_filtered = df_Ng[(df_Ng['Year'] >= selected_years[0]) & (df_Ng['Year'] <= selected_years[1])]

        trend_vars = ["Fuel_Price_USD_per_Liter", "Fuel_Consumption_Liter_per_HH", "Gini_Index", "Cash_Transfer_USD_per_person_per_month"]
        fig = px.line(df_filtered, x="Year", y=trend_vars, markers=True,
                      labels={"value": "Value", "variable": "Variable"},
                      title="Trends of Key Variables in Nigeria")
        st.plotly_chart(fig, use_container_width=True)
        with st.expander("Show Raw Data"):
            st.dataframe(df_filtered)

    elif Ng_page == "Correlation":
        st.title("Correlation Matrix of Key Variables (Nigeria)")
        vars_corr = ["Fuel_Price_USD_per_Liter", "Fuel_Subsidy_perc_GDP", "Fuel_Consumption_Liter_per_HH",
                     "Consumption_Change_pct", "Gini_Index", "Poverty_Rate_pct", "Cash_Transfer_USD_per_person_per_month"]
        df_corr = df_Ng[vars_corr].dropna()
        scaler = StandardScaler()
        df_scaled = pd.DataFrame(scaler.fit_transform(df_corr), columns=vars_corr)
        corr = df_scaled.corr().round(2)
        z = corr.values
        fig = ff.create_annotated_heatmap(z, x=corr.columns.tolist(),
                                          y=corr.index.tolist(), colorscale='RdBu')
        st.plotly_chart(fig, use_container_width=True)

    elif Ng_page == "Causal Diagram":
        st.subheader("Causal Diagram Based on Correlation")
        G = nx.DiGraph()
        edges_ng_final = [("Fuel_Price", "Fuel_Subsidy", "-"),
                          ("Fuel_Price", "Consumption_Change", "-"),
                          ("Fuel_Price", "Gini_Index", "+"),
                          ("Fuel_Price", "Cash_Transfer", "+"),
                          ("Fuel_Subsidy", "Consumption_Change", "+"),
                          ("Fuel_Subsidy", "Fuel_Consumption", "+"),
                          ("Fuel_Subsidy", "Cash_Transfer", "-"),
                          ("Consumption_Change", "Gini_Index", "-"),
                          ("Consumption_Change", "Cash_Transfer", "-"),
                          ("Gini_Index", "Cash_Transfer", "+"),
                          ("Fuel_Consumption", "Poverty_Rate", "-")]

        for src, dst, sign in edges_ng_final:
            G.add_edge(src, dst, sign=sign)

        pos_ng = {"Fuel_Price": (-3, 1),"Fuel_Subsidy": (-1.5, 2),
                      "Fuel_Consumption": (-1.5, 0),
                      "Cash_Transfer": (-1.5, -2),
                      "Consumption_Change": (0.5, 0.5),"Gini_Index": (2, 1),
                      "Poverty_Rate": (3.5, 1)}
        plt.figure(figsize=(14, 8))
        nx.draw_networkx_nodes(G, pos_ng, node_color="lightcoral",
                                   node_size=2200)
        nx.draw_networkx_labels(G, pos_ng, font_size=9)
        edge_colors = ['green' if G[u][v]['sign'] == '+' else 'red' for u, v in G.edges()]
        nx.draw_networkx_edges(G, pos_ng, edge_color=edge_colors, arrowsize=20)
        edge_labels = nx.get_edge_attributes(G, "sign")
        nx.draw_networkx_edge_labels(G, pos_ng, edge_labels=edge_labels, font_color="red", font_size=10)
        plt.title("Causal Diagram based on Correlation Matrix – Nigeria", fontsize=15)
        plt.axis("off")
        plt.tight_layout()
        st.pyplot(plt)
        plt.clf()

    elif Ng_page == "Cost-Benefit":
        st.title("Cost-Benefit Analysis Summary")
        df_cb = df_Ng.dropna(subset=["Fuel_Subsidy_perc_GDP", "Cash_Transfer_USD_per_person_per_month", "Gini_Index"])
        avg_subsidy = df_cb["Fuel_Subsidy_perc_GDP"].mean()
        avg_transfer = df_cb["Cash_Transfer_USD_per_person_per_month"].mean()
        gini_change = df_cb["Gini_Index"].iloc[-1] - df_cb["Gini_Index"].iloc[0]
        st.markdown(f"- 🧾 **Avg Subsidy (% of GDP):** `{avg_subsidy:.2f}`")
        st.markdown(f"- 💸 **Avg Cash Transfer:** `{avg_transfer:.2f} USD`")
        st.markdown(f"- 📉 **Change in Gini Index:** `{gini_change:.3f}`")

    elif Ng_page == "Elasticity":
        st.title("Fuel Price Elasticity by President")
        st.markdown("Elasticity = %Δ Consumption / %Δ Price")
        presidents_list = df_Ng["president"].dropna().unique()

        results = []
        for p in presidents_list:
            df_pres = df_Ng[df_Ng["president"] == p].dropna(
                subset=["Fuel_Price_USD_per_Liter",
                        "Fuel_Consumption_Liter_per_HH"])
            if len(df_pres) >= 2:
                price_change = (df_pres["Fuel_Price_USD_per_Liter"].iloc[-1] - df_pres["Fuel_Price_USD_per_Liter"].iloc[0]) / df_pres["Fuel_Price_USD_per_Liter"].iloc[0]
                cons_change = (df_pres["Fuel_Consumption_Liter_per_HH"].iloc[-1] - df_pres["Fuel_Consumption_Liter_per_HH"].iloc[0]) / df_pres["Fuel_Consumption_Liter_per_HH"].iloc[0]
                elasticity = cons_change / price_change if price_change != 0 else None
                results.append({"president": p, "Elasticity": round(elasticity, 2)})

        df_elas = pd.DataFrame(results)
        st.dataframe(df_elas)

        fig = px.bar(df_elas, x="president", y="Elasticity", color="president",
                    text="Elasticity",
                    title="Elasticity of Fuel Demand under Each President",
                    labels={"Elasticity": "Elasticity (Consumption/Price)"})
        st.plotly_chart(fig, use_container_width=True)


    elif Ng_page == "Presidents and Policy Map":
        tab1, tab2, tab3= st.tabs(["President Trends", "Static Policy Map","Future Research Directions"])

        with tab1:
            st.subheader("📊 Trends by President")
            president_options = ["All"] + sorted(df_Ng["president"].dropna().unique())
            selected_president = st.selectbox("Select President", president_options)
            selected_var = st.selectbox("Select Variable",
                                        ["Fuel_Price_USD_per_Liter",
                                         "Fuel_Consumption_Liter_per_HH",
                                         "Fuel_Subsidy_perc_GDP",
                                         "Cash_Transfer_USD_per_person_per_month",
                                         "Gini_Index", "Poverty_Rate_pct"])

            if selected_president != "All":
                df_president = df_Ng[df_Ng["president"] == selected_president]
                df_president = df_Ng[df_Ng["president"] == selected_president]
            else:
                df_president = df_Ng.copy()

            filtered_summary=df_president[
                    ['Fuel_Price_USD_per_Liter',
                     'Fuel_Consumption_Liter_per_HH',
                     'Fuel_Subsidy_perc_GDP','Gini_Index']]

            summary_df = filtered_summary.describe()
            avg_price = summary_df.loc["mean", "Fuel_Price_USD_per_Liter"]
            avg_cons = summary_df.loc["mean", "Fuel_Consumption_Liter_per_HH"]
            avg_subsidy = summary_df.loc["mean", "Fuel_Subsidy_perc_GDP"]
            avg_gini = summary_df.loc["mean", "Gini_Index"]
            st.markdown(f"""### 🧾 Summary for President **{selected_president}**:
    - 🛢️ Avg Fuel Price: `{avg_price:.2f} USD/L`
    - ⛽ Avg Fuel Consumption: `{avg_cons:.2f} L/HH`
    - 💰 Avg Fuel Subsidy: `{avg_subsidy:.2f}% of GDP`
    - 📉 Avg Gini Index: `{avg_gini:.3f}`
    """)
            # Line chart for selected variable
            if "Year" in df_president.columns:
                chart = alt.Chart(df_president).mark_line(point=True).encode(
                    x='Year:O',y=alt.Y(f'{selected_var}:Q',
                                       title=selected_var.replace("_", " ")),
                    tooltip=['Year', selected_var]).properties(width=700,
                                                               height=400,
                                                               title=f"{selected_var.replace('_', ' ')} Trend under {selected_president}")
                st.altair_chart(chart, use_container_width=True)

        with tab2:
            st.subheader("🗺 Reform Policy Map")
            st.markdown("Select a Nigerian president from the dropdown to view their fuel subsidy reform policies and broader economic agenda.")
            president_options = ["Olusegun Obasanjo (1999–2007)",
                                 "Umaru Musa Yar’Adua (2007–2010)",
                                 "Goodluck Jonathan (2010–2015)",
                                 "Muhammadu Buhari (2015–2023)",
                                 ]
            selected_president = st.selectbox("Choose President",
                                              president_options)

            if selected_president.startswith("Olusegun Obasanjo"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    Obasanjo_image_path = os.path.join("images", "Olusegun Obasanjo.jpg")
                    st.image(Obasanjo_image_path, use_container_width=True)

                with col2:
                    st.markdown("### 🧾 President: Olusegun Obasanjo (1999–2007)")
                    st.markdown("**General Economic Policy:** Economic liberalization, structural adjustment continuation, and **anti-corruption** initiatives.")
                    st.markdown("**Fuel Subsidy Reform:**")
                    st.markdown("- Limited fuel subsidy reforms; focus on gradual fiscal consolidation.")
                    st.markdown("- Emphasized economic stabilization and attracting foreign investment.")

            if selected_president.startswith("Umaru Musa Yar’Adua"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    Musa_image_path = os.path.join("images", "Umaru Musa Yar’Adua.jpg")
                    st.image(Musa_image_path, use_container_width=True)

                with col2:
                    st.markdown("### 🧾 President: Umaru Musa Yar’Adua (2007–2010)")
                    st.markdown("**General Economic Policy:** Peace-building, institutional stability, and modest reform attempts.")
                    st.markdown("**Fuel Subsidy Reform:**")
                    st.markdown("- No major subsidy reforms; maintained status quo.")
                    st.markdown("- Focused on improving governance and addressing corruption.")


            if selected_president.startswith("Goodluck Jonathan"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    Jonathan_image_path = os.path.join("images", "Goodluck Jonathan.jpg")
                    st.image(Jonathan_image_path, use_container_width=True)

                with col2:
                    st.markdown("### 🧾 President: Goodluck Jonathan (2010–2015)")
                    st.markdown("**General Economic Policy:** Electoral reforms and incremental liberalization.")
                    st.markdown("**Fuel Subsidy Reform:**")
                    st.markdown("- Attempted abrupt subsidy removal in 2012, which triggered widespread protests.")
                    st.markdown("- Resulted in partial rollback and cautious policy adjustments.")

            if selected_president.startswith("Muhammadu Buhari"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    Buhari_image_path = os.path.join("images", "Muhammadu Buhari.jpg")
                    st.image(Buhari_image_path, use_container_width=True)

                with col2:
                    st.markdown("### 🧾 President: Muhammadu Buhari (2015–2023)")
                    st.markdown("**General Economic Policy:** Anti-corruption and subsidy reduction.")
                    st.markdown("**Fuel Subsidy Reform:**")
                    st.markdown("- Implemented phased subsidy removal starting in 2016.")
                    st.markdown("- Aimed at fiscal consolidation, market liberalization, and reduced government burden.")

                    
 
        with tab3:
            st.expander("🔬 Future Research Directions:")
            st.markdown("While this dashboard presents a foundational overview of fuel subsidy reforms and their macroeconomic implications, several key areas remain for future exploration:")
            st.markdown("- **Corruption and Governance**: Investigating how corruption levels and institutional quality influence the outcomes of subsidy reforms.")
            st.markdown("- **Price Stability and Inflation Control**: Analyzing how reforms affect long-term price stability and the credibility of monetary policy.")
            st.markdown("- **Equity and Social Impact**: Studying the distributional consequences of subsidy removal on different income groups.")
            st.markdown("- **Subnational Variations**: Exploring regional disparities in reform impacts within each country.")
            st.markdown("- **Data Gaps**: Filling missing time-series data and integrating more granular indicators such as fuel price pass-through, shadow economy effects, and enforcement mechanisms.")
            st.markdown("These aspects are currently under development and will be integrated into future updates of this dashboard.")
  

         

    elif Ng_page == "Download":
        def filedownload(df):
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="Indonesia_Reform_Filtered.csv">Download CSV</a>'
            return href
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("📥 Download Processed Data")
        
        st.download_button("📄 Download Summary  of Fox policy as PDF",
                           data=pdf_bytes,
                           file_name="fox_policy_summary.pdf",
                            mime="application/pdf")
        st.markdown(filedownload(df_indo), unsafe_allow_html=True)

#=======================================Egypt=============================================================
df_Eg=load_Egypt_data()
st.dataframe(df_Eg)
if country == "Egypt":

    if Eg_page == "Overview":
        st.title("Egypt Fuel Subsidy Reform Dashboard - Overview")
        year_min, year_max = int(df_Eg['Year'].min()), int(df_Eg['Year'].max())
        selected_years = st.slider("Select Year Range", year_min, year_max, (year_min, year_max))
        df_filtered = df_Eg[(df_Eg['Year'] >= selected_years[0]) & (df_Eg['Year'] <= selected_years[1])]

        trend_vars = ["Fuel_Price_USD_per_Liter", "Fuel_Consumption_Liter_per_HH", "Gini_Index", "Cash_Transfer_USD_per_person_per_month"]
        fig = px.line(df_filtered, x="Year", y=trend_vars, markers=True,
                      labels={"value": "Value", "variable": "Variable"},
                      title="Trends of Key Variables in Egypt")
        st.plotly_chart(fig, use_container_width=True)
        with st.expander("Show Raw Data"):
            st.dataframe(df_filtered)

    elif Eg_page == "Correlation":
        st.title("Correlation Matrix of Key Variables (Egypt)")
        vars_corr = ["Fuel_Price_USD_per_Liter", "Fuel_Subsidy_perc_GDP", "Fuel_Consumption_Liter_per_HH",
                     "Consumption_Change_pct", "Gini_Index", "Poverty_Rate_pct", "Cash_Transfer_USD_per_person_per_month"]
        df_corr = df_Eg[vars_corr].dropna()
        scaler = StandardScaler()
        df_scaled = pd.DataFrame(scaler.fit_transform(df_corr), columns=vars_corr)
        corr = df_scaled.corr().round(2)
        z = corr.values
        fig = ff.create_annotated_heatmap(z, x=corr.columns.tolist(),
                                          y=corr.index.tolist(), colorscale='RdBu')
        st.plotly_chart(fig, use_container_width=True)

    elif Eg_page == "Causal Diagram":
        st.subheader("Causal Diagram Based on Correlation")
        variables_Eg = [
        "Fuel_Price", "Subsidy", "Fuel_Consumption", "Consumption_Change",
        "Gini", "Poverty_Rate", "Cash_Transfer"]
        G.add_nodes_from(variables_Eg)
        edges_Eg = [("Fuel_Price", "Subsidy", "-"),("Fuel_Price", "Fuel_Consumption", "+"),
                    ("Fuel_Price", "Consumption_Change", "+"),
                    ("Fuel_Price", "Gini", "-"),
                    ("Fuel_Price", "Poverty_Rate", "+"),
                    ("Fuel_Price", "Cash_Transfer", "+"),
                    ("Subsidy", "Fuel_Consumption", "-"),
                    ("Subsidy", "Consumption_Change", "-"),
                    ("Subsidy", "Gini", "+"),
                    ("Subsidy", "Poverty_Rate", "-"),
                    ("Subsidy", "Cash_Transfer", "-"),
                    ("Fuel_Consumption", "Consumption_Change", "+"),
                    ("Fuel_Consumption", "Poverty_Rate", "+"),
                    ("Fuel_Consumption", "Cash_Transfer", "+"),
                    ("Consumption_Change", "Cash_Transfer", "+"),
                    ("Gini", "Poverty_Rate", "+"),
                    ("Gini", "Cash_Transfer", "-"),
                    ("Poverty_Rate", "Cash_Transfer", "+")]
        for u, v, sign in edges_Eg:
            G.add_edge(u, v, sign=sign)
        fig, ax = plt.subplots(figsize=(14, 10))
        pos = nx.spring_layout(G, seed=42)
        nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=1500, ax=ax)
        edge_colors = ["green" if G[u][v]["sign"] == "+" else "red" for u, v in G.edges()]
        nx.draw_networkx_edges(G, pos, edge_color=edge_colors, arrows=True, arrowstyle='->', width=2, ax=ax)
        edge_labels = {(u, v): G[u][v]["sign"] for u, v in G.edges()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=14, font_weight="bold", ax=ax)
        ax.set_title("Egypt Fuel Reform - Causal Graph (+/- Correlations)", fontsize=16)
        ax.axis("off")
        st.pyplot(fig)

    elif Eg_page == "Cost-Benefit":
        st.title("Cost-Benefit Analysis Summary")
        df_cb = df_Eg.dropna(subset=["Fuel_Subsidy_perc_GDP", "Cash_Transfer_USD_per_person_per_month", "Gini_Index"])
        avg_subsidy = df_cb["Fuel_Subsidy_perc_GDP"].mean()
        avg_transfer = df_cb["Cash_Transfer_USD_per_person_per_month"].mean()
        gini_change = df_cb["Gini_Index"].iloc[-1] - df_cb["Gini_Index"].iloc[0]
        st.markdown(f"- 🧾 **Avg Subsidy (% of GDP):** `{avg_subsidy:.2f}`")
        st.markdown(f"- 💸 **Avg Cash Transfer:** `{avg_transfer:.2f} USD`")
        st.markdown(f"- 📉 **Change in Gini Index:** `{gini_change:.3f}`")

    elif Eg_page == "Elasticity":
        st.title("Fuel Price Elasticity by President")
        st.markdown("Elasticity = %Δ Consumption / %Δ Price")
        presidents_list = df_Eg["president"].dropna().unique()

        results = []
        for p in presidents_list:
            df_pres = df_Eg[df_Eg["president"] == p].dropna(
                subset=["Fuel_Price_USD_per_Liter",
                        "Fuel_Consumption_Liter_per_HH"])
            if len(df_pres) >= 2:
                price_change = (df_pres["Fuel_Price_USD_per_Liter"].iloc[-1] - df_pres["Fuel_Price_USD_per_Liter"].iloc[0]) / df_pres["Fuel_Price_USD_per_Liter"].iloc[0]
                cons_change = (df_pres["Fuel_Consumption_Liter_per_HH"].iloc[-1] - df_pres["Fuel_Consumption_Liter_per_HH"].iloc[0]) / df_pres["Fuel_Consumption_Liter_per_HH"].iloc[0]
                elasticity = cons_change / price_change if price_change != 0 else None
                results.append({"president": p, "Elasticity": round(elasticity, 2)})

        df_elas = pd.DataFrame(results)
        st.dataframe(df_elas)

        fig = px.bar(df_elas, x="president", y="Elasticity", color="president",
                    text="Elasticity",
                    title="Elasticity of Fuel Demand under Each President",
                    labels={"Elasticity": "Elasticity (Consumption/Price)"})
        st.plotly_chart(fig, use_container_width=True)


    elif Eg_page == "Presidents and Policy Map":
        tab1, tab2, tab3= st.tabs(["President Trends", "Static Policy Map","Future Research Directions"])

        with tab1:
            st.subheader("📊 Trends by President")
            president_options = ["All"] + sorted(df_Eg["president"].dropna().unique())
            selected_president = st.selectbox("Select President", president_options)
            selected_var = st.selectbox("Select Variable",
                                        ["Fuel_Price_USD_per_Liter",
                                         "Fuel_Consumption_Liter_per_HH",
                                         "Fuel_Subsidy_perc_GDP",
                                         "Cash_Transfer_USD_per_person_per_month",
                                         "Gini_Index", "Poverty_Rate_pct"])

            if selected_president != "All":
                df_president = df_Eg[df_Eg["president"] == selected_president]
                df_president = df_Eg[df_Eg["president"] == selected_president]
            else:
                df_president = df_Eg.copy()

            filtered_summary=df_president[
                    ['Fuel_Price_USD_per_Liter',
                     'Fuel_Consumption_Liter_per_HH',
                     'Fuel_Subsidy_perc_GDP','Gini_Index']]

            summary_df = filtered_summary.describe()
            avg_price = summary_df.loc["mean", "Fuel_Price_USD_per_Liter"]
            avg_cons = summary_df.loc["mean", "Fuel_Consumption_Liter_per_HH"]
            avg_subsidy = summary_df.loc["mean", "Fuel_Subsidy_perc_GDP"]
            avg_gini = summary_df.loc["mean", "Gini_Index"]
            st.markdown(f"""### 🧾 Summary for President **{selected_president}**:
    - 🛢️ Avg Fuel Price: `{avg_price:.2f} USD/L`
    - ⛽ Avg Fuel Consumption: `{avg_cons:.2f} L/HH`
    - 💰 Avg Fuel Subsidy: `{avg_subsidy:.2f}% of GDP`
    - 📉 Avg Gini Index: `{avg_gini:.3f}`
    """)
            # Line chart for selected variable
            if "Year" in df_president.columns:
                chart = alt.Chart(df_president).mark_line(point=True).encode(
                    x='Year:O',y=alt.Y(f'{selected_var}:Q',
                                       title=selected_var.replace("_", " ")),
                    tooltip=['Year', selected_var]).properties(width=700,
                                                               height=400,
                                                               title=f"{selected_var.replace('_', ' ')} Trend under {selected_president}")
                st.altair_chart(chart, use_container_width=True)

        with tab2:
            st.subheader("🗺 Reform Policy Map")
            st.markdown("Select a Egyption president from the dropdown to view their fuel subsidy reform policies and broader economic agenda.")
            president_options = ["Hosni Mubarak (1981–2011)",
                                 "SCAF (2011)",
                                 "Mohamed Morsi (2012–2013)",
                                 "Abdel Fattah el-Sisi (2014–present)"]
                                 
            selected_president = st.selectbox("Choose President",
                                              president_options)

            if selected_president.startswith("Hosni Mubarak"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    Mubarak_image_path = os.path.join("images", "Hosni Mubarak.jpg")
                    st.image("Hosni Mubarak.jpg", use_container_width=True)

                with col2:
                    st.markdown("### 🧾 President: Hosni Mubarak (1981–2011)")
                    st.markdown("**General Economic Policy:** Gradual liberalization, privatization of state assets, and alignment with IMF prescriptions in the 1990s.")
                    st.markdown("**Fuel Subsidy Reform:**")
                    st.markdown("- Fuel subsidies remained largely intact throughout his rule.")
                    st.markdown("- Attempts at reform were politically sensitive and limited in scope.")

            if selected_president.startswith("SCAF"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    SCAF_image_path = os.path.join("images", "Arab Spring.jpg")
                    st.image(SCAF_image_path, use_container_width=True)

                with col2:
                   st.markdown("### 🧾 Transitional Authority: Supreme Council of the Armed Forces (SCAF) – 2011")
                   st.markdown("**Context:** Following the 2011 Egyptian Revolution—part of the wider *Arab Spring* movement that swept across the Middle East and North Africa—President Hosni Mubarak stepped down after nearly 30 years in power. The Supreme Council of the Armed Forces (SCAF) assumed interim control of the country.")
                   st.markdown("**General Economic Policy:**")
                   st.markdown("- Short-term stabilization and crisis management.")
                   st.markdown("- Navigated severe economic uncertainty amid social unrest and declining tourism revenue.")
                   st.markdown("**Fuel Subsidy Reform:**")
                   st.markdown("- No significant fuel subsidy reforms.")
                   st.markdown("- Maintained existing subsidy structure to preserve social stability during the transition.")

            if selected_president.startswith("Mohamed Morsi"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    Morsi_image_path = os.path.join("images", "Mohamed Morsi.jpg")
                    st.image(Morsi_image_path,use_container_width=True)

                with col2:
                     st.markdown("### 🧾 President: Mohamed Morsi (2012–2013)")
                     st.markdown("**General Economic Policy:** Islamist-leaning development agenda with efforts to renegotiate IMF loans.")
                     st.markdown("**Fuel Subsidy Reform:**")
                     st.markdown("- Initial attempts to rationalize subsidies.")
                     st.markdown("- Faced significant political resistance and instability.")

            if selected_president.startswith("Abdel Fattah el-Sisi"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    sisi_image_path = os.path.join("images", "sisi.jpg")
                    st.image(sisi_image_path, use_container_width=True)

                with col2:
                     st.markdown("### 🧾 President: Abdel Fattah el-Sisi (2014–present)")
                     st.markdown("**General Economic Policy:** Aggressive economic reform with IMF-backed austerity measures and infrastructure megaprojects.")
                     st.markdown("**Fuel Subsidy Reform:**")
                     st.markdown("- Major cuts in fuel subsidies starting in 2014.")
                     st.markdown("- Shifted toward targeted cash transfers to mitigate social impacts.")
                    
 
        with tab3:
            st.expander("🔬 Future Research Directions:")
            st.markdown("While this dashboard presents a foundational overview of fuel subsidy reforms and their macroeconomic implications, several key areas remain for future exploration:")
            st.markdown("- **Corruption and Governance**: Investigating how corruption levels and institutional quality influence the outcomes of subsidy reforms.")
            st.markdown("- **Price Stability and Inflation Control**: Analyzing how reforms affect long-term price stability and the credibility of monetary policy.")
            st.markdown("- **Equity and Social Impact**: Studying the distributional consequences of subsidy removal on different income groups.")
            st.markdown("- **Subnational Variations**: Exploring regional disparities in reform impacts within each country.")
            st.markdown("- **Data Gaps**: Filling missing time-series data and integrating more granular indicators such as fuel price pass-through, shadow economy effects, and enforcement mechanisms.")
            st.markdown("These aspects are currently under development and will be integrated into future updates of this dashboard.")
  

         

    elif Mx_page == "Download":
        def filedownload(df):
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="Indonesia_Reform_Filtered.csv">Download CSV</a>'
            return href
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("📥 Download Processed Data")
        
        st.download_button("📄 Download Summary  of Fox policy as PDF",
                           data=pdf_bytes,
                           file_name="fox_policy_summary.pdf",
                            mime="application/pdf")
        st.markdown(filedownload(df_indo), unsafe_allow_html=True)
        
