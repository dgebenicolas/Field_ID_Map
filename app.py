import os
import json
import pandas as pd
import streamlit as st
import plotly.express as px

def display_choropleth_map(results_df, config):
    st.subheader("Predicted Value Map")
    try:
        geojson_filepath = os.path.join(os.path.dirname(__file__), 'All Fields Polygons.geojson')
        if not os.path.exists(geojson_filepath):
            st.error("Missing GEOJSON file")
            return

        with open(geojson_filepath, 'r') as f:
            geojson_data = json.load(f)

        # Filters
        filters = {
            'Организация': st.multiselect(
                "Filter by Организация:",
                options=sorted(results_df['Организация'].unique()),
                default=sorted(results_df['Организация'].unique())
            ),
            'Подразделение': st.multiselect(
                "Filter by Подразделение:",
                options=sorted(results_df['Подразделение'].unique()),
                default=sorted(results_df['Подразделение'].unique())
            )
        }

        # Apply filters
        map_data = results_df.copy()
        for col, selected_values in filters.items():
            map_data = map_data[map_data[col].isin(selected_values)]

        fig_map = px.choropleth_mapbox(
            map_data,
            geojson=geojson_data,
            locations='Field_ID',
            featureidkey="properties.Field_ID",
            mapbox_style="carto-positron",
            zoom=8,
            center={'lat': 51.1801, 'lon': 71.4383},
            opacity=0.7,
            hover_data=['Field_ID']
        )

        fig_map.update_layout(
            margin={"r": 0, "t": 30, "l": 0, "b": 0},
            height=600,
            title=dict(text='Field Locations', x=0.5)
        )
        st.plotly_chart(fig_map, use_container_width=True)

    except Exception as e:
        st.error(f"Error creating map: {str(e)}")

def main():
    st.title('Field Mapping')

    # File uploader
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        display_choropleth_map(df, {
            'field_id_col': 'Field_ID',
            'map_center': {'lat': 51.1801, 'lon': 71.4383}
        })

if __name__ == "__main__":
    main()