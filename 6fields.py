import pandas as pd
import streamlit as st
import openpyxl
import re

df = pd.read_excel('bigdata.xls')
df['Product'] = df['Product'].fillna('nan')
df['Importance'] = df['Importance'].fillna('Null')
unique_therapeutic_areas = df['Therapeutic Area'].fillna('nan').str.strip().str.lower().unique()
unique_product = df['Product'].fillna('nan').str.strip().str.lower().unique()
unique_regions = df['Region'].fillna('nan').str.strip().str.lower().unique()
unique_countries = df['Country'].fillna('nan').str.strip().str.lower().unique()
unique_month = df['Month'].fillna('nan').str.strip().str.lower().unique()
unique_year = df['Year'].unique()
unique_importances = df['Importance'].fillna('nan').str.strip().str.lower().unique()


st.set_page_config(page_title="Insight Report Chatbot", layout="centered")
st.title("Insight Report Chatbot")

# Custom CSS
st.markdown(
    """  
    <style>
    [theme]
    primaryColor="#ffffff"
    backgroundColor="#4bc3ff"
    secondaryBackgroundColor="#00f5e7"
    textColor="#ff0000"


    .main {
        background-color: #4bc3ff;  /* Light background */
    }
    h1 {
        color: ##ffffff;  /* Light blue color for the main title */
    }
    .highlight {
        color: #00f5e7;  /* Orange highlight */
        font-weight: bold;
    }
    .chatbot-box {
        background-color: #e6f7ff;  /* Light blue background for chatbot box */
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #4b8bbe;
    }
    .user-input-box {
        background-color: #ffeadb;  /* Light orange background for input box */
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ff4500;
    }
    .stButton>button {
        background-color: #4682b4; /* Steel blue color for buttons */
        color: white;
    }
    .stButton>button:hover {
        background-color: #ff4500; /* Change color on hover */
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to extract multiple values from a question
def extract_multiple_from_question(question, unique_values):
    extracted = []
    if pd.api.types.is_string_dtype(unique_values):
        for value in unique_values:
            if re.search(rf"\b{re.escape(value.lower())}\b", question.lower()):
                extracted.append(value)
    elif pd.api.types.is_numeric_dtype(unique_values):
        for value in unique_values:
            if re.search(rf"\b{value}\b", question):
                extracted.append(value)
    return extracted

def number_of_insights(question):
    importances = extract_multiple_from_question(question, unique_importances)
    regions = extract_multiple_from_question(question, unique_regions)
    countries = extract_multiple_from_question(question, unique_countries)
    months = extract_multiple_from_question(question, unique_month)
    years = extract_multiple_from_question(question, unique_year)
    products = extract_multiple_from_question(question, unique_product)
    therapeutic_areas = extract_multiple_from_question(question, unique_therapeutic_areas)

    insights_info = []
    total_count = 0
    insights_dfs = []  # List to hold DataFrames for insights
    if importances:
        for importance in importances:
            imp_df=df[df['Importance'].str.lower()==importance.lower()]   
            if therapeutic_areas:
                imp_df =imp_df[imp_df['Therapeutic Area'].isin([i.lower() for i in importances])]
            if regions:
                imp_df =imp_df[imp_df['Region'].str.lower().isin([r.lower() for r in regions])]
            if countries:
                imp_df=imp_df[imp_df['Country'].str.lower().isin([c.lower() for c in countries])]
            if months:
                imp_df = imp_df[imp_df['Month'].str.lower().isin([m.lower() for m in months])]
            if years:
                imp_df = imp_df[imp_df['Year'].isin(years)]
            if products:
                imp_df = imp_df[imp_df['Product'].str.lower().isin([p.lower() for p in products])]

            if not imp_df.empty:
                count=imp_df.shape[0]
                insights_info.append(f"Total insights for {importance} : {count}")
                total_count+= count
                insights_dfs.append(imp_df)
            else:
                insights_info.append(f"No insights available for {importance} in the specified filters.")

        return insights_info, insights_dfs if insights_info else "No insights found for the specified query."

    if therapeutic_areas:
        for area in therapeutic_areas:
            area_df=df[df['Therapeutic Area'].str.lower()==area.lower()]
            if regions:
                area_df=area_df[area_df['Region'].str.lower().isin([r.lower() for r in regions])]
            if countries:
                area_df=area_df[area_df['Country'].str.lower().isin([c.lower() for c in countries])]
            if months:
                area_df = area_df[area_df['Month'].str.lower().isin([m.lower() for m in months])]
            if years:
                area_df = area_df[area_df['Year'].isin(years)]
            if products:
                area_df=area_df[area_df['Product'].str.lower().isin([p.lower() for p in products])]

            if not area_df.empty:
                count=area_df.shape[0]
                insights_info.append(f"Total insights for {area} : {count}")
                total_count+= count
                insights_dfs.append(area_df)
            else:
                insights_info.append(f"No insights available for {area} in the specified filters.")

        return insights_info, insights_dfs if insights_info else "No insights found for the specified query."        

    elif products:
        for product in products:
            product_df=df[df['Product'].str.lower()==product.lower()]
            if regions:
                product_df=product_df[product_df['Region'].str.lower().isin([r.lower() for r in regions])]
            if countries:
                product_df=product_df[product_df['Country'].str.lower().isin([c.lower() for c in countries])]
            if months:
                product_df = product_df[product_df['Month'].str.lower().isin([m.lower() for m in months])]
            if years:
                product_df = product_df[product_df['Year'].isin(years)]

            if not product_df.empty:
                count=product_df.shape[0]
                insights_info.append(f"Total insights for {product} product : {count}")
                total_count+= count
                insights_dfs.append(product_df)
            else:
                insights_info.append(f"No insights available for {product} in the specified filters.")

        return insights_info, insights_dfs if insights_info else "No insights found for the specified query."        

    # Process regions
    elif regions:
        for region in regions:
            region_df = df[df['Region'].str.lower() == region.lower()]
            if countries:
                product_df=product_df[product_df['Country'].str.lower().isin([c.lower() for c in countries])]
            if months:
                region_df = region_df[region_df['Month'].str.lower().isin([m.lower() for m in months])]
            if years:
                region_df = region_df[region_df['Year'].isin(years)]

            if not region_df.empty:
                count = region_df.shape[0]
                insights_info.append(f"Total insights for {region}: {count}")
                total_count += count
                insights_dfs.append(region_df)  # Append the DataFrame for this region
            else:
                insights_info.append(f"No insights found for {region} in the specified query.")

        return insights_info, insights_dfs if insights_info else "No insights found for the specified query."        

    # Process countries
    elif countries:
        for country in countries:
            country_df = df[df['Country'].str.lower() == country.lower()]
            if months:
                country_df = country_df[country_df['Month'].str.lower().isin([m.lower() for m in months])]
            if years:
                country_df = country_df[country_df['Year'].isin(years)]

            if not country_df.empty:
                count = country_df.shape[0]
                insights_info.append(f"Total insights for {country}: {count}")
                total_count += count
                insights_dfs.append(country_df)  # Append the DataFrame for this country
            else:
                insights_info.append(f"No insights found for {country} in the specified query.")

        return insights_info, insights_dfs if insights_info else "No insights found for the specified query."        

    # If no regions or countries were specified
    elif not regions and not countries and not products:
        filtered_df = df
        if months:
            filtered_df = filtered_df[filtered_df['Month'].str.lower().isin([m.lower() for m in months])]
        if years:
            filtered_df = filtered_df[filtered_df['Year'].isin(years)]

        if not filtered_df.empty:
            total_count = filtered_df.shape[0]
            insights_info.append(f"Total insights: {total_count}")
            insights_dfs.append(filtered_df)  # Append the filtered DataFrame
        else:
            insights_info.append("No insights found for the specified query.")

    # Return the insights information and the combined DataFrame
    return insights_info, insights_dfs if insights_info else "No insights found for the specified query."

def highest_insights_by_month(question):
    # Extract filters from the question
    importances = extract_multiple_from_question(question, unique_importances)
    regions = extract_multiple_from_question(question, unique_regions)
    countries = extract_multiple_from_question(question, unique_countries)
    months = extract_multiple_from_question(question, unique_month)
    years = extract_multiple_from_question(question, unique_year)
    products = extract_multiple_from_question(question, unique_product)
    therapeutic_areas = extract_multiple_from_question(question, unique_therapeutic_areas) 

    insights_info = []
    insights_dfs = []  # List to hold DataFrames for insights

    if importances:
        for importance in importances:
            imp_df=df[df['Importance'].str.lower()==importance.lower()]   
            if therapeutic_areas:
                imp_df = imp_df[imp_df['Therapeutic Area'].str.lower().isin([a.lower() for a in therapeutic_areas])]
            if products:
                imp_df = imp_df[imp_df['Product'].str.lower().isin([p.lower() for p in products])]
            if regions:
                imp_df = imp_df[imp_df['Region'].str.lower().isin([r.lower() for r in regions])]
            if countries:
                imp_df = imp_df[imp_df['Country'].str.lower().isin([c.lower() for c in countries])]
            if months:
                imp_df = imp_df[imp_df['Month'].str.lower().isin([m.lower() for m in months])]
            if years:
                imp_df = imp_df[imp_df['Year'].isin(years)]

            # Group by month and find the month with the highest count
            if not imp_df.empty:
                if 'month' in question:
                    month_counts = imp_df.groupby('Month').size().reset_index(name='insight_count')
                    highest_month = month_counts.loc[month_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {importance}, the month with the highest insights is {highest_month['Month']} with {highest_month['insight_count']} insights.")
                    insights_dfs.append(imp_df.loc[imp_df['Month'].str.lower() == (highest_month['Month'].lower())])

                if 'year' in question:
                    year_counts = imp_df.groupby('Year').size().reset_index(name='insight_count')
                    highest_year = year_counts.loc[year_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {importance}, the year with the highest insights is {highest_year['Year']} with {highest_year['insight_count']} insights.")
                    insights_dfs.append(imp_df.loc[imp_df['Year'] == highest_year['Year']])

                if 'country' in question:
                    country_counts = imp_df.groupby('Country').size().reset_index(name='insight_count')
                    highest_country = country_counts.loc[country_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {importance}, the country with the highest insights is {highest_country['Country']} with {highest_country['insight_count']} insights.")
                    insights_dfs.append(imp_df.loc[imp_df['Country'].str.lower() == (highest_country['Country'].lower())])

                if 'region' in question:
                    region_counts = imp_df.groupby('Region').size().reset_index(name='insight_count')
                    highest_region = region_counts.loc[region_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {importance}, the region with the highest insights is {highest_region['Region']} with {highest_region['insight_count']} insights.")
                    insights_dfs.append(imp_df.loc[imp_df['Region'].str.lower() == (highest_region['Region'].lower())])

                if 'product' in question:
                    product_counts = imp_df.groupby('Product').size().reset_index(name='insight_count')
                    highest_product = product_counts.loc[product_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {importance}, the product with the highest insights is {highest_product['Product']} with {highest_product['insight_count']} insights.")
                    insights_dfs.append(imp_df.loc[imp_df['Product'].str.lower() == (highest_product['Product'].lower())])

                if 'therapeutic area' in question:
                    area_counts = imp_df.groupby('Therapeutic Area').size().reset_index(name='insight_count')
                    highest_area = area_counts.loc[area_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {importance}, the area with the highest insights is {highest_area['Therapeutic Area']} with {highest_area['insight_count']} insights.")
                    insights_dfs.append(imp_df.loc[imp_df['Therapeutic Area'].str.lower() == (highest_area['Therapeutic Area'].lower())])

                else:
                    month_counts = product_df.groupby('Month').size().reset_index(name='insight_count')
                    highest_month = month_counts.loc[month_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {product},the highest insights is {highest_month['Month']} with {highest_month['insight_count']} insights.")
                    insights_dfs.append(product_df.loc[product_df['Month'].str.lower() == (highest_month['Month'].lower())])
            else:
                insights_info.append(f"No insights available for {importance} in the specified filters.")

        # Return the insights information and the combined DataFrame
        return insights_info, insights_dfs if insights_info else "No insights found for the specified query."

    # Process based on therapeutic area, product, region, country filters
    if therapeutic_areas:
        for therapeutic_area in therapeutic_areas:
            therapeutic_area_df = df[df['Therapeutic Area'].str.lower() == therapeutic_area.lower()]
            if products:
                therapeutic_area_df = therapeutic_area_df[therapeutic_area_df['Product'].str.lower().isin([p.lower() for p in products])]
            if regions:
                therapeutic_area_df = therapeutic_area_df[therapeutic_area_df['Region'].str.lower().isin([r.lower() for r in regions])]
            if countries:
                therapeutic_area_df = therapeutic_area_df[therapeutic_area_df['Country'].str.lower().isin([c.lower() for c in countries])]
            if months:
                therapeutic_area_df = therapeutic_area_df[therapeutic_area_df['Month'].str.lower().isin([m.lower() for m in months])]
            if years:
                therapeutic_area_df = therapeutic_area_df[therapeutic_area_df['Year'].isin(years)]

            # Group by month and find the month with the highest count
            if not therapeutic_area_df.empty:
                if 'month' in question:
                    month_counts = therapeutic_area_df.groupby('Month').size().reset_index(name='insight_count')
                    highest_month = month_counts.loc[month_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {therapeutic_area}, the month with the highest insights is {highest_month['Month']} with {highest_month['insight_count']} insights.")
                    insights_dfs.append(therapeutic_area_df.loc[therapeutic_area_df['Month'].str.lower() == (highest_month['Month'].lower())])

                if 'year' in question:
                    year_counts = therapeutic_area_df.groupby('Year').size().reset_index(name='insight_count')
                    highest_year = year_counts.loc[year_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {therapeutic_area}, the year with the highest insights is {highest_year['Year']} with {highest_year['insight_count']} insights.")
                    insights_dfs.append(therapeutic_area_df.loc[therapeutic_area_df['Year'] == highest_year['Year']])

                if 'country' in question:
                    country_counts = therapeutic_area_df.groupby('Country').size().reset_index(name='insight_count')
                    highest_country = country_counts.loc[country_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {therapeutic_area}, the country with the highest insights is {highest_country['Country']} with {highest_country['insight_count']} insights.")
                    insights_dfs.append(therapeutic_area_df.loc[therapeutic_area_df['Country'].str.lower() == (highest_country['Country'].lower())])

                if 'region' in question:
                    region_counts = therapeutic_area_df.groupby('Region').size().reset_index(name='insight_count')
                    highest_region = region_counts.loc[region_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {therapeutic_area}, the region with the highest insights is {highest_region['Region']} with {highest_region['insight_count']} insights.")
                    insights_dfs.append(therapeutic_area_df.loc[therapeutic_area_df['Region'].str.lower() == (highest_region['Region'].lower())])

                if 'product' in question:
                    product_counts = therapeutic_area_df.groupby('Product').size().reset_index(name='insight_count')
                    highest_product = product_counts.loc[product_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {importance}, the product with the highest insights is {highest_product['Product']} with {highest_product['insight_count']} insights.")
                    insights_dfs.append(therapeutic_area_df.loc[therapeutic_area_df['Product'].str.lower() == (highest_product['Product'].lower())])

                else:
                    month_counts = product_df.groupby('Month').size().reset_index(name='insight_count')
                    highest_month = month_counts.loc[month_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {product},the highest insights is {highest_month['Month']} with {highest_month['insight_count']} insights.")
                    insights_dfs.append(product_df.loc[product_df['Month'].str.lower() == (highest_month['Month'].lower())])
            else:
                insights_info.append(f"No insights available for {therapeutic_area} in the specified filters.")

        # Return the insights information and the combined DataFrame
        return insights_info, insights_dfs if insights_info else "No insights found for the specified query."

    elif products:
        for product in products:
            product_df = df[df['Product'].str.lower() == product.lower()]
            # Apply region filter
            if regions:
                product_df = product_df[product_df['Region'].str.lower().isin([r.lower() for r in regions])]
            # Apply country filter
            if countries:
                product_df = product_df[product_df['Country'].str.lower().isin([c.lower() for c in countries])]
            # Apply month filter
            if months:
                product_df = product_df[product_df['Month'].str.lower().isin([m.lower() for m in months])]
            # Apply year filter
            if years:
                product_df = product_df[product_df['Year'].isin(years)]

            # Group by month and find the month with the highest count
            if not product_df.empty:
                if 'month' in question:
                    month_counts = product_df.groupby('Month').size().reset_index(name='insight_count')
                    highest_month = month_counts.loc[month_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {product}, the month with the highest insights is {highest_month['Month']} with {highest_month['insight_count']} insights.")
                    insights_dfs.append(product_df.loc[product_df['Month'].str.lower() == (highest_month['Month'].lower())])                

                elif 'year' in question:
                    year_counts = product_df.groupby('Year').size().reset_index(name='insight_count')
                    highest_year = year_counts.loc[year_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {product}, the year with the highest insights is {highest_year['Year']} with {highest_year['insight_count']} insights.")
                    insights_dfs.append(product_df.loc[product_df['Year'].str.lower() == (highest_year['Year'].lower())])

                elif 'country' in question:
                    country_counts = product_df.groupby('Country').size().reset_index(name='insight_count')
                    highest_country = country_counts.loc[country_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {product}, the country with the highest insights is {highest_country['Country']} with {highest_country['insight_count']} insights.")
                    insights_dfs.append(product_df.loc[product_df['Country'].str.lower() == (highest_country['Country'].lower())])
                
                elif 'region' in question:
                    month_region = product_df.groupby('Region').size().reset_index(name='insight_count')
                    highest_region = region_counts.loc[region_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {product}, the region with the highest insights is {highest_region['Region']} with {highest_region['insight_count']} insights.")
                    insights_dfs.append(product_df.loc[product_df['Region'].str.lower() == (highest_region['Region'].lower())])
                
                else:
                    month_counts = product_df.groupby('Month').size().reset_index(name='insight_count')
                    highest_month = month_counts.loc[month_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {product},the highest insights is {highest_month['Month']} with {highest_month['insight_count']} insights.")
                    insights_dfs.append(product_df.loc[product_df['Month'].str.lower() == (highest_month['Month'].lower())])
                
            else:
                insights_info.append(f"No insights available for {product} in the specified filters.")

        # Return the insights information and the combined DataFrame
        return insights_info, insights_dfs if insights_info else "No insights found for the specified query."

    # Process regions when no products are given
    elif regions:
        for region in regions:
            region_df = df[df['Region'].str.lower() == region.lower()]
            # Apply country filter
            if countries:
                region_df = region_df[region_df['Country'].str.lower().isin([c.lower() for c in countries])]
            # Apply month filter
            if months:
                region_df = region_df[region_df['Month'].str.lower().isin([m.lower() for m in months])]
            # Apply year filter
            if years:
                region_df = region_df[region_df['Year'].isin(years)]

            # Group by month and find the month with the highest count
            if not region_df.empty:
                if 'month' in question:
                    month_counts = region_df.groupby('Month').size().reset_index(name='insight_count')
                    highest_month = month_counts.loc[month_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {region}, the month with the highest insights is {highest_month['Month']} with {highest_month['insight_count']} insights.")
                    insights_dfs.append(region_df.loc[region_df['Month'].str.lower() == (highest_month['Month'].lower())])                

                if 'year' in question:
                    year_counts = region_df.groupby('Year').size().reset_index(name='insight_count')
                    highest_year = year_counts.loc[year_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {region}, the year with the highest insights is {highest_year['Year']} with {highest_year['insight_count']} insights.")
                    insights_dfs.append(region_df.loc[region_df['Year'].str.lower() == (highest_year['Year'].lower())])
                
                else:
                    month_counts = product_df.groupby('Month').size().reset_index(name='insight_count')
                    highest_month = month_counts.loc[month_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {product},the highest insights is {highest_month['Month']} with {highest_month['insight_count']} insights.")
                    insights_dfs.append(product_df.loc[product_df['Month'].str.lower() == (highest_month['Month'].lower())])

            else:
                insights_info.append(f"No insights found for {region} in the specified query.")

            return insights_info, insights_dfs if insights_info else "No insights found for the specified query."

    # Process countries when no products or regions are given
    elif countries:
        for country in countries:
            country_df = df[df['Country'].str.lower() == country.lower()]
            # Apply month filter
            if months:
                country_df = country_df[country_df['Month'].str.lower().isin([m.lower() for m in months])]
            # Apply year filter
            if years:
                country_df = country_df[country_df['Year'].isin(years)]

            # Group by month and find the month with the highest count
            if not country_df.empty:
                if 'month' in question:
                    month_counts = country_df.groupby('Month').size().reset_index(name='insight_count')
                    highest_month = month_counts.loc[month_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {country}, the month with the highest insights is {highest_month['Month']} with {highest_month['insight_count']} insights.")
                    insights_dfs.append(country_df.loc[country_df['Month'].str.lower() == (highest_month['Month'].lower())])                

                if 'year' in question:
                    year_counts = country_df.groupby('Year').size().reset_index(name='insight_count')
                    highest_year = year_counts.loc[year_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {country}, the year with the highest insights is {highest_year['Year']} with {highest_year['insight_count']} insights.")
                    insights_dfs.append(country_df.loc[country_df['Year'] == (highest_year['Year'])])

                else:
                    month_counts = product_df.groupby('Month').size().reset_index(name='insight_count')
                    highest_month = month_counts.loc[month_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {product},the highest insights is {highest_month['Month']} with {highest_month['insight_count']} insights.")
                    insights_dfs.append(product_df.loc[product_df['Month'].str.lower() == (highest_month['Month'].lower())])
            else:
                insights_info.append(f"No insights found for {country} in the specified query.")

            # Return the insights information and the combined DataFrame
            return insights_info, insights_dfs if insights_info else "No insights found for the specified query."

    # If no products, regions, or countries are specified, filter based on month/year
    #didnt add country region product keywords search
    elif not regions and not countries and not products:
        filtered_df = df
        # Apply month filter
        if months:
            filtered_df = filtered_df[filtered_df['Month'].str.lower().isin([m.lower() for m in months])]

        # Apply year filter
        if years:
            filtered_df = filtered_df[filtered_df['Year'].isin(years)]

        # Group by month and find the month with the highest count
        if not filtered_df.empty:
            if "product" in question:
                product_counts = filtered_df.groupby('Product').size().reset_index(name='insight_count')
                highest_product = product_counts.loc[product_counts['insight_count'].idxmax()]
                insights_info.append(f"The month with the highest overall insights is {highest_product['Product']} with {highest_product['insight_count']} insights.")
                insights_dfs.append(filtered_df.loc[filtered_df['Product'].str.lower() == (highest_product['Product'].lower())])

          
            elif "region" in question:
                region_counts = filtered_df.groupby('Region').size().reset_index(name='insight_count')
                highest_region = region_counts.loc[region_counts['insight_count'].idxmax()]
                filtered_region_df = filtered_df[filtered_df['Region'].str.lower() == highest_region['Region'].lower()]
                if "country" in question:
                    country_counts = filtered_region_df.groupby('Country').size().reset_index(name='insight_count')
                    highest_country = country_counts.loc[country_counts['insight_count'].idxmin()]
                    insights_info.append(f"The region with the highest insights is {highest_region['Region']} with {highest_region['insight_count']} insights. The country with the lowest insights in {lowest_region['Region']} is {lowest_country['Country']} with {lowest_country['insight_count']} insights.")                   
                else:
                    insights_info.append(f"The region with the highest overall insights is {highest_region['Region']} with {highest_region['insight_count']} insights.")
                    insights_dfs.append(filtered_df.loc[filtered_df['Region'].str.lower() == (highest_region['Region'].lower())])

            if "country" in question:
                country_counts = filtered_df.groupby('Country').size().reset_index(name='insight_count')
                highest_country = country_counts.loc[country_counts['insight_count'].idxmax()]
                insights_info.append(f"The country with the highest overall insights is {highest_country['Country']} with {highest_country['insight_count']} insights.")
                insights_dfs.append(filtered_df.loc[filtered_df['Country'].str.lower() == (highest_country['Country'].lower())])  

            if "year" in question:
                year_counts = filtered_df.groupby('Year').size().reset_index(name='insight_count')
                highest_year = year_counts.loc[year_counts['insight_count'].idxmax()]
                insights_info.append(f"The year with the highest overall insights is {highest_year['Year']} with {highest_year['insight_count']} insights.")
                insights_dfs.append(filtered_df.loc[filtered_df['Year'] == (highest_year['Year'])])

            if "month" in question:
                month_counts = filtered_df.groupby('Month').size().reset_index(name='insight_count')
                highest_month = month_counts.loc[month_counts['insight_count'].idxmax()]
                insights_info.append(f"The month with the highest overall insights is {highest_month['Month']} with {highest_month['insight_count']} insights.")
                insights_dfs.append(filtered_df.loc[filtered_df['Month'].str.lower() == (highest_month['Month'].lower())])

            if not insights_info:  # Only append if no insights were found
                insights_info.append("No insights found for the specified query.")

            # Return the final insights information and the combined DataFrame
        return insights_info, insights_dfs if insights_info else "No insights found for the specified query."
    
def lowest_insights_by_month(question):
    importances = extract_multiple_from_question(question, unique_importances)
    regions = extract_multiple_from_question(question, unique_regions)
    countries = extract_multiple_from_question(question, unique_countries)
    months = extract_multiple_from_question(question, unique_month)
    years = extract_multiple_from_question(question, unique_year)
    products = extract_multiple_from_question(question, unique_product)
    therapeutic_areas = extract_multiple_from_question(question, unique_therapeutic_areas) 

    insights_info = []
    insights_dfs = [] 
    if importances:
        for importance in importances:
            imp_df=df[df['Importance'].str.lower()==importance.lower()]   
            if therapeutic_areas:
                imp_df = imp_df[imp_df['Therapeutic Area'].str.lower() == therapeutic_area.lower()]
            if products:
                imp_df = imp_df[imp_df['Product'].str.lower().isin([p.lower() for p in products])]
            if regions:
                imp_df = imp_df[imp_df['Region'].str.lower().isin([r.lower() for r in regions])]
            if countries:
                imp_df = imp_df[imp_df['Country'].str.lower().isin([c.lower() for c in countries])]
            if months:
                imp_df = imp_df[imp_df['Month'].str.lower().isin([m.lower() for m in months])]
            if years:
                imp_df = imp_df[imp_df['Year'].isin(years)]

            # Group by month and find the month with the lowest count
            if not imp_df.empty:
                if 'month' in question:
                    month_counts = imp_df.groupby('Month').size().reset_index(name='insight_count')
                    lowest_month = month_counts.loc[month_counts['insight_count'].idxmin()]
                    insights_info.append(f"For {importance}, the month with the lowest insights is {highest_month['Month']} with {highest_month['insight_count']} insights.")
                    insights_dfs.append(imp_df.loc[imp_df['Month'].str.lower() == (highest_month['Month'].lower())])

                if 'year' in question:
                    year_counts = imp_df.groupby('Year').size().reset_index(name='insight_count')
                    lowest_year = year_counts.loc[year_counts['insight_count'].idxmin()]
                    insights_info.append(f"For {importance}, the year with the lowest insights is {lowest_year['Year']} with {lowest_year['insight_count']} insights.")
                    insights_dfs.append(imp_df.loc[imp_df['Year'] == lowest_year['Year']])

                if 'country' in question:
                    country_counts = imp_df.groupby('Country').size().reset_index(name='insight_count')
                    lowest_country = country_counts.loc[country_counts['insight_count'].idxmin()]
                    insights_info.append(f"For {importance}, the country with the lowest insights is {lowest_country['Country']} with {lowest_country['insight_count']} insights.")
                    insights_dfs.append(imp_df.loc[imp_df['Country'].str.lower() == (lowest_country['Country'].lower())])

                if 'region' in question:
                    region_counts = imp_df.groupby('Region').size().reset_index(name='insight_count')
                    lowest_region = region_counts.loc[region_counts['insight_count'].idxmin()]
                    insights_info.append(f"For {importance}, the region with the lowest insights is {lowest_region['Region']} with {lowest_region['insight_count']} insights.")
                    insights_dfs.append(imp_df.loc[imp_df['Region'].str.lower() == (lowest_region['Region'].lower())])

                if 'product' in question:
                    product_counts = imp_df.groupby('Product').size().reset_index(name='insight_count')
                    lowest_product = product_counts.loc[product_counts['insight_count'].idxmin()]
                    insights_info.append(f"For {importance}, the product with the lowest insights is {lowest_product['Product']} with {lowest_product['insight_count']} insights.")
                    insights_dfs.append(imp_df.loc[imp_df['Product'].str.lower() == (lowest_product['Product'].lower())])

                if 'therapeutic area' in question:
                    area_counts = imp_df.groupby('Therapeutic Area').size().reset_index(name='insight_count')
                    lowest_area = area_counts.loc[area_counts['insight_count'].idxmin()]
                    insights_info.append(f"For {importance}, the area with the highest insights is {lowest_area['Therapeutic Area']} with {lowest_area['insight_count']} insights.")
                    insights_dfs.append(imp_df.loc[imp_df['Therapeutic Area'].str.lower() == (lowest_area['Therapeutic Area'].lower())])

                else:
                    month_counts = product_df.groupby('Month').size().reset_index(name='insight_count')
                    highest_month = month_counts.loc[month_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {product},the highest insights is {highest_month['Month']} with {highest_month['insight_count']} insights.")
                    insights_dfs.append(product_df.loc[product_df['Month'].str.lower() == (highest_month['Month'].lower())])
            else:
                insights_info.append(f"No insights available for {importance} in the specified filters.")
        return insights_info, insights_dfs if insights_info else "No insights found for the specified query."

    elif therapeutic_areas:
        for therapeutic_area in therapeutic_areas:
            therapeutic_area_df = df[df['Therapeutic Area'].str.lower() == therapeutic_area.lower()]
            if products:
                therapeutic_area_df = therapeutic_area_df[therapeutic_area_df['Product'].str.lower().isin([p.lower() for p in products])]
            if regions:
                therapeutic_area_df = therapeutic_area_df[therapeutic_area_df['Region'].str.lower().isin([r.lower() for r in regions])]
            if countries:
                therapeutic_area_df = therapeutic_area_df[therapeutic_area_df['Country'].str.lower().isin([c.lower() for c in countries])]
            if months:
                therapeutic_area_df = therapeutic_area_df[therapeutic_area_df['Month'].str.lower().isin([m.lower() for m in months])]
            if years:
                therapeutic_area_df = therapeutic_area_df[therapeutic_area_df['Year'].isin(years)]

            # Group by month and find the month with the lowest count
            if not therapeutic_area_df.empty:
                if 'month' in question:
                    month_counts = therapeutic_area_df.groupby('Month').size().reset_index(name='insight_count')
                    lowest_month = month_counts.loc[month_counts['insight_count'].idxmin()]
                    insights_info.append(f"For {therapeutic_area}, the month with the lowest insights is {lowest_month['Month']} with {lowest_month['insight_count']} insights.")
                    insights_dfs.append(therapeutic_area_df.loc[therapeutic_area_df['Month'].str.lower() == (lowest_month['Month'].lower())])

                if 'year' in question:
                    year_counts = therapeutic_area_df.groupby('Year').size().reset_index(name='insight_count')
                    lowest_year = year_counts.loc[year_counts['insight_count'].idxmin()]
                    insights_info.append(f"For {therapeutic_area}, the year with the lowest insights is {lowest_year['Year']} with {lowest_year['insight_count']} insights.")
                    insights_dfs.append(therapeutic_area_df.loc[therapeutic_area_df['Year'] == lowest_year['Year']])

                if 'country' in question:
                    country_counts = therapeutic_area_df.groupby('Country').size().reset_index(name='insight_count')
                    lowest_country = country_counts.loc[country_counts['insight_count'].idxmin()]
                    insights_info.append(f"For {therapeutic_area}, the country with the lowest insights is {lowest_country['Country']} with {lowest_country['insight_count']} insights.")
                    insights_dfs.append(therapeutic_area_df.loc[therapeutic_area_df['Country'].str.lower() == (lowest_country['Country'].lower())])

                if 'region' in question:
                    region_counts = therapeutic_area_df.groupby('Region').size().reset_index(name='insight_count')
                    lowest_region = region_counts.loc[region_counts['insight_count'].idxmin()]
                    insights_info.append(f"For {therapeutic_area}, the region with the lowest insights is {lowest_region['Region']} with {lowest_region['insight_count']} insights.")
                    insights_dfs.append(therapeutic_area_df.loc[therapeutic_area_df['Region'].str.lower() == (lowest_region['Region'].lower())])
                
                if 'product' in question:
                    product_counts = therapeutic_area_df.groupby('Product').size().reset_index(name='insight_count')
                    lowest_product = product_counts.loc[product_counts['insight_count'].idxmin()]
                    insights_info.append(f"For {therapeutic_area}, the product with the lowest insights is {lowest_product['Product']} with {lowest_product['insight_count']} insights.")
                    insights_dfs.append(therapeutic_area_df.loc[therapeutic_area_df['Product'].str.lower() == (lowest_product['Product'].lower())])
            
                else:
                    month_counts = product_df.groupby('Month').size().reset_index(name='insight_count')
                    highest_month = month_counts.loc[month_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {product},the highest insights is {highest_month['Month']} with {highest_month['insight_count']} insights.")
                    insights_dfs.append(product_df.loc[product_df['Month'].str.lower() == (highest_month['Month'].lower())])
            else:
                insights_info.append(f"No insights available for {therapeutic_area} in the specified filters.")

        # Return the insights information and the combined DataFrame
        return insights_info, insights_dfs if insights_info else "No insights found for the specified query."

    elif products:
        for product in products:
            product_df = df[df['Product'].str.lower() == product.lower()]
            # Apply region filter
            if regions:
                product_df = product_df[product_df['Region'].str.lower().isin([r.lower() for r in regions])]
            # Apply country filter
            if countries:
                product_df = product_df[product_df['Country'].str.lower().isin([c.lower() for c in countries])]
            # Apply month filter
            if months:
                product_df = product_df[product_df['Month'].str.lower().isin([m.lower() for m in months])]
            # Apply year filter
            if years:
                product_df = product_df[product_df['Year'].isin(years)]

            # Group by month and find the month with the highest count
            if not product_df.empty:
                if 'month' in question:
                    month_counts = product_df.groupby('Month').size().reset_index(name='insight_count')
                    highest_month = month_counts.loc[month_counts['insight_count'].idxmin()]
                    insights_info.append(f"For {product}, the month with the lowest insights is {highest_month['Month']} with {highest_month['insight_count']} insights.")
                    insights_dfs.append(product_df.loc[product_df['Month'].str.lower() == (highest_month['Month'].lower())])                

                if 'year' in question:
                    year_counts = product_df.groupby('Year').size().reset_index(name='insight_count')
                    highest_year = year_counts.loc[year_counts['insight_count'].idxmin()]
                    insights_info.append(f"For {product}, the year with the lowest insights is {highest_year['Year']} with {highest_year['insight_count']} insights.")
                    insights_dfs.append(product_df.loc[product_df['Year'].str.lower() == (highest_year['Year'].lower())])

                if 'country' in question:
                    country_counts = product_df.groupby('Country').size().reset_index(name='insight_count')
                    highest_country = country_counts.loc[country_counts['insight_count'].idxmin()]
                    insights_info.append(f"For {product}, the country with the lowest insights is {highest_country['Country']} with {highest_country['insight_count']} insights.")
                    insights_dfs.append(product_df.loc[product_df['Country'].str.lower() == (highest_country['Country'].lower())])
                
                if 'region' in question:
                    region_counts = product_df.groupby('Region').size().reset_index(name='insight_count')
                    highest_region = region_counts.loc[region_counts['insight_count'].idxmin()]
                    insights_info.append(f"For {product}, the region with the lowest insights is {highest_region['Region']} with {highest_region['insight_count']} insights.")
                    insights_dfs.append(product_df.loc[product_df['Region'].str.lower() == (highest_region['Region'].lower())])

                else:
                    month_counts = product_df.groupby('Month').size().reset_index(name='insight_count')
                    highest_month = month_counts.loc[month_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {product},the highest insights is {highest_month['Month']} with {highest_month['insight_count']} insights.")
                    insights_dfs.append(product_df.loc[product_df['Month'].str.lower() == (highest_month['Month'].lower())])    
            else:
                insights_info.append(f"No insights available for {product} in the specified filters.")

        # Return the insights information and the combined DataFrame
        return insights_info, insights_dfs if insights_info else "No insights found for the specified query."

    # Process regions when no products are given
    elif regions:
        for region in regions:
            region_df = df[df['Region'].str.lower() == region.lower()]
            # Apply country filter
            if countries:
                region_df = region_df[region_df['Country'].str.lower().isin([c.lower() for c in countries])]
            # Apply month filter
            if months:
                region_df = region_df[region_df['Month'].str.lower().isin([m.lower() for m in months])]
            # Apply year filter
            if years:
                region_df = region_df[region_df['Year'].isin(years)]

            # Group by month and find the month with the lowest count
            if not region_df.empty:
                if 'month' in question:
                    month_counts = region_df.groupby('Month').size().reset_index(name='insight_count')
                    lowest_month = month_counts.loc[month_counts['insight_count'].idxmin()]
                    insights_info.append(f"For {region}, the month with the lowest insights is {lowest_month['Month']} with {lowest_month['insight_count']} insights.")
                    insights_dfs.append(region_df.loc[region_df['Month'].str.lower() == (lowest_month['Month'].lower())])                

                if 'year' in question:
                    month_counts = region_df.groupby('Year').size().reset_index(name='insight_count')
                    lowest_year = month_counts.loc[month_counts['insight_count'].idxmin()]
                    insights_info.append(f"For {region}, the year with the lowest insights is {lowest_year['Year']} with {lowest_year['insight_count']} insights.")
                    insights_dfs.append(region_df.loc[region_df['Year'].str.lower() == (lowest_year['Year'].lower())])

                else:
                    month_counts = product_df.groupby('Month').size().reset_index(name='insight_count')
                    highest_month = month_counts.loc[month_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {product},the highest insights is {highest_month['Month']} with {highest_month['insight_count']} insights.")
                    insights_dfs.append(product_df.loc[product_df['Month'].str.lower() == (highest_month['Month'].lower())])
            else:
                insights_info.append(f"No insights found for {region} in the specified query.")

        return insights_info, insights_dfs if insights_info else "No insights found for the specified query."

    # Process countries when no products or regions are given
    elif countries:
        for country in countries:
            country_df = df[df['Country'].str.lower() == country.lower()]
            # Apply month filter
            if months:
                country_df = country_df[country_df['Month'].str.lower().isin([m.lower() for m in months])]
            # Apply year filter
            if years:
                country_df = country_df[country_df['Year'].isin(years)]

            # Group by month and find the month with the highest count
            if not country_df.empty:
                if 'month' in question:
                    month_counts = country_df.groupby('Month').size().reset_index(name='insight_count')
                    lowest_month = month_counts.loc[month_counts['insight_count'].idxmin()]
                    insights_info.append(f"For {country}, the month with the lowest insights is {highest_month['Month']} with {highest_month['insight_count']} insights.")
                    insights_dfs.append(country_df.loc[country_df['Month'].str.lower() == (highest_month['Month'].lower())])                

                if 'year' in question:
                    month_counts = country_df.groupby('Year').size().reset_index(name='insight_count')
                    lowest_year  = month_counts.loc[month_counts['insight_count'].idxmin()]
                    insights_info.append(f"For {country}, the year with the lowest insights is {lowest_year['Year']} with {lowest_year['insight_count']} insights.")
                    insights_dfs.append(country_df.loc[country_df['Year'] == (lowest_year ['Year'])])
                
                else:
                    month_counts = product_df.groupby('Month').size().reset_index(name='insight_count')
                    highest_month = month_counts.loc[month_counts['insight_count'].idxmax()]
                    insights_info.append(f"For {product},the highest insights is {highest_month['Month']} with {highest_month['insight_count']} insights.")
                    insights_dfs.append(product_df.loc[product_df['Month'].str.lower() == (highest_month['Month'].lower())])
            else:
                insights_info.append(f"No insights found for {country} in the specified query.")

            # Return the insights information and the combined DataFrame
            return insights_info, insights_dfs if insights_info else "No insights found for the specified query."

    # If no products, regions, or countries are specified, filter based on month/year
    #didnt add country region product keywords search
    elif not regions and not countries and not products and not therapeutic_areas and not importances:
        filtered_df = df
        # Apply month filter
        if months:
            filtered_df = filtered_df[filtered_df['Month'].str.lower().isin([m.lower() for m in months])]

        # Apply year filter
        if years:
            filtered_df = filtered_df[filtered_df['Year'].isin(years)]

        # Group by month and find the month with the lowest count
        if not filtered_df.empty:
          if "product" in question:
            product_counts = filtered_df.groupby('Product').size().reset_index(name='insight_count')           
            if "region" in question:
                product_counts = filtered_df.groupby('Region').size().reset_index(name='insight_count')
                if "country" in question:
                    product_counts = filtered_df.groupby('Country').size().reset_index(name='insight_count')
                    lowest_country = product_counts.loc[product_counts['insight_count'].idxmin()]
                    insights_info.append(f"The region with the lowest insights is {lowest_country['Region']} with {lowest_country['insight_count']} insights. The country with the lowest insights in {lowest_region['Region']} is {lowest_country['Country']} with {lowest_country['insight_count']} insights.")        
                else:
                    lowest_product = product_counts.loc[region_counts['insight_count'].idxmin()]
                    insights_info.append(f"The region with the lowest overall insights is {lowest_region['Region']} with {lowest_region['insight_count']} insights.")
                    insights_dfs.append(filtered_df.loc[filtered_df['Region'].str.lower() == (lowest_region['Region'].lower())])           
            else:
                lowest_product = product_counts.loc[product_counts['insight_count'].idxmin()]
                insights_info.append(f"The prodyct with the lowest overall insights is {lowest_product['Product']} with {lowest_product['insight_count']} insights.")
                insights_dfs.append(filtered_df.loc[filtered_df['Product'].str.lower() == (lowest_product['Product'].lower())])
            
            if "country" in question:
                    product_counts = filtered_df.groupby('Country').size().reset_index(name='insight_count')
                    lowest_country = product_counts.loc[product_counts['insight_count'].idxmin()]
                    insights_info.append(f"The country with the lowest insights is {lowest_country['Country']} with {lowest_country['insight_count']} insights.")        
            else:
                lowest_product = product_counts.loc[region_counts['insight_count'].idxmin()]
                insights_info.append(f"The product with the lowest overall insights is {lowest_region['Region']} with {lowest_region['insight_count']} insights.")
                insights_dfs.append(filtered_df.loc[filtered_df['Region'].str.lower() == (lowest_region['Region'].lower())])

          elif "region" in question:
            region_counts = filtered_df.groupby('Region').size().reset_index(name='insight_count')
            lowest_region = region_counts.loc[region_counts['insight_count'].idxmin()]
            filtered_region_df = filtered_df[filtered_df['Region'].str.lower() == lowest_region['Region'].lower()]
            if "country" in question:
                country_counts = filtered_region_df.groupby('Country').size().reset_index(name='insight_count')
                lowest_country = country_counts.loc[country_counts['insight_count'].idxmin()]
                insights_info.append(f"The region with the lowest insights is {lowest_region['Region']} with {lowest_region['insight_count']} insights. The country with the lowest insights in {lowest_region['Region']} is {lowest_country['Country']} with {lowest_country['insight_count']} insights.")                   
            else:
                insights_info.append(f"The region with the lowest overall insights is {lowest_region['Region']} with {lowest_region['insight_count']} insights.")
                insights_dfs.append(filtered_df.loc[filtered_df['Region'].str.lower() == (lowest_region['Region'].lower())])
          
          elif "country" in question:
            country_counts = filtered_df.groupby('Country').size().reset_index(name='insight_count')
            lowest_country = country_counts.loc[country_counts['insight_count'].idxmin()]
            insights_info.append(f"The contry with the lowest overall insights is {lowest_country['Country']} with {lowest_country['insight_count']} insights.")
            insights_dfs.append(filtered_df.loc[filtered_df['Country'].str.lower() == (lowest_country['Country'].lower())])
          
          elif "year" in question:
            month_counts = filtered_df.groupby('Year').size().reset_index(name='insight_count')
            lowest_year = month_counts.loc[month_counts['insight_count'].idxmin()]
            insights_info.append(f"The year with the lowest overall insights is {lowest_year['Year']} with {lowest_year['insight_count']} insights.")
            insights_dfs.append(filtered_df.loc[filtered_df['Year'] == (lowest_year['Year'])])

          elif "month" in question:
            month_counts = filtered_df.groupby('Month').size().reset_index(name='insight_count')
            lowest_month = month_counts.loc[month_counts['insight_count'].idxmin()]
            insights_info.append(f"The month with the lowest overall insights is {lowest_month['Month']} with {lowest_month['insight_count']} insights.")
            insights_dfs.append(filtered_df.loc[filtered_df['Month'].str.lower() == (lowest_month['Month'].lower())])

          elif "therapeutic area" in question:
            month_counts = filtered_df.groupby('Therapeutic Area').size().reset_index(name='insight_count')
            lowest_month = month_counts.loc[month_counts['insight_count'].idxmin()]
            insights_info.append(f"The 'Therapeutic Area' with the lowest overall insights is {lowest_month['Therapeutic Area']} with {lowest_month['insight_count']} insights.")
            insights_dfs.append(filtered_df.loc[filtered_df['Therapeutic Area'].str.lower() == (lowest_month['Therapeutic Area'].lower())])  

          elif "importance" in question:
            month_counts = filtered_df.groupby('Importance').size().reset_index(name='insight_count')
            lowest_month = month_counts.loc[month_counts['insight_count'].idxmin()]
            insights_info.append(f"The importance with the lowest overall insights is {lowest_month['Importance']} with {lowest_month['insight_count']} insights.")
            insights_dfs.append(filtered_df.loc[filtered_df['Importance'].str.lower() == (lowest_month['Importance'].lower())])

        if not insights_info:  # Only append if no insights were found
                insights_info.append("No insights found for the specified query.")

        # Return the final insights information and the combined DataFrame
        return insights_info, insights_dfs if insights_info else "No insights found for the specified query."
    
def unique(question):
    insights_info = []
    insights_dfs = [] 

    # Extract regions, countries, months, years, and products from the question
    importances = extract_multiple_from_question(question, unique_importances)
    regions = extract_multiple_from_question(question, unique_regions)
    countries = extract_multiple_from_question(question, unique_countries)
    months = extract_multiple_from_question(question, unique_month)
    years = extract_multiple_from_question(question, unique_year)
    products = extract_multiple_from_question(question, unique_product)
    therapeutic_areas = extract_multiple_from_question(question, unique_therapeutic_areas) 

    # Apply filters on the DataFrame
    filtered_df = df

    if importances:
        filtered_df = filtered_df[filtered_df['Importance'].str.lower().isin([i.lower() for i in importances])]

    if therapeutic_areas:
        filtered_df = filtered_df[filtered_df['Therapeutic Areas'].str.lower().isin([a.lower() for a in therapeutic_areas])]

    if products:
        filtered_df = filtered_df[filtered_df['Product'].str.lower().isin([m.lower() for m in products])]

    if countries:
        filtered_df = filtered_df[filtered_df['Country'].str.lower().isin([m.lower() for m in countries])]

    if regions:
        filtered_df = filtered_df[filtered_df['Region'].str.lower().isin([m.lower() for m in regions])]

    if months:
        filtered_df = filtered_df[filtered_df['Month'].str.lower().isin([m.lower() for m in months])]

    if years:
        filtered_df = filtered_df[filtered_df['Year'].isin(years)]

    # Check the user's question for what unique values to return
    if 'importance' in question:
        insights_info.append("The unique products are:")
        insights_dfs.append(filtered_df['Importance'].unique())  # Return unique Importances

    if 'therapeutic area' in question:
        insights_info.append("The unique products are:")
        insights_dfs.append(filtered_df['Therapeutic Area'].unique())  # Return unique Therapeutic Areas

    if 'product' in question:
        insights_info.append("The unique products are:")
        insights_dfs.append(filtered_df['Product'].unique())  # Return unique products

    if 'region' in question:
        insights_info.append("The unique regions are:")
        insights_dfs.append(filtered_df['Region'].unique())  # Return unique regions

    if 'country' in question:
        insights_info.append("The unique countries are:")
        insights_dfs.append(filtered_df['Country'].unique())  # Return unique countries

    if 'month' in question:
        insights_info.append("The unique months are:")
        insights_dfs.append(filtered_df['Month'].unique())  # Return unique months

    if 'year' in question:
        insights_info.append("The unique years are:")
        insights_dfs.append(filtered_df['Year'].unique())  # Return unique years
    

    # Return the insights information and the insights DataFrame list
    return insights_info, insights_dfs if insights_info else "No insights found for the specified query."

def analyze_data_for_insight(question):
    question = question.lower()
    if "highest" in question:
        return highest_insights_by_month(question)
    elif "lowest" in question:
        return lowest_insights_by_month(question)
    elif "available" in question:
        return unique(question)
    else:
        return number_of_insights(question)

# Chatbot function
def chatbot(question):
    analysis_result, insights_dfs = analyze_data_for_insight(question)
    return analysis_result, insights_dfs


# Analyze the question when the user clicks the 'Analyze' button
with st.container():
    st.subheader("Ask a question:")
    question = st.text_input("Type your question here...")

    if st.button('Submit'):
        if question:
            # Call the chatbot function with the question as input
            analysis_result, insights_dfs = chatbot(question)
            print(analysis_result, insights_dfs)

            # Display the results dynamically based on the question
            if analysis_result:              
                for i in range(0, min(len(analysis_result), len(insights_dfs))):
                    st.success(analysis_result[i])
                    st.write("Here are the filtered insights data:")
                    st.dataframe(insights_dfs[i])
            else:
                st.warning("No insights found for the specified query.")
        else:
            st.warning("Please enter a valid question.")
