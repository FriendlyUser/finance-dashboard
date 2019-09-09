import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from ..api.stats.getStats import get_statscan, exchange_rates

def generate_table(dataframe, max_rows=100):
    if dataframe.empty == True:
        return html.P("Nothing")
    return dbc.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

def gen_p2():
  """ Generate page 2
  """
  stats_df = get_statscan()
  print(stats_df)
  stats_df.columns = ['Region', '$ (100 M)', 'Description', 'Month', 'Change %', 'Period']
  stats_html = generate_table(stats_df, 18)
  ex_df = exchange_rates()
  ex_df = ex_df.reset_index()
  ex_df.columns = ['Dollar', 'Conversion']
  ex_html = generate_table(ex_df, 18)
  return html.Div([
          html.Br(),
          html.Br(),
          html.Br(),
          html.Br(),
          dbc.Row([
            dbc.Col([
              stats_html,
              dbc.Alert(
                [
                    "0 corresponds to Canada and 10 to BC",
                    html.Br(),
                    "Fields need to optimizated later"
                ],
                color="primary",
              ),
              ex_html
            ], className='shadow-page')
          ])
        ])
