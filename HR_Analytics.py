import numpy as np
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import os
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")


#set up page title and icon
st.set_page_config(page_title = "HR_Analytics", page_icon = "📉", layout = "wide")
st.title("📈 HR_Analytics DashBoard" )
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html = True)


# set up side bar
st.sidebar.image("logo1.jfif")


# uploading data for the dashboard
fl = st.sidebar.file_uploader("🗂 Upload a  file", type = (["csv","txt","xlsx","xls"]))
if fl is not None:
	filename = fl.name
	st.write(filename)
	df = pd.read_csv(filename)
else:
	os.chdir(os.getcwd())
	df = pd.read_csv("HR_cleanData.csv")


# creating side filters
st.sidebar.header("Please Choose Filter")

Work_type  = st.sidebar.multiselect("Filter by Work Type", df["WorkType"].unique())
if not Work_type:
	df1 = df.copy()
else:
	df1 = df[df["WorkType"].isin(Work_type)]

Business_unit = st.sidebar.multiselect("Filter by Business Unit", df["BusinessUnit"].unique())
if not Business_unit:
	df2 = df1.copy()
else:
	df2 = df1[df["BusinessUnit"].isin(Business_unit)]

Cost_centre = st.sidebar.multiselect("Filter by Cost Centre", df["CostCentre"].unique())

if not Work_type and not Business_unit and not Cost_centre:
	df_selection = df
elif not Business_unit and not Cost_centre:
	df_selection = df[df["WorkType"].isin(Work_type)]
elif not Work_type and not Cost_centre:
	df_selection = df[df["BusinessUnit"].isin(Business_unit)]
elif Business_unit and Cost_centre:
	df_selection = df2[df["BusinessUnit"].isin(Business_unit) & df2["CostCentre"].isin(Cost_centre)]
elif Work_type and Cost_centre:
	df_selection = df2[df["WorkType"].isin(Work_type) & df2["CostCentre"].isin(Cost_centre)]
elif Work_type and Business_unit:
	df_selection = df2[df["WorkType"].isin(Work_type) & df2["BusinessUnit"].isin(Business_unit)]
elif Cost_centre:
	df_selection = df2[df2["CostCentre"].isin(Cost_centre)]
else:
	df_selection = df2[df2["WorkType"].isin(Work_type) & df2["BusinessUnit"].isin(Business_unit) & df2["CostCentre"].isin(Cost_centre)]



# creating top KPI's
def kpi():
	total_salary =int(df_selection["CurrentSalary"].sum())
	avg_salary = round(df_selection["CurrentSalary"].mean(),2)
	avg_rating = int(round(df_selection["CurrentEmployeeRating"].mean(),0))
	avg_star_rating = "⭐" * int(avg_rating)
	col1, col2, col3 = st.columns(3)
	with col1:
		st.info("Total Salary", icon = "📌")
		st.metric(label = "sumSalary", value = f"US $ {total_salary:,}")
	with col2:
		st.info("Average Salary", icon = "📌")
		st.metric(label = "avgSalary",value = f"US $ {avg_salary:,}")
	with col3:
		st.info(f"Average Rating", icon = "📌")
		st.metric(label = "avgRating",value = f"{avg_rating} {avg_star_rating}")

kpi()

# creating  pie charts
col1, col2 = st.columns(2)
with col1:
	cl1, cl2 = st.columns(2)
	with cl1:
		category_df = df_selection.groupby(by = ("BusinessUnit"), as_index = False)["CurrentSalary"].sum()
		category_df.sort_values(by = "CurrentSalary", ascending = True, inplace = True)
		fig = px.bar(category_df, x = "CurrentSalary",y = "BusinessUnit", title = "Salary by Business Unit",orientation = "h", 
			text = ["${:,.2f}".format(x) for x in category_df["CurrentSalary"]], template = "seaborn")
		st.plotly_chart(fig, use_container_width = True)


	with cl2:
		df_selection["HireDate"] = pd.to_datetime(df_selection["HireDate"])
		df_selection["Year"] = df_selection["HireDate"].dt.to_period("Y")
		linechart  = pd.DataFrame(df_selection.groupby(df_selection["Year"].dt.strftime("%Y")).sum()["CurrentSalary"]).reset_index()
		fig2 = px.line(linechart, x = "Year", y = "CurrentSalary",title = "Current Salary by Year", height = 500, width = 1000, template = "gridon")
		st.plotly_chart(fig2, use_container_width=True)


with col2:
		fig = px.pie(df_selection, values= "CurrentSalary", names = "WorkType", title = "Salary based on WorkType", hole = 0.5)
		fig.update_traces(text = df_selection["WorkType"], textposition = "outside")
		st.plotly_chart(fig, use_container_width = True)
	

columns1, columns2 = st.columns(2)
with columns1:
	c1, c2 = st.columns(2)
	with c1:
		category_df = df_selection.groupby(by = ("CostCentre"), as_index = False)["CurrentSalary"].sum()
		category_df.sort_values(by = "CurrentSalary", ascending = True, inplace = True)
		fig = px.bar(category_df, x = "CurrentSalary",y = "CostCentre",title = "Salary by CostCentre",orientation = "h", 
		text = ["${:,.2f}".format(x) for x in category_df["CurrentSalary"]], template = "seaborn")
		st.plotly_chart(fig, use_container_width = True)
	with c2:
		fig = px.pie(df_selection, values= "CurrentSalary", names = "Gender", title = "Salary based on Gender", hole = 0.5)
		fig.update_traces(text = df_selection["Gender"], textposition = "outside")
		st.plotly_chart(fig, use_container_width = True)	


with columns2:

	category_df = df_selection.groupby(by = (["AgeGroup","RemainsEmployed"]), as_index = False)["CurrentSalary"].sum()
	category_df.sort_values(by = "CurrentSalary", ascending = True, inplace = True)
	fig = px.bar(category_df, x = "CurrentSalary",y = "AgeGroup", color = "RemainsEmployed", orientation = "h", title = "Salary by Age Group", 
			text = ["${:,.2f}".format(x) for x in category_df["CurrentSalary"]], template = "seaborn")
	st.plotly_chart(fig, use_container_width = True)

st.markdown("""<style> [data-testid = column]:nth-of-type(1) [data-testid=stVerticalBlock]{
	gap: 0rem;
	}
	</style>""", unsafe_allow_html = True)

bottom_left_col, bottom_right_col = st.columns(2)
with bottom_left_col:
		rating_df = df.groupby(by = ("BusinessUnit"), as_index= False)["CurrentEmployeeRating"].mean()
		rating_df.sort_values(by = "CurrentEmployeeRating", ascending = True, inplace = True)
		fig = px.bar(rating_df, x = "CurrentEmployeeRating",y = "BusinessUnit", title = "Perfomance by Business Unit",orientation = "h", 
			text = ["{:,.2f}".format(x) for x in rating_df["CurrentEmployeeRating"]], template = "seaborn")
		st.plotly_chart(fig, use_container_width = True)



with bottom_right_col:
	fig2 = px.treemap(df_selection, path = ["EthnicGroup", "CostCentre"], values = "CurrentSalary", hover_data = ["CurrentSalary"], 
		title = "Hierachical View of Salary ",color = "CostCentre")
	st.plotly_chart(fig2, use_container_width = True)






	