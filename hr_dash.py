import dash_bootstrap_components as dbc
import plotly.express as px

import matplotlib.pyplot as plt
import numpy as np
from plotly.tools import mpl_to_plotly
import webbrowser
from threading import Timer

import random
import pandas as pd
import plotly.express as px
pd.options.mode.chained_assignment = None  # default='warn'
from dash import Dash, html, dcc, Input, Output,dash_table
import plotly.graph_objects as go

url="https://raw.githubusercontent.com/zohrehkazemi/pyDash/main/c-sample.csv"

data = pd.read_csv(url)



##########################_____Hire Date  process_____##############################

hire= data.loc[:,['Hire Date']]
hire_date = pd.to_datetime(data["Hire Date"])
#print("last hire date:  ",max(hire_date))
#print("first hire date:  ",min(hire_date))
hire_df=pd.DataFrame(hire_date)
hire_df['year']=hire_df['Hire Date'].dt.year
hire_df['month']=hire_df['Hire Date'].dt.month
year_list_hire=hire_df['year'].value_counts().keys().tolist()
num_employee_in_year=hire_df['year'].value_counts().tolist()
h_data={'year':year_list_hire,'Number of employees hired each year':num_employee_in_year}
hire_dataframe=pd.DataFrame(h_data)
last_hire_df_in_year=hire_dataframe.sort_values(by=['year', 'Number of employees hired each year'])
#print("Hire Date:number of employee in year",last_hire_df_in_year)


###################################Exite Date process###########################

exit=((data.loc[:, ['Exit Date']]))
exit_date= pd.to_datetime(data["Exit Date"])

#print("last Exit date:  ",max(exit_date))
#print("first Exit date:  ",min(exit_date))
exit_df=pd.DataFrame(exit_date)
exit_df['year-x']=exit_df['Exit Date'].dt.year
exit_df['month-x']=exit_df['Exit Date'].dt.month


year_list_exit=exit_df['year-x'].value_counts().keys().tolist()
num_employee_in_year_exit=exit_df['year-x'].value_counts().tolist()
year_list_exit_final=[]
for i in year_list_exit:
       r=round(i)
       year_list_exit_final.append(r)
e_data={'year-x':year_list_exit_final,'Number of employees exited each year':num_employee_in_year_exit}
exit_dataframe=pd.DataFrame(e_data)
last_exit_df_in_year=exit_dataframe.sort_values(by=['year-x', 'Number of employees exited each year'])
#print("Exit Date:number of employee in year: \n\n\n\n\n",last_exit_df_in_year)

result = pd.concat([last_hire_df_in_year,last_exit_df_in_year], axis=1).reindex(last_hire_df_in_year.index)

result = result.drop('year-x', axis=1)
result=result.fillna(0)

#print(result)

#############################################################per dep

hire= data.loc[:,['Hire Date']]
data['hire'] = pd.to_datetime(data["Hire Date"])
data['exit'] = pd.to_datetime(data['Exit Date'])
data['hire-year']=data['hire'].dt.year
data['exit-year']=data['exit'].dt.year

hire_dep_df=pd.DataFrame(data[['Department','hire-year']])
hire_dep_df=hire_dep_df.sort_values(by=['hire-year', 'Department'])

"""result = pd.concat([hire_dep_df,exit_dep_df], axis=1).reindex(hire_dep_df.index)
result = result.drop('x-dep', axis=1)
result=result.fillna(0)
print('res is\n',result)"""

#for text on bar
exit_dep_df=pd.DataFrame(data[['Department','exit-year']])
exit_dep_df=exit_dep_df.fillna(0)
mask = exit_dep_df['exit-year'] == 0
# select all rows except the ones that contain 0
exit_dep_df = exit_dep_df[~mask]
exit_dep_list=exit_dep_df['Department'].value_counts(sort=False).sort_index(ascending=True).keys().tolist()
exit_dep_num_list=exit_dep_df['Department'].value_counts(sort=False).sort_index(ascending=True).tolist()
hire_dep_num_list=hire_dep_df['Department'].value_counts(sort=False).sort_index(ascending=True).tolist()


last_exit_datafram=pd.DataFrame({'department':exit_dep_list,
                                 'exit_per_dep':exit_dep_num_list,
                                'The number of people hired in each department':hire_dep_num_list})

