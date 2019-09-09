from server import app, server
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import time
import dash_table
from dashapp.util.parse_config import get_config
import pandas as pd
from dashapp.api.sel.calc_profit import calc_profit, calc_stock_profit
from dashapp.api.sel.banks.util.get_env import get_env
from dashapp.layouts.page2 import gen_p2

curr_env = get_env()
# if curr_env not in ["production"]:
if curr_env not in ["production"]:
    from dashapp.util.data_sel import gen_bank_info_sel
else:
    from dashapp.util.data_gcf import gen_bank_info_gcf

def generate_table(dataframe, max_rows=500):
    if dataframe.empty == True:
        return ""
    # print(dataframe)
    return dbc.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="NavbarSimple",
    brand_href="#",
    color="primary",
    dark=True,
)

report_title = html.Div([
    dbc.Row([
        dbc.Col(
            html.Img(
                src=app.get_asset_url(
                    "cool-logo.png"
                ),
                className="page-1a",
            )
        ),
        dbc.Col(
            [
                html.H6("David Li"),
                html.H5("Financial Report"),
                html.H6(time.ctime()),
            ],
            className="page-1b",
        ),
        dbc.Col(
            [
                html.H6("Add Basic Auth"),
                html.H5("Add Stuff Later"),
                html.H6("Full Money Amount"),
            ],
            className="page-1e",
        ),
    ], className="page-1c")
], className="page-1d")

if curr_env not in ["production"]:
    rbc_data, td_data = gen_bank_info_sel()
else:
    rbc_data, td_data = gen_bank_info_gcf()

mf_profit, mf_profit_values = calc_profit(rbc_data, td_data)
stock_profit, stock_profit_values = calc_stock_profit()
stock_profit = stock_profit.reset_index()
total_profit = sum(mf_profit_values) + sum(stock_profit_values)

config = get_config()
td_fund_names = config["banks"]["td"]["codes"]
td_data_part = td_data[td_data['Fund Code'].isin(td_fund_names)]
rbc_fund_names = config["banks"]["rbc"]["codes"]
rbc_data_part = rbc_data[rbc_data['Code'].isin(rbc_fund_names)]
partial_stats = html.Div([
    dbc.Row([
        dbc.Col([
            html.H4("RBC Funds"),
            generate_table(rbc_data_part)
        ], width=6),
        dbc.Col([
            html.H4("TD Funds"),
            generate_table(td_data_part),
        ], width=6)
    ]),
])
metadata_cards = dbc.Row([
    dbc.Col([
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4("Stocks", className="card-title"),
                        html.H6( round(sum(stock_profit_values), 2), className="card-subtitle"),
                    ]
                )
            ],
            style={"width": "12rem"}
        )
    ]),
    dbc.Col([
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4("Mutual Funds", className="card-title"),
                        html.H6( round(sum(mf_profit_values), 2), className="card-subtitle"),
                    ]
                )
            ],
            style={"width": "12rem"}
        )
    ]),
    dbc.Col([
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4("Total Profit", className="card-title"),
                        html.H6(round(total_profit, 2), className="card-subtitle"),
                    ]
                )
            ],
            style={"width": "12rem"}
        )
    ]),
    dbc.Col([
    ]),
])
gains_losses = dbc.Row([
        dbc.Col([
            html.H4("Profit MF Funds"),
            generate_table(mf_profit)
        ]),
        dbc.Col([
            html.H4("Stock Funds"),
            generate_table(stock_profit)
        ])
    ])
rbc_data_trim = rbc_data = rbc_data.drop(['Series'], axis=1)
basic_stats = dbc.Row([
    dbc.Col([
        html.H4("RBC Funds"),
        generate_table(rbc_data_trim)
    ], width=6),
    dbc.Col([
        html.H4("TD Funds"),
        generate_table(td_data),
    ], width=6)
])

page_1_tabs = dbc.Tabs([
        dbc.Tab(gains_losses, label="Gains/Losses", tab_id='gains-losses'),
        dbc.Tab(partial_stats, label="Partial Stats", tab_id='part-stats'),
        dbc.Tab(basic_stats, label="Full Stats", tab_id='full-stats')
        # dbc.Tab(
        #     html.Iframe(src=f'https://www.rbcgam.com/en/ca/products/mutual-funds/RBF900/detail',
        #     className='full-width'),
        #     label="Iframe", tab_id='iframe'
        # )
    ],
    id="tabs",
    active_tab="gains-losses",
)

page_1 = dbc.Row(
        [
            dbc.Col([
                report_title,
                html.Br(),
                html.Br(),
                metadata_cards,
                html.Br(),
                page_1_tabs,
                html.Br(),
                html.Br()
                # only here for demo purposes
                ], className='shadow-page')
        ]
    )

page_2 = gen_p2()

app.layout = dbc.Container([page_1, page_2])