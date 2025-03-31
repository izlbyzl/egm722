import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches


# ---------------------------------------------------------------------------------------------------------------------
# in this section, write the script to load the data and complete the main part of the analysis.
# try to print the results to the screen using the format method demonstrated in the workbook

# load the necessary data here and transform to a UTM projection
counties = gpd.read_file('Week3/data_files/Counties.shp']
wards = gpd.read_file('Week3/data_files/NI_Wards.shp']
counties = counties.to_crs(epsg=32629)
wards = wards.to_crs(epsg=32629)

# your analysis goes here...
join = gpd.sjoin(counties, wards, how='inner', lsuffix='left', rsuffix='right') # join wards and counties 

# find counties total population
county_total_popn = join.groupby('CountyName')['Population'].sum() # grouped by county name and summed population
print(county_total_popn)

highest_popn_county = county_total_popn.idxmax() # finds the name of the county with highest population 
county_popn_max = county_total_popn.max() # finds greatest population value  
print(f'The county with the highest population is {highest_popn_county}, with a population of {county_popn_max}')

lowest_popn_county = county_total_popn.idxmin() # finds county name with lowest population
county_popn_min = county_total_popn.min() # finds lowest population value
print(f'The county with the lowest population is {lowest_popn_county}, with a population of {county_popn_min}')

ward_counties = join.groupby('Ward')['CountyName'].nunique() # group by ward and count number of unique counties associated with
wards_multi_county = ward_counties[ward_counties > 1] # filters wards associated with more than 1 county
print(f'Wards located in more than one county are: {wards_multi_county}')


# ---------------------------------------------------------------------------------------------------------------------
# below here, you may need to modify the script somewhat to create your map.
# create a crs using ccrs.UTM() that corresponds to our CRS
ni_utm = ccrs.UTM(29)

# create a figure of size 10x10 (representing the page size in inches
fig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw=dict(projection=ni_utm))

# add gridlines below
gridlines = ax.gridlines(draw_labels=True,
                         xlocs=[-8, -7.5, -7, -6.5, -6, -5.5],
                         ylocs=[54, 54.5, 55, 55.5])
gridlines.right_labels = False
gridlines.bottom_labels = False

# to make a nice colorbar that stays in line with our map, use these lines:
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1, axes_class=plt.Axes)

# plot the ward data into our axis, using gdf.plot()
ward_plot = wards.plot(column='Population', ax=ax, vmin=1000, vmax=8000, cmap='viridis',
                       legend=True, cax=cax, legend_kwds={'label': 'Resident Population'})

# add county outlines in red using ShapelyFeature
county_outlines = ShapelyFeature(counties['geometry'], ni_utm, edgecolor='r', facecolor='none')
ax.add_feature(county_outlines)

county_handles = generate_handles([''], ['none'], edge='r')

# add a legend in the upper left-hand corner
ax.legend(county_handles, ['County Boundaries'], fontsize=12, loc='upper left', framealpha=1)

# save the figure
fig.savefig('sample_map.png', dpi=300, bbox_inches='tight')