#print(last_exit_datafram)

################################per dep

female=data['Gender'].value_counts()['Female']
#print("number of female is :",female)
male=data['Gender'].value_counts()['Male']
#print("number of male is :",male)
sum_employee=male+female

sum_exit_employee=sum(num_employee_in_year_exit)
active_employee=sum_employee-sum_exit_employee
attrition_rate=((sum_exit_employee/sum_employee)*100)


###################################### country processing #############################

country=((data.loc[:, ['Country']]))
#print(country.describe())
#print(country.nunique())
count=data["Country"].value_counts()
number_country_list=list(count)
name_country=list(count.keys())
countryDf=pd.DataFrame({'Country':name_country,'Number':number_country_list})


############################Gender and Age processing########################################
age=((data.loc[:, ['Age']]))
#print(age.describe())
count0=0
count1=0
count2=0
count3=0
count4=0
count5=0

for i in  data['Age']:
    if i<25:
        count0+=1
    if 25 <= i < 35:
        count1 += 1
    elif 35 <= i < 45:
        count2 += 1
    elif 45<= i < 55:
        count3 += 1
    elif 55<= i < 65:
        count4+=1
    else:
        count5+=1
"""print("under 25=",count0)
print("25-35 =:",count1)
print("35-45 =:",count2)
print("45-55 =:",count3)
print("55-65 =:",count4)
print(">65:",count5)"""
total_number=[count0,count1,count2,count3,count4,count5]
ageRange=['under 25','25-35','35-45','45-55','55-65','>65']
ageDf=pd.DataFrame({'Age Range':ageRange,'Number':total_number})


labels_age=['25-35','35-45','45-55','55-65','>65']
bins_age=[25,35,45,55,65,66]
data['AgeGroup Age'] = pd.cut(data['Age'], bins=bins_age, labels=labels_age, right=False)
#print(data)
last=data[['AgeGroup Age','Gender']].groupby('AgeGroup Age').value_counts()


#female=data['Gender'].value_counts()['Female']
#print("number of female is :",female)
#male=data['Gender'].value_counts()['Male']
#print("number of male is :",male)
count_gender= data['Gender'].value_counts()
genderDf=pd.DataFrame({'Gender':data['Gender'].value_counts().keys(),'Number':data['Gender'].value_counts()})
#print((genderDf))
sum_employee=male+female
perfemal=(female/sum_employee)*100
permale=(male/sum_employee)*100

####################################################salary process#######################
salary=((data.loc[:,['Annual Salary']]))
firstsalary = data['Annual Salary'].str.extract(r'(\d......)', expand=False)
final_salary=firstsalary.str.replace(',','')
numbers = pd.to_numeric(final_salary)
#print(sum(numbers))
number_df=pd.DataFrame(numbers)
#print(number_df)
salaryDf=pd.DataFrame({'count':numbers.describe().keys(),'Annual Salary':round(numbers.describe())  })

salaryDf=salaryDf.drop('count')

new_row = {'count': 'Total', 'Annual Salary': sum(numbers)}

# Append the dictionary to the DataFrame
salaryDf.loc[len(salaryDf)] = new_row

# Reset the index
salaryDf= salaryDf.reset_index(drop=True)

#################################################Bouns process#######################################

help_list=data[["Department","Bonus %"]].groupby("Department").value_counts()
int_bon=data['Bonus %'].str.extract(r'(\d.)', expand=False)
int_bon=int_bon.str.replace('%','')
data['int_bon'] = pd.to_numeric(int_bon)
jobs=data['Job Title'].value_counts(sort=False).sort_index(ascending=True).keys().tolist()
number_employee_per_job=data['Job Title'].value_counts(sort=False).sort_index(ascending=True).tolist()
jobDf=pd.DataFrame({'jobs':jobs,'number employee':number_employee_per_job})

zerobon=data['int_bon'].value_counts()[0]
contain_bon=data['int_bon'].value_counts().sum()

total_bon=contain_bon-zerobon
zero = data['int_bon'] == 0
data= data[~zero]

data1=pd.DataFrame(data[['int_bon','Job Title','Department']].groupby('Department').value_counts())

