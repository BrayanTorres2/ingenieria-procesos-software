import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import datetime as dt



app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Dashboard energia"

server = app.server
app.config.suppress_callback_exceptions = True


# Load data from csv
def load_data():
    # To do: Completar la funciÃ³n 
    

# Cargar datos
data = load_data()

# Graficar serie
def plot_series(data, initial_date, proy):
    data_plot = data.loc[initial_date:]
    data_plot = data_plot[:-(120-proy)]
    fig = go.Figure([
        go.Scatter(
            name='Demanda energÃ©tica',
            x=data_plot.index,
            y=data_plot['AT_load_actual_entsoe_transparency'],
            mode='lines',
            line=dict(color="#188463"),
        ),
        go.Scatter(
            name='ProyecciÃ³n',
            x=data_plot.index,
            y=data_plot['forecast'],
            mode='lines',
            line=dict(color="#bbffeb",),
        ),
        go.Scatter(
            name='Upper Bound',
            x=data_plot.index,
            y=data_plot['Upper bound'],
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False
        ),
        go.Scatter(
            name='Lower Bound',
            x=data_plot.index,
            y=data_plot['Lower bound'],
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            fillcolor="rgba(242, 255, 251, 0.3)",
            fill='tonexty',
            showlegend=False
        )
    ])

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        yaxis_title='Demanda total [MW]',
        #title='Continuous, variable value error bars',
        hovermode="x"
    )
    #fig = px.line(data2, x='local_timestamp', y="Demanda total [MW]", markers=True, labels={"local_timestamp": "Fecha"})
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#2cfec1")
    fig.update_xaxes(showgrid=True, gridwidth=0.25, gridcolor='#7C7C7C')
    fig.update_yaxes(showgrid=True, gridwidth=0.25, gridcolor='#7C7C7C')
    #fig.update_traces(line_color='#2cfec1')

    return fig



def description_card():
    """
    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            #html.H5("Proyecto 1"),
            html.H3("PronÃ³stico de producciÃ³n energÃ©tica"),
            html.Div(
                id="intro",
                children="Esta herramienta contiene informaciÃ³n sobre la demanda energÃ©tica total en Austria cada hora segÃºn lo pÃºblicado en ENTSO-E Data Portal. Adicionalmente, permite realizar pronÃ³sticos hasta 5 dias en el futuro."
            ),
        ],
    )


def generate_control_card():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[

            # Fecha inicial
            html.P("Seleccionar fecha y hora inicial:"),

            html.Div(
                id="componentes-fecha-inicial",
                children=[
                    html.Div(
                        id="componente-fecha",
                        children=[
                            dcc.DatePickerSingle(
                                id='datepicker-inicial',
                                min_date_allowed=min(data.index.date),
                                max_date_allowed=max(data.index.date),
                                initial_visible_month=min(data.index.date),
                                date=max(data.index.date)-dt.timedelta(days=7)
                            )
                        ],
                        style=dict(width='30%')
                    ),
                    
                    html.P(" ",style=dict(width='5%', textAlign='center')),
                    
                    html.Div(
                        id="componente-hora",
                        children=[
                            dcc.Dropdown(
                                id="dropdown-hora-inicial-hora",
                                options=[{"label": i, "value": i} for i in np.arange(0,25)],
                                value=pd.to_datetime(max(data.index)-dt.timedelta(days=7)).hour,
                                # style=dict(width='50%', display="inline-block")
                            )
                        ],
                        style=dict(width='20%')
                    ),
                ],
                style=dict(display='flex')
            ),

            html.Br(),

            # Slider proyecciÃ³n
            html.Div(
                id="campo-slider",
                children=[
                    html.P("Ingrese horas a proyectar:"),
                    dcc.Slider(
                        id="slider-proyeccion",
                        min=0,
                        max=119,
                        step=1,
                        value=0,
                        marks=None,
                        tooltip={"placement": "bottom", "always_visible": True},
                    )
                ]
            )     
     
        ]
    )


app.layout = html.Div(
    id="app-container",
    children=[
        
        # Left column
        html.Div(
            id="left-column",
            className="four columns",
            children=[description_card(), generate_control_card()]
            + [
                html.Div(
                    ["initial child"], id="output-clientside", style={"display": "none"}
                )
            ],
        ),
        
        # Right column
        html.Div(
            id="right-column",
            className="eight columns",
            children=[


                # Grafica de la serie de tiempo
                html.Div(
                    id="model_graph",
                    children=[
                        html.B("Demanda energÃ©tica total en Austria [MW]"),
                        html.Hr(),
                        dcc.Graph(
                            id="plot_series",  
                        )
                    ],
                ),

            
            ],
        ),
    ],
)


@app.callback(
    Output(component_id="plot_series", component_property="figure"),
    [Input(component_id="datepicker-inicial", component_property="date"),
    Input(component_id="dropdown-hora-inicial-hora", component_property="value"),
    Input(component_id="slider-proyeccion", component_property="value")]
)
def update_output_div(date, hour, proy):

    if ((date is not None) & (hour is not None) & (proy is not None)):
        hour = str(hour)
        minute = str(0)

        initial_date = date + " " + hour + ":" + minute
        initial_date = pd.to_datetime(initial_date, format="%Y-%m-%d %H:%M")

        # Graficar
        plot = plot_series(data, initial_date, int(proy))
        return plot


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)