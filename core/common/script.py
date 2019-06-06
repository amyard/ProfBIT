import pandas as pd
import datetime
import pytz


pd.set_option('display.max_colwidth', -1)


def clean_date(x):
    d = x.tz_convert(None)
    d = d.strftime('%d.%m.%Y %I:%M')
    return d



def get_orders_by_date(df):
    df.rename(columns={'amount':'Количество', 'order_id':'Номер заказа', 'order_id__created_date':'Дата', 'product_name':'Продукт', 'product_price':'Цена'},
              inplace=True)
    df['Товары'] = df.apply(lambda x: x["Продукт"]+str(' * ')+ str(x["Количество"]), axis=1)

    new_df = df.groupby(['Номер заказа', 'Дата'])['Цена'].agg({'Сумма':sum}).reset_index()
    new_df2 = df.groupby(['Номер заказа', 'Дата'])['Товары'].apply(lambda pr: ', '.join(pr)).reset_index()

    last = pd.merge(new_df2, new_df, on=['Номер заказа', 'Дата']).sort_values('Сумма', ascending=False).reset_index(drop=True)
    last = last[['Дата','Номер заказа','Сумма','Товары']]
    last['Номер заказа'] = last['Номер заказа'].apply(lambda x: f'Заказ {x}')
    last['Дата'] = last['Дата'].apply(lambda x: clean_date(x))
    last = last.to_html(classes="table table-bordered df-tables")
    return last


def get_top_hundred_product(df):
    df.rename(columns={'amount':'Количество', 'order_id':'Номер заказа', 'order_id__created_date':'Дата', 'product_name':'Продукт', 'product_price':'Цена'},
                  inplace=True)
    df['Дата'] = df['Дата'].apply(lambda x: clean_date(x))
    df['Номер заказа'] = df['Номер заказа'].apply(lambda x: f'Заказ {x}')

    df['Цена'] = df['Цена'].apply(lambda x: f'Общая цена {x}')
    df['Дата'] = df['Дата'].apply(lambda x: f'Дата {x}')
    df['Товары'] = df.apply(lambda x: x['Номер заказа']+' - '+x['Цена']+' - '+x['Дата'], axis=1)

    new_df = df.groupby(['Продукт'])['Количество'].agg({'Сумма':sum}).reset_index()
    new_df2 = df.groupby(['Продукт'])['Товары'].apply(lambda pr: ', '.join(pr)).reset_index()

    last = pd.merge(new_df, new_df2, on=['Продукт']).sort_values('Сумма', ascending=False).reset_index(drop=True)
    last=last.head(100)
    last.drop('Сумма', axis=1, inplace=True)
    last.index+=1
    last = last.to_html(classes="table table-bordered df-tables")
    return last