"""print(zerobon,contain_bon,total_bon)
print(data['int_bon'].describe())

print(data['Job Title'].value_counts(sort=False).sort_index(ascending=True).keys().tolist())
print(data['Job Title'].value_counts(sort=False).sort_index(ascending=True).tolist())"""
jobDf_bon=pd.DataFrame({'jobs':data['Job Title'].value_counts(sort=False).sort_index(ascending=True).keys().tolist(),
                        'count':data['Job Title'].value_counts(sort=False).sort_index(ascending=True).tolist()})



#print(data[['int_bon','Job Title']].groupby('int_bon').value_counts().keys())

labels=['5-10','10-20','20-30','30-40']
bins=[5,10,20,30,40]
data['AgeGroup Bonus'] = pd.cut(data['int_bon'], bins=bins, labels=labels, right=False)

#******************************************************************************************##
roundbutton = {
    "border": None,
    "border-radius": "70%",
    "padding": 0,
    "backgroundColor": "#98B5FF",
    "color": "year",
    "textAlign": "center",
    "display": "h",
    "fontSize": 10,
    "height":90,
    "width": 90,
    "margin":30,

}

app = Dash(external_stylesheets=[dbc.themes.JOURNAL,dbc.themes.SOLAR])
server=app.server

def bounFigure():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.pie(ageDf, names='Age Range',
                                   values='Number',
                                   color='Age Range',
                                  title="نمودار توزیع کارکنان بر حسب سن").update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                        #xaxis_title="",
                        #yaxis_title="",
                        title_x=.5,

                    ).update_coloraxes(showscale=False),

                config={
                        'displayModeBar': False
                    }
                ),

            ])
        ),
    ])

def countryFigure():
    colors = ["#" + ''.join([random.choice('0123456789ABCDEF') for i in range(6)])
              for j in range(len(name_country))]

    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.pie(countryDf, names='Country',
                                   values='Number',
                                  title="Disterbution chart of employees by Country",color='Country').update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                        xaxis_title="",
                        yaxis_title="",
                        title_x=.5,
                        uniformtext=dict(minsize=20, mode='hide'),
                        #autosize=False,width=500,height=485

                    ).update_coloraxes(showscale=False),

                config={
                        'displayModeBar': False
                    }
                ),

            ])
        ),
    ])


def exitdepFigure():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.bar(last_exit_datafram, x='department',
                                   y='The number of people hired in each department',
                                   color='exit_per_dep',
                                  title="نمودار استخدام و خروج کارکنان هر بخش").update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                        xaxis_title="",
                        yaxis_title="",
                        title_x=.5,

                    ).update_coloraxes(showscale=False),

                config={
                        'displayModeBar': False
                    }
                ),

            ])
        ),
    ])

def drawTable():

    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div(children=[

                    dash_table.DataTable(salaryDf.to_dict('records'), [{"name": i, "id": i} for i in salaryDf.columns],
                                         style_cell={'textAlign': 'center'}, style_as_list_view=True,
                                         style_header={
                                             'backgroundColor': 'rgb(30, 30, 30)',
                                             'color': 'white', 'border': '1px solid red'
                                         },
                                         style_data={
                                             'backgroundColor': 'rgb(50, 50, 50)',
                                             'color': 'white',
                                             'border': '1px solid blue',

                                             'height': 10,
                                             'lineHeight': '15px'
                                         },




                                         )

                ])

            ])
        ),

    ])



# Text field
def drawText1():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2([attrition_rate, '%', html.Br(), "Attrition Rate"],style={'color':'silver','font-weight':'bold'}),

                ], style={'textAlign': 'center','font_family': 'Garamond'})
            ])
        ),
    ])

def drawText2():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2([sum_exit_employee, html.Br(), "Attrition Count"],style={'color':'silver','font-weight':'bold'}),

                ], style={'textAlign': 'center','font_family': 'Garamond'})
            ])
        ),
    ])

def drawText3():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2([active_employee, html.Br(), " Active Employees"],style={'color':'silver','font-weight':'bold'}),

                ], style={'textAlign': 'center'})
            ])
        ),
    ])

def drawText4():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2([sum_employee, html.Br(), " Employee Count "],style={'color':'silver','font-weight':'bold'}),

                ], style={'textAlign': 'center'})
            ])
        ),
    ])

