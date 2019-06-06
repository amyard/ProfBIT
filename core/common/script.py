import pandas as pd
import datetime
import pytz


pd.set_option('display.max_colwidth', -1)


def get_orders_by_date(df):
    df.rename(columns={'amount':'Количество', 'order_id':'Номер заказа', 'order_id__created_date':'Дата', 'product_name':'Продукт', 'product_price':'Цена'},
              inplace=True)
    df['Товары'] = df.apply(lambda x: x["Продукт"]+str(' * ')+ str(x["Количество"]), axis=1)

    new_df = df.groupby(['Номер заказа', 'Дата'])['Цена'].agg({'Сумма':sum}).reset_index()
    new_df2 = df.groupby(['Номер заказа', 'Дата'])['Товары'].apply(lambda pr: ', '.join(pr)).reset_index()

    last = pd.merge(new_df2, new_df, on=['Номер заказа', 'Дата']).sort_values('Сумма', ascending=False).reset_index(drop=True)
    last = last[['Дата','Номер заказа','Сумма','Товары']]
    last['Дата'] = last['Дата'].apply(lambda x: x.tz_convert(None))
    # last['Дата'] = last['Дата'].apply(lambda x: x.split('+')[0])
    last = last.to_html(classes="table table-bordered df-tables")
    return last