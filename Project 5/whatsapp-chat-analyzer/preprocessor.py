import pandas as pd
import re

def preprocessor(text):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s?(?:AM|PM)\s-\s'

    messages = re.split(pattern, text)[1:]
    dates = re.findall(pattern, text)

    df = pd.DataFrame({'user_messages': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format="%m/%d/%y, %I:%M %p - ")
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # separate users and messages
    users = []
    messages = []
    for message in df['user_messages']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # username
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_messages'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))

    df['period'] = period
    return df