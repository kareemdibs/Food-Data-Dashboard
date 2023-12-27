import pandas as pd
from dash import Dash, html, dash_table, dcc, Output, Input
import plotly.express as px

# Read the Excel file into a DataFrame
df = pd.read_excel('foodinfo.xlsx', sheet_name="FoodList")

# Columns to remove
columns_to_remove = ['Measure', 'Unnamed: 8', 'Note: Protein, Fat, Carbs, Fibre, are measured in grams']

# Drop unnecessary columns
df = df.drop(columns=columns_to_remove)

# Initialize the Dash app
app = Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.Div(children='Food Data'),
    html.Hr(),
    # Dropdown for selecting the metric (Calories, Protein, Fat, Carbs, Fibre)
    dcc.Dropdown(
        id='metric-dropdown',
        options=[
            {'label': col, 'value': col} for col in ['Calories', 'Protein', 'Fat', 'Carbs', 'Fibre']
        ],
        value='Calories',  # Default metric
        style={'width': '50%'}
    ),
    # Display the DataTable
    dash_table.DataTable(
        id='food-table',
        columns=[{'name': col, 'id': col} for col in df.columns],
        data=df.to_dict('records'),
        page_size=10,
        row_selectable='multi'  # Allow multiple rows to be selected
    ),
    # Placeholder for the graph
    dcc.Graph(id='food-graph'),
    html.Footer(children='2023 Kareem Dibs'),
])

# Define the callback to update the graph based on user selection
@app.callback(
    Output('food-graph', 'figure'),
    [Input('metric-dropdown', 'value'),
     Input('food-table', 'selected_rows')]
)
def update_graph(selected_metric, selected_rows):
    # If no rows are selected, return an empty figure
    if not selected_rows:
        return px.scatter()

    # Get the selected food items
    selected_food_items = df.iloc[selected_rows]['Food Item']

    # Create a new DataFrame for the selected food items
    selected_food_df = df[df['Food Item'].isin(selected_food_items)]

    # Plot the graph
    fig = px.bar(selected_food_df, x='Food Item', y=selected_metric,
                 title=f'Statistics for {selected_metric} in selected food items')

    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
