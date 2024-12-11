import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np

def mape(raw, actual: str = "actual", fcst: str = "fcst"):
    raw = raw.loc[pd.notnull(raw.fcst) & pd.notnull(raw.actual)]
    return 1 - abs(raw[actual] - raw[fcst]) / raw[actual]
def correlation(y, y_hat):
    sigma_p = y.std(axis=-1)
    sigma_g = y_hat.std(axis=-1)
    mean_p = y.mean(axis=-1)
    mean_g = y_hat.mean(axis=-1)
    return ((y - np.expand_dims(mean_p, axis=-1)) * (y_hat - np.expand_dims(mean_g, axis=-1))).mean(axis=-1) / (sigma_p * sigma_g)
def smape(raw, actual: str = "actual", fcst: str = "fcst"):
    raw_ = raw.copy()
    raw_ = raw_.loc[pd.notnull(raw_.fcst) & pd.notnull(raw_.actual)]
    raw_["smape"] = 1 - abs(raw_[actual] - raw_[fcst]) / (abs(raw_[actual]) + abs(raw_[fcst]))
    raw_.loc[(raw_[actual] == 0) & (raw_[fcst] == 0), "smape"] = 1
    return raw_["smape"]

def credible_interval_plot_plotly(input_inf, data, subtitle="tbd"):
    
    interval = ["fcst0.02","fcst0.1","fcst0.25","fcst0.5","fcst0.75","fcst0.9","fcst0.98"]
    data[interval] = data.loc[:, interval].round(0)
    input_inf = input_inf.sort_values("timestamp")
    data = data.sort_values("targetdate")

    
    qty_ = go.Scatter(x=input_inf.loc[:, "timestamp"],y=input_inf.loc[:,"actual"],
                                      line=go.scatter.Line(color="Blue", width=2, dash="dashdot"), name="Actual")

    mean_ = go.Scatter(x=data.loc[:, "targetdate"],y=data.loc[:,"fcst0.5"],
                                      line=go.scatter.Line(color="Crimson", width=2, dash="dashdot"), name="Mean of fcst")
    upper_75 = go.Scatter(x=data.loc[:, "targetdate"],
                                 y=data.loc[:,"fcst0.75"],
                                 line=go.scatter.Line(color="dimgray", width=0.5),
                                 fill="tonexty", legendgroup="group",
                                 legendgrouptitle_text="Credible Interval (p:0.5)",
                                 name="Upper Credible Interval")
    
    lower_25 = go.Scatter(x=data.loc[:, "targetdate"],
                                 y=data.loc[:,"fcst0.25"],
                                 line=go.scatter.Line(color="dimgray", width=0.5),
                                 fill="tonexty",legendgroup="group",
                                 legendgrouptitle_text="Credible Interval (p:0.5)",
                                 name="Lower Credible Interval")
        
    upper_9 = go.Scatter(x=data.loc[:, "targetdate"],
                                 y=data.loc[:,"fcst0.9"],
                                 line=go.scatter.Line(color="dimgray", width=0.5),
                                 fill="tonexty", legendgroup="group1",
                                 legendgrouptitle_text="Credible Interval (p:0.8)",
                                 name="Upper Credible Interval")   
    lower_1 = go.Scatter(x=data.loc[:, "targetdate"],
                                 y=data.loc[:,"fcst0.1"],
                                 line=go.scatter.Line(color="dimgray", width=0.5),
                                 fill="tonexty", legendgroup="group1",
                                 legendgrouptitle_text="Credible Interval (p:0.8)",
                                 name="Lower Credible Interval")
        
    upper_98 = go.Scatter(x=data.loc[:, "targetdate"],
                                 y=data.loc[:,"fcst0.98"],
                                 line=go.scatter.Line(color="dimgray", width=0.5),
                                 fill="tonexty",
                                 legendgroup="group2",
                                 legendgrouptitle_text="Credible Interval (p:0.96)",
                                 name="Upper Credible Interval")
    
    lower_02 = go.Scatter(x=data.loc[:, "targetdate"],
                                 y=data.loc[:,"fcst0.02"],
                                 line=go.scatter.Line(color="dimgray", width=0.5),
                                 fill="tonexty",
                                 legendgroup="group2",
                                 legendgrouptitle_text="Credible Interval (p:0.96)",
                                 name="Lower Credible Interval")
    
    layout =  go.Layout(title = {'text':"<b> Forecasting Result </b>",
                                 'x':0.44,
                                 'y':0.88,
                                 'xanchor':'center',
                                 'yanchor':'top'},
                        width  = 950, height = 450,
                        annotations = [dict(xref='paper',
                                            yref='paper',
                                            x=0.5, y=1.1,
                                            showarrow=False,
                                            text = subtitle,
                                            font_size=14)],
                        # paper_bgcolor = "white",
                        # plot_bgcolor  = "whitesmoke",
                        font_family   = "LG스마트체 Regular",
                        # font_color    = "black"
                        )
    fig_list = [qty_, mean_,  upper_75, lower_25, upper_9, lower_1, upper_98, lower_02]

    fig = go.Figure(data=[qty_, mean_, upper_75, lower_25, upper_9, lower_1, upper_98, lower_02], layout=layout)  
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(count=3, label="3y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    return fig
