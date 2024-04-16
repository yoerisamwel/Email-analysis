import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

# ----------------------------------------------------------------------------------------------------------------------
# loading data

df = pd.read_csv(("data/Cleaned_Email_Domains.csv"), low_memory=False)

#-----------------------------------------------------------------------------------------------------------------------
#Data cleaning/preparation

df_renamed = df.rename(columns={'tld': 'Domain name'})

#-----------------------------------------------------------------------------------------------------------------------
#Setting up graphs
#pie chart
fig_pie = px.pie(df, names='gender', title='Gender Distribution in Dataset',
             color='gender',  # Maps the colors to the gender
             color_discrete_map={'male': 'blue', 'female': 'red', 'non-binary': 'green'},  # Custom colors
             hole=0.3,  # Turns the pie into a donut chart
             labels={'gender': 'Gender Identity'},  # Custom labels
             )

fig_pie.update_traces(textposition='inside', textinfo='percent+label')  # Adjust text placement and information
fig_pie.update_layout(legend_title_text='Gender',  # Customize the legend title
                  title_font_size=20,  # Title font size
                  legend_font_size=12,  # Legend font size
                  font_family="Arial, sans-serif",  # Font family
                  )

#Sunburst
# Create a group by gender and domain to count occurrences
grouped = df.groupby(['gender', 'email_domain']).size().reset_index(name='counts')

# Prepare labels, parents, and values for the sunburst chart
labels = list(grouped['gender'].unique()) + list(grouped['email_domain'])
parents = [""] * len(grouped['gender'].unique()) + list(grouped['gender'])
values = [grouped[grouped['gender'] == x]['counts'].sum() for x in grouped['gender'].unique()] + list(grouped['counts'])

# Create the sunburst chart
fig_sunburst = go.Figure(go.Sunburst(
    labels=labels,
    parents=parents,
    values=values,
    branchvalues="total"
))
fig_sunburst.update_layout(margin=dict(t=0, l=0, r=0, b=0))

#bar chart
# Count the frequency of each domain
domain_counts = df['email_domain'].value_counts().reset_index()
domain_counts.columns = ['email_domain', 'count']

# Create a bar chart
fig_bar = go.Figure(go.Bar(
    x=domain_counts['email_domain'],
    y=domain_counts['count'],
    text=domain_counts['count'],
    textposition='auto'
))

fig_bar.update_layout(
    title='Email Domain Distribution',
    xaxis_title='Email Domain',
    yaxis_title='Domain counts'
)
# ----------------------------------------------------------------------------------------------------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )




app.layout = dbc.Container([

    dbc.Row(
        dbc.Col(html.H1("Email domain analysis"),
                width=12)),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Total orders per shipping method"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=fig_pie,
                        id='pie_chart'
                    )
                ])
            ]),
            width=6
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Email domains per gender"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=fig_sunburst,
                        id='sunburst'
                    )
                ])
            ]),
            width=6
        )
    ]),
    dbc.Row([
        dbc.Col(
                    dbc.Card([
                        dbc.CardHeader("Email domains distribution"),
                        dbc.CardBody([
                            dcc.Graph(
                                figure=fig_bar,
                                id='barchart'
                            )
                        ])
                    ]),
                    width=12
                )
    ])
], fluid=True)

# ------------------------------------------------
# launching the app

if __name__ == '__main__':
    app.run_server(debug=True)