def drawText5():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2([female, '  👩🏻‍🦰' , html.Br(),male, "  🧑🏻‍💼",],style={'color':'silver','font-weight':'bold'}),

                ], style={'textAlign': 'center'})
            ])
        ),
    ])
# Build App
app.layout =html.Div([
html.Div(children=[
    html.Div(children=[
        html.H1('Foulad Asin Company', style={'backgroundColor': 'darkslategray', 'color': 'white','font_family': 'Algerian','font-weight': 'bold'}),
        html.H3('Human resources dashboard', style={'fontsize': '100'}),
        html.H3('by Zohreh Kazemi'),
        html.Hr(),
        #html.Button([attrition_rate, '%', html.Br(), "نرخ خروج"], style=roundbutton),
        #html.Button([sum_exit_employee, html.Br(), " کارمندان خارج شده"], style=roundbutton),
        #html.Button([active_employee, html.Br(), "کارمندان فعال"], style=roundbutton),
        #html.Button([sum_employee, html.Br(), " کل کارمندان"], style=roundbutton),

    ], style={'textAlign': 'center', 'backgroundColor': 'slate',
              'color': 'lightsteelblue', }),



]),

    dbc.Card(
        dbc.CardBody([

            dbc.Row([

                dbc.Col([
                    drawText1()
                ], width=3),
                dbc.Col([
                    drawText2()
                ], width=3),
                dbc.Col([
                    drawText3()
                ], width=3),

                dbc.Col([
                    drawText4()
                ], width=2),
                dbc.Col([
                    drawText5()
                ], width=1),

            ], align='center'),
            html.Br(),
            dbc.Row([
                dbc.Col([
                html.Label(['please select a graph:'], style={'font-weight': 'bold'}),
                dcc.Dropdown(result.columns[1:], value=result.columns[1], id='input', multi=True,
                             style={'backgroundColor': '#0C5962',"font-family": "sans-serif","color":"black",'font-weight': 'bold','font-size':23},),

                html.Div(children=[

                dcc.Graph(id='output_chart',config={
        'displayModeBar': False
    }),

                ]),


                ], width=8),
                dbc.Col([
                    html.H3("Annual Salary Table",style={'textAlign': 'center', 'backgroundColor': 'slate'}),
                    drawTable(),

                ], width=4),
            ], align='center'),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.Br(),
                    countryFigure(),
                    html.Br(),
                    html.Br(),

                ], width=3),


                dbc.Col([
                    html.Label(['Age Group & Gender :'], style={'font-weight': 'bold'}),

                    dbc.Card(
                        dbc.CardBody([

                            dcc.Dropdown(

                                options=[
                                    {'label': 'Gender Chart', 'value': 'graph1'},
                                    {'label': 'Age Chart', 'value': 'graph2'},
                                   # {'label': 'هیستوگرام جنسیت وسن', 'value': 'graph3'}

                                ], value='graph2', id='radio',
                                style={'backgroundColor': '#0C5962', "color": "black", 'font-weight': 'bold','font-size':22},

                            ),

                            html.Div(children=[
                                dcc.Graph(id='graph', config={
                                    'displayModeBar': False}),

                            ]),

                        ])
                    )

                ], width=3),

                dbc.Col([
                    html.Label(['Bonus & Jobs :'], style={'font-weight': 'bold', 'textAlign': 'center'}),

                    dbc.Card(
                        dbc.CardBody([

                            dcc.Dropdown(

                                options=[
                                    {'label': 'Job Positions ', 'value': 'graph5'},
                                    {'label': 'Job Positions with bonuses', 'value': 'graph4'},
                                    {'label': 'Bonus range of each job position', 'value': 'graph6'}

                                ], value='graph5', id='bon', style={'backgroundColor': '#0C5962', "color": "black",
                                                                    'font-weight': 'bold','font-size':23},

                            ),

                            html.Div(children=[
                                dcc.Graph(id='graph_bon', config={
                                    'displayModeBar': False}),

                            ]),

                        ])
                    )

                ], width=6),
             ]),

        ]), color = 'dark'
    )
])
@app.callback(Output('output_chart', 'figure',),
              Input('input', 'value'))

