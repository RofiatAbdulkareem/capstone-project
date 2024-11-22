from dotenv import load_dotenv
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# Load environment variables from .env file
load_dotenv()

# Fetch the password from environment variable
db_password = os.getenv('DB_PASSWORD')

# Database connection details
db_user = "rofee"
db_host = (
    "terraform-20241113122124605100000001."
    "cz4qw448wzk4.us-east-1.rds.amazonaws.com"
)
db_port = "5432"
db_name = "travel_agency_dw"

# Connection string
connection_string = (
    f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:"
    f"{db_port}/{db_name}"
)

# Create the engine
engine = create_engine(connection_string)

# Query to fetch all views from the database
query_views = (
    "SELECT table_name "
    "FROM pg_catalog.pg_views "
    "WHERE schemaname = 'public';"
)
# Fetch list of all views
views_df = pd.read_sql(query_views, engine)
print("Available Views:")
print(views_df)

# Loop through each view in the list and fetch data
for view in views_df['table_name']:
    query = f"SELECT * FROM public.{view} LIMIT 5;"  # Preview first 5 rows
    data = pd.read_sql(query, engine)
    print(f"\nPreviewing data for {view}:")
    print(data.head())  # Preview first 5 rows of each view

# Fetch the data for currency_count_by_continent
currency_data = pd.read_sql(
    "SELECT * FROM public."
    "currency_count_by_continent;", engine
)
# Save Bar Plot for currency_count_by_continent
plt.figure(figsize=(10, 6))
sns.barplot(
    x='continent',
    y='total_currencies',
    data=currency_data,
    hue='continent',
    palette="Set2"
)
plt.title("Number of Currencies by Continent")
plt.xlabel("Continent")
plt.ylabel("Number of Currencies")
plt.savefig("currency_count_by_continent.png")
plt.close()

# Fetch the data for population_density
population_density_data = pd.read_sql(
    "SELECT * FROM public."
    "population_density;", engine
)

# Sorting data to get the top 10 highest and lowest population density
top_population_density = population_density_data.sort_values(
    by='population_density',
    ascending=False
).head(10)
bottom_population_density = population_density_data.sort_values(
    by='population_density',
    ascending=True
).head(10)

# Plot for Top 10 Countries by Population Density
plt.figure(figsize=(12, 6))
sns.barplot(
    x='country_name',
    y='population_density',
    data=top_population_density,
    hue='country_name',
    palette="Greens_d"
)
plt.title("Top 10 Countries by Population Density")
plt.xlabel("Country")
plt.ylabel("Population Density")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("top_10_population_density.png")
plt.close()

# Plot for Bottom 10 Countries by Population Density
plt.figure(figsize=(12, 6))
sns.barplot(
    x='country_name',
    y='population_density',
    data=bottom_population_density,
    hue='country_name',
    palette="Reds_d"
)
plt.title("Bottom 10 Countries by Population Density")
plt.xlabel("Country")
plt.ylabel("Population Density")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("bottom_10_population_density.png")
plt.close()

# Fetch the data for start_of_week_analysis
start_of_week_data = pd.read_sql(
    "SELECT * FROM public."
    "start_of_week_analysis;", engine
)

# Save Bar Plot for start_of_week_analysis
plt.figure(figsize=(8, 5))
sns.barplot(
    x='start_of_week',
    y='country_count',
    data=start_of_week_data,
    hue='start_of_week',
    palette="Blues_d"
)
plt.title("Start of the Week Analysis")
plt.xlabel("Day of the Week")
plt.ylabel("Country Count")
plt.savefig("start_of_week_analysis.png")
plt.close()

# Fetch the data for top_regions
regions_data = pd.read_sql("SELECT * FROM public.top_regions;", engine)
fig, axes = plt.subplots(1, 2, figsize=(18, 6))

# Population plot
sns.barplot(
    x='region',
    y='total_population',
    data=regions_data,
    ax=axes[0],
    hue='region',
    palette="Blues_d"
)
axes[0].set_title("Total Population by Region")
axes[0].set_xlabel("Region")
axes[0].set_ylabel("Total Population")

# Area plot
sns.barplot(
    x='region',
    y='total_area',
    data=regions_data,
    ax=axes[1],
    hue='region',
    palette="Greens_d"
)
axes[1].set_title("Total Area by Region")
axes[1].set_xlabel("Region")
axes[1].set_ylabel("Total Area (sq km)")
plt.subplots_adjust(left=0.1, right=0.9)
plt.tight_layout()
plt.savefig("total_population_and_area_by_region.png")
plt.close()

# Fetch the data for top_languages_by_region
languages_data = pd.read_sql(
    "SELECT * FROM public."
    "top_languages_by_region;", engine
)

# Save Bar Plot for top_languages_by_region
plt.figure(figsize=(12, 6))
sns.barplot(
    x='region',
    y='language_count',
    data=languages_data,
    hue='languages',
    palette="Set1"
)
plt.title("Top Languages by Region")
plt.xlabel("Region")
plt.ylabel("Language Count")
plt.legend(title="Languages")
plt.savefig("top_languages_by_region.png")
plt.close()