def hire_exitFigure(x):

    figur = px.bar(
        result,  # dataframe
        x='year',  # x
        y=x,
        labels={"x": "year", "y": "number of employee"},  # define lable
        #color='year',
        color_continuous_scale=px.colors.sequential.RdBu,  # color
        # text=offence_district.groupby("Offence")["Total"].agg(sum),#text
        title="Hire and Exit Chart", # title
        orientation="v" , # vertical bar chart
        )
    figur.update_layout(title_x=0.5,
                       #plot_bgcolor='#0C0F12' ,
                       title_font_size=35,
                       template='plotly_dark',
                       plot_bgcolor='rgba(0, 0, 0, 0)',
                       paper_bgcolor='rgba(0, 0, 0, 0)',
                       xaxis_title="Year",
                       yaxis_title="Number in year",


                       )



    return figur



@app.callback( Output('graph', 'figure'),
              [Input('radio','value')])

def gender_age(value):


    if value=='graph1':
          return px.pie(genderDf,names='Gender',values='Number',color_discrete_sequence=px.colors.sequential.Rainbow,
                                  title="Disterbution chart of employees by Gender").update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                        xaxis_title="",
                        yaxis_title="",
                        title_x=.5,


                    )




   # if value=='graph3':
        #  return px.bar(data,x='Gender',y='Age',color='AgeGroup Age',barmode='group',
                             #     title="نمودار توزیع کارکنان بر حسب سن و جنسیت").update_layout(
                       # template='plotly_dark',
                      #  plot_bgcolor= 'rgba(0, 0, 0, 0)',
                      #  paper_bgcolor= 'rgba(0, 0, 0, 0)',
                       # xaxis_title="",
                       # yaxis_title="",
                       # title_x=.5,
                      #  yaxis=dict(
                      #  showticklabels=False,
                      #  title='',
             # ),
               #     )


    else:
         return px.pie(ageDf, names='Age Range',
                                   values='Number',
                                   color='Age Range',
                                  title="Disterbution chart of employees by Age",
                        color_discrete_sequence=px.colors.sequential.Rainbow_r,hole=0.40).update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                        uniformtext = dict(minsize = 20, mode = 'hide'),
                        title_x=.5,

                    )

##########bouns def################

@app.callback( Output('graph_bon', 'figure'),
              [Input('bon','value')])

def bouns(value):


    if value=='graph4':
          return px.bar(jobDf_bon,x='count',
                        y='jobs',title="Job Positions with bonuses").update_traces(marker_color = 'yellow',
                                                #marker_line_color = 'white',
                                                marker_line_width = 2,
                                                opacity = 1).update_layout(
                                                template='plotly_dark',
                                                plot_bgcolor= 'rgba(0, 0, 0, 0)',
                                                paper_bgcolor= 'rgba(0, 0, 0, 0)',
                                                xaxis_title="",
                                                yaxis_title="",
                                                title_x=.5,



                    )




    if value=='graph5':
          return px.bar(jobDf,x='jobs',
                        y='number employee',title="Job Positions").update_traces(marker_color = 'yellowgreen',
                                             #   marker_line_width = 2,
                                                opacity = 1).update_layout(
                                                template='plotly_dark',
                                                plot_bgcolor= 'rgba(0, 0, 0, 0)',
                                                paper_bgcolor= 'rgba(0, 0, 0, 0)',
                                                xaxis_title="",
                                                yaxis_title="",
                                                title_x=.5,


                    )


    else:
        return px.bar(data,x='Job Title',y='int_bon',
                      color='AgeGroup Bonus',color_discrete_sequence=px.colors.sequential.Rainbow_r,title="Bonus range of each job position").update_yaxes(showticklabels=False).update_layout(
                     template='plotly_dark',
                     plot_bgcolor='rgba(0, 0, 0, 0)',
                     paper_bgcolor='rgba(0, 0, 0, 0)',
                     xaxis_title="",
                     yaxis_title="",
                     title_x=.5,

        )


#port = 5000 # or simply open on the default `8050` port

#def open_browser():
	#webbrowser.open_new("http://localhost:{}".format(8888))

# Run app and display result inline in the notebook

if __name__ == '__main__':
    app.run_server(debug=True)
