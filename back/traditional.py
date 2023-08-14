import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
from arch import arch_model
from env.data_preprocess import LI_preprocess, feature_engineer


from statsmodels.tsa.seasonal import seasonal_decompose
# from statsmodels.tsa.arima_model import ARIMA, ARMA
from statsmodels.tsa.arima.model import ARIMA
# , ARMA
from statsmodels.tsa.holtwinters import SimpleExpSmoothing, Holt, ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.api import VAR
import arch
# from sklearn.model_selection import train_test_split
import pickle

plt.rcParams['font.sans-serif'] = ['SimHei']


# wind_id = '1'
# df = pd.read_csv(f'./data/{wind_id}.csv', parse_dates=['DATATIME'], infer_datetime_format=True, dayfirst=True)
# df = df.sort_values(by='DATATIME', ascending=True)

def get_dates_between(start_time, end_time):
    date_format = '%Y-%m-%d'  # 日期格式
    time_format = ' %H:%M:%S'  # 时间格式
    start_date = datetime.strptime(start_time, date_format).date()
    end_date = datetime.strptime(end_time, date_format).date()

    dates = []
    current_date = start_date

    while current_date <= end_date:
        date_string = current_date.strftime(date_format)
        date_string += " 04:45:00"  # 添加时间
        dates.append(date_string)
        current_date += timedelta(days=1)

    return dates


def Traditional_AR(n,user_start_time,user_end_time,p):
    '''
    调用模型预测的函数
    :param n: 风机编号，主要这里为str格式
    :param start_time: 用户的开始时间（注意要先判断是否合法）
    :param end_time: 用户的结束结束
    :return: 预测结果，对应时间为用户填写的结束时间的前一天5五点到结束时间当天五点这24小时的分解结果
    '''
    # 得到完整的预测目标时间序列
    dates_between = get_dates_between(user_start_time, user_end_time)
    # ['2021-03-01 04:45:00', '2021-03-02 04:45:00']
    # print(dates_between)
    # 计算时间
    # 第一步，完成数据格式统一
    f = n + ".csv"
    # 获取csv文件路径
    data_file = os.path.join('data', f)
    if not os.path.exists('preprocess'):
        os.mkdir('preprocess')
    out_file = os.path.join('preprocess', n + '.csv')
    df = pd.read_csv(data_file,
                    parse_dates=['DATATIME'],
                    infer_datetime_format=True,
                    dayfirst=True)
    try: turbine_id = int(n)
    except: turbine_id=1    
    # 数据预处理
    df = LI_preprocess(df)
    # 特征工程
    df = feature_engineer(df)
    # 将处理后的数据保存到本地
    df.to_csv(out_file, index=False)
    df = df.set_index("DATATIME")

    # 模型部分
    # 1.判断是否已生成对应算法的模型，如果没有，先生成模型
    
    model_file = os.path.join('tradtitionalmodel',f'{user_start_time}_{user_end_time}_AR({p})_'+ n + '.pkl')
    # print(model_file)
    if not os.path.exists(model_file):
        
        if not os.path.exists('tradtitionalmodel'):
            os.mkdir('tradtitionalmodel')    
        # 生成模型
        # train_set, test_set = train_test_split(df['YD15'], test_size=0.2, random_state=42)
        train_set = df['YD15'][:user_start_time + " 04:45:00"]
        model = ARIMA(train_set, order=(p,0,0)).fit()
        # 保存模型
        model.save(model_file)
    
    # 2.如果已生成模型，直接调用模型
    else:
        model = pickle.load(open(model_file,"rb"))
        # print('ok')
    # print('ok')
    # 选出YD15这一列做出时间序列分解
    # print(user_start_time)
    ust_d1 = datetime.strptime(user_start_time, '%Y-%m-%d') + timedelta(days=-1)
    # print(ust_d1)
    # print(ust_d1.strftime('%Y-%m-%d'))
    original_data = df[ust_d1.strftime('%Y-%m-%d') + " 04:45:00":user_end_time + " 04:45:00"]
    # print(original_data)
    # print(len(original_data))
    ts = original_data['YD15']
    
    # 3.调用模型，得到预测结果
    # r_list=[]
    # for et in dates_between:
    #     d = df[:et]
    #     r=model.predict(d, turbine_id, out_file, et)
    #     r_list.append(r)
    #     result=pd.concat(r_list, axis=0)
    # result.to_csv(out_file, index=False)
    result =  model.predict(user_start_time + ' 05:00:00',user_end_time + ' 04:45:00', dynamic=True)
    return result,ts

def Traditional_MA(n,user_start_time,user_end_time,q):
    '''
    调用模型预测的函数
    :param n: 风机编号，主要这里为str格式
    :param start_time: 用户的开始时间（注意要先判断是否合法）
    :param end_time: 用户的结束结束
    :return: 预测结果，对应时间为用户填写的结束时间的前一天5五点到结束时间当天五点这24小时的分解结果
    '''
    # 得到完整的预测目标时间序列
    dates_between = get_dates_between(user_start_time, user_end_time)
    # ['2021-03-01 04:45:00', '2021-03-02 04:45:00']
    # print(dates_between)
    # 计算时间
    # 第一步，完成数据格式统一
    f = n + ".csv"
    # 获取csv文件路径
    data_file = os.path.join('data', f)
    if not os.path.exists('preprocess'):
        os.mkdir('preprocess')
    out_file = os.path.join('preprocess', n + '.csv')
    df = pd.read_csv(data_file,
                    parse_dates=['DATATIME'],
                    infer_datetime_format=True,
                    dayfirst=True)
    try: turbine_id = int(n)
    except: turbine_id=1    
    # 数据预处理
    df = LI_preprocess(df)
    # 特征工程
    df = feature_engineer(df)
    # 将处理后的数据保存到本地
    df.to_csv(out_file, index=False)
    df = df.set_index("DATATIME")

    # 模型部分
    # 1.判断是否已生成对应算法的模型，如果没有，先生成模型
    model_file = os.path.join('tradtitionalmodel',f'{user_start_time}_{user_end_time}_MA({q})_'+ n + '.pkl')
    if not os.path.exists(model_file):
        print('not exist')
        if not os.path.exists('tradtitionalmodel'):
            os.mkdir('tradtitionalmodel')    
        # 生成模型
        # train_set, test_set = train_test_split(df['YD15'], test_size=0.2, random_state=42)
        train_set = df['YD15'][:user_start_time + " 04:45:00"]
        model = ARIMA(train_set, order=(0,0,q)).fit()
        # 保存模型
        model.save(model_file)
    
    # 2.如果已生成模型，直接调用模型
    else:
        model = pickle.load(open(model_file,"rb"))
    
    # 选出YD15这一列做出时间序列分解
    ust_d1 = datetime.strptime(user_start_time, '%Y-%m-%d') + timedelta(days=-1)

    original_data = df[ust_d1.strftime('%Y-%m-%d') + " 04:45:00":user_end_time + " 04:45:00"]
    ts = original_data['YD15']
    
    # 3.调用模型，得到预测结果
    result =  model.predict(user_start_time + ' 05:00:00',user_end_time + ' 04:45:00', dynamic=True)
    return result,ts

def Traditional_ARMA(n,user_start_time,user_end_time,p,q):
    '''
    调用模型预测的函数
    :param n: 风机编号，主要这里为str格式
    :param start_time: 用户的开始时间（注意要先判断是否合法）
    :param end_time: 用户的结束结束
    :return: 预测结果，对应时间为用户填写的结束时间的前一天5五点到结束时间当天五点这24小时的分解结果
    '''
    # 得到完整的预测目标时间序列
    dates_between = get_dates_between(user_start_time, user_end_time)
    # ['2021-03-01 04:45:00', '2021-03-02 04:45:00']
    # print(dates_between)
    # 计算时间
    # 第一步，完成数据格式统一
    f = n + ".csv"
    # 获取csv文件路径
    data_file = os.path.join('data', f)
    if not os.path.exists('preprocess'):
        os.mkdir('preprocess')
    out_file = os.path.join('preprocess', n + '.csv')
    df = pd.read_csv(data_file,
                    parse_dates=['DATATIME'],
                    infer_datetime_format=True,
                    dayfirst=True)
    try: turbine_id = int(n)
    except: turbine_id=1    
    # 数据预处理
    df = LI_preprocess(df)
    # 特征工程
    df = feature_engineer(df)
    # 将处理后的数据保存到本地
    df.to_csv(out_file, index=False)
    df = df.set_index("DATATIME")
    # print('ok')
    # 模型部分
    # 1.判断是否已生成对应算法的模型，如果没有，先生成模型
    model_file = os.path.join('tradtitionalmodel',f'{user_start_time}_{user_end_time}_ARMA({p,q})_'+ n + '.pkl')
    # print(model_file)
    if not os.path.exists(model_file):
        print('ok')
        if not os.path.exists('tradtitionalmodel'):
            print('ok')
            os.mkdir('tradtitionalmodel')    
        # 生成模型
        # train_set, test_set = train_test_split(df['YD15'], test_size=0.2, random_state=42)
        train_set = df['YD15'][:user_start_time + " 04:45:00"]
        model = ARIMA(train_set, order=(p,0,q)).fit()
        # 保存模型
        model.save(model_file)
    
    # 2.如果已生成模型，直接调用模型
    else:
        print('okok')
        model = pickle.load(open(model_file,"rb"))
        print('okok')
    
    
    # 选出YD15这一列做出时间序列分解
    ust_d1 = datetime.strptime(user_start_time, '%Y-%m-%d') + timedelta(days=-1)

    original_data = df[ust_d1.strftime('%Y-%m-%d') + " 04:45:00":user_end_time + " 04:45:00"]
    ts = original_data['YD15']
    
    # 3.调用模型，得到预测结果
    result =  model.predict(user_start_time + ' 05:00:00',user_end_time + ' 04:45:00', dynamic=True)
    return result,ts

def Traditional_ARIMA(n,user_start_time,user_end_time,p,d,q):
    '''
    调用模型预测的函数
    :param n: 风机编号，主要这里为str格式
    :param start_time: 用户的开始时间（注意要先判断是否合法）
    :param end_time: 用户的结束结束
    :return: 预测结果，对应时间为用户填写的结束时间的前一天5五点到结束时间当天五点这24小时的分解结果
    '''
    # 得到完整的预测目标时间序列
    dates_between = get_dates_between(user_start_time, user_end_time)
    # ['2021-03-01 04:45:00', '2021-03-02 04:45:00']
    # print(dates_between)
    # 计算时间
    # 第一步，完成数据格式统一
    f = n + ".csv"
    # 获取csv文件路径
    data_file = os.path.join('data', f)
    if not os.path.exists('preprocess'):
        os.mkdir('preprocess')
    out_file = os.path.join('preprocess', n + '.csv')
    df = pd.read_csv(data_file,
                    parse_dates=['DATATIME'],
                    infer_datetime_format=True,
                    dayfirst=True)
    try: turbine_id = int(n)
    except: turbine_id=1    
    # 数据预处理
    df = LI_preprocess(df)
    # 特征工程
    df = feature_engineer(df)
    # 将处理后的数据保存到本地
    df.to_csv(out_file, index=False)
    df = df.set_index("DATATIME")

    # 模型部分
    # 1.判断是否已生成对应算法的模型，如果没有，先生成模型
    model_file = os.path.join('tradtitionalmodel',f'{user_start_time}_{user_end_time}_ARIMA({p,d,q})_'+ n + '.pkl')
    if not os.path.exists(model_file):
        if not os.path.exists('tradtitionalmodel'):
            os.mkdir('tradtitionalmodel')    
        # 生成模型
        # train_set, test_set = train_test_split(df['YD15'], test_size=0.2, random_state=42)
        train_set = df['YD15'][:user_start_time + " 04:45:00"]
        model = ARIMA(train_set, order=(p,d,q)).fit()
        # 保存模型
        model.save(model_file)
    
    # 2.如果已生成模型，直接调用模型
    else:
        model = pickle.load(open(model_file,"rb"))
    
    # 选出YD15这一列做出时间序列分解
    ust_d1 = datetime.strptime(user_start_time, '%Y-%m-%d') + timedelta(days=-1)

    original_data = df[ust_d1.strftime('%Y-%m-%d') + " 04:45:00":user_end_time + " 04:45:00"]
    ts = original_data['YD15']
    
    # 3.调用模型，得到预测结果
    result =  model.predict(user_start_time + ' 05:00:00',user_end_time + ' 04:45:00')
    return result,ts

# SES（simple exponential smoothing）单指数平滑
def Traditional_SES(n,user_start_time,user_end_time):
    '''
    调用模型预测的函数
    :param n: 风机编号，主要这里为str格式
    :param start_time: 用户的开始时间（注意要先判断是否合法）
    :param end_time: 用户的结束结束
    :return: 预测结果，对应时间为用户填写的结束时间的前一天5五点到结束时间当天五点这24小时的分解结果
    '''
    # 得到完整的预测目标时间序列
    dates_between = get_dates_between(user_start_time, user_end_time)
    # ['2021-03-01 04:45:00', '2021-03-02 04:45:00']
    # print(dates_between)
    # 计算时间
    # 第一步，完成数据格式统一
    f = n + ".csv"
    # 获取csv文件路径
    data_file = os.path.join('data', f)
    if not os.path.exists('preprocess'):
        os.mkdir('preprocess')
    out_file = os.path.join('preprocess', n + '.csv')
    df = pd.read_csv(data_file,
                    parse_dates=['DATATIME'],
                    infer_datetime_format=True,
                    dayfirst=True)
    try: turbine_id = int(n)
    except: turbine_id=1    
    # 数据预处理
    df = LI_preprocess(df)
    # 特征工程
    df = feature_engineer(df)
    # 将处理后的数据保存到本地
    df.to_csv(out_file, index=False)
    df = df.set_index("DATATIME")

    # 模型部分
    # 1.判断是否已生成对应算法的模型，如果没有，先生成模型
    model_file = os.path.join('tradtitionalmodel',f'{user_start_time}_{user_end_time}_SES_'+ n + '.pkl')
    if not os.path.exists(model_file):
        if not os.path.exists('tradtitionalmodel'):
            os.mkdir('tradtitionalmodel')    
        # 生成模型
        # train_set, test_set = train_test_split(df['YD15'], test_size=0.2, random_state=42)
        train_set = df['YD15'][:user_start_time + " 04:45:00"]
        model = SimpleExpSmoothing(train_set).fit()
        # 保存模型
        model.save(model_file)
    
    # 2.如果已生成模型，直接调用模型
    else:
        model = pickle.load(open(model_file,"rb"))
    
    # 选出YD15这一列做出时间序列分解
    ust_d1 = datetime.strptime(user_start_time, '%Y-%m-%d') + timedelta(days=-1)

    original_data = df[ust_d1.strftime('%Y-%m-%d') + " 04:45:00":user_end_time + " 04:45:00"]
    ts = original_data['YD15']
    
    # 3.调用模型，得到预测结果
    result =  model.predict(user_start_time + ' 05:00:00',user_end_time + ' 04:45:00')
    return result,ts

# DES（double exponential smoothing）双指数平滑,Holt's 方法
def Traditional_DES(n,user_start_time,user_end_time):
    '''
    调用模型预测的函数
    :param n: 风机编号，主要这里为str格式
    :param start_time: 用户的开始时间（注意要先判断是否合法）
    :param end_time: 用户的结束结束
    :return: 预测结果，对应时间为用户填写的结束时间的前一天5五点到结束时间当天五点这24小时的分解结果
    '''
    # 得到完整的预测目标时间序列
    dates_between = get_dates_between(user_start_time, user_end_time)
    # ['2021-03-01 04:45:00', '2021-03-02 04:45:00']
    # print(dates_between)
    # 计算时间
    # 第一步，完成数据格式统一
    f = n + ".csv"
    # 获取csv文件路径
    data_file = os.path.join('data', f)
    if not os.path.exists('preprocess'):
        os.mkdir('preprocess')
    out_file = os.path.join('preprocess', n + '.csv')
    df = pd.read_csv(data_file,
                    parse_dates=['DATATIME'],
                    infer_datetime_format=True,
                    dayfirst=True)
    try: turbine_id = int(n)
    except: turbine_id=1    
    # 数据预处理
    df = LI_preprocess(df)
    # 特征工程
    df = feature_engineer(df)
    # 将处理后的数据保存到本地
    df.to_csv(out_file, index=False)
    df = df.set_index("DATATIME")

    # 模型部分
    # 1.判断是否已生成对应算法的模型，如果没有，先生成模型
    model_file = os.path.join('tradtitionalmodel',f'{user_start_time}_{user_end_time}_DES_'+ n + '.pkl')
    if not os.path.exists(model_file):
        if not os.path.exists('tradtitionalmodel'):
            os.mkdir('tradtitionalmodel')    
        # 生成模型
        # train_set, test_set = train_test_split(df['YD15'], test_size=0.2, random_state=42)
        train_set = df['YD15'][:user_start_time + " 04:45:00"]
        model = Holt(train_set).fit()
        # 保存模型
        model.save(model_file)
    
    # 2.如果已生成模型，直接调用模型
    else:
        model = pickle.load(open(model_file,"rb"))
    
    # 选出YD15这一列做出时间序列分解
    ust_d1 = datetime.strptime(user_start_time, '%Y-%m-%d') + timedelta(days=-1)

    original_data = df[ust_d1.strftime('%Y-%m-%d') + " 04:45:00":user_end_time + " 04:45:00"]
    ts = original_data['YD15']
    
    # 3.调用模型，得到预测结果
    result =  model.predict(user_start_time + ' 05:00:00',user_end_time + ' 04:45:00')
    return result,ts

# TES（triple exponential smoothing）三次指数平滑
def Traditional_TES(n,user_start_time,user_end_time,SEASONAL_PERIODS):
    '''
    调用模型预测的函数
    :param n: 风机编号，主要这里为str格式
    :param start_time: 用户的开始时间（注意要先判断是否合法）
    :param end_time: 用户的结束结束
    :return: 预测结果，对应时间为用户填写的结束时间的前一天5五点到结束时间当天五点这24小时的分解结果
    '''
    # 得到完整的预测目标时间序列
    dates_between = get_dates_between(user_start_time, user_end_time)
    # ['2021-03-01 04:45:00', '2021-03-02 04:45:00']
    # print(dates_between)
    # 计算时间
    # 第一步，完成数据格式统一
    f = n + ".csv"
    # 获取csv文件路径
    data_file = os.path.join('data', f)
    if not os.path.exists('preprocess'):
        os.mkdir('preprocess')
    out_file = os.path.join('preprocess', n + '.csv')
    df = pd.read_csv(data_file,
                    parse_dates=['DATATIME'],
                    infer_datetime_format=True,
                    dayfirst=True)
    try: turbine_id = int(n)
    except: turbine_id=1    
    # 数据预处理
    df = LI_preprocess(df)
    # 特征工程
    df = feature_engineer(df)
    # 将处理后的数据保存到本地
    df.to_csv(out_file, index=False)
    df = df.set_index("DATATIME")

    # 模型部分
    # 1.判断是否已生成对应算法的模型，如果没有，先生成模型
    model_file = os.path.join('tradtitionalmodel',f'{user_start_time}_{user_end_time}_TES({SEASONAL_PERIODS})_'+ n + '.pkl')
    if not os.path.exists(model_file):
        if not os.path.exists('tradtitionalmodel'):
            os.mkdir('tradtitionalmodel')    
        # 生成模型
        # train_set, test_set = train_test_split(df['YD15'], test_size=0.2, random_state=42)
        train_set = df['YD15'][:user_start_time + " 04:45:00"]
        model = ExponentialSmoothing(train_set,
                            trend='add',
                            seasonal='add',
                            seasonal_periods=SEASONAL_PERIODS,
                            damped=True).fit()
        # 保存模型
        model.save(model_file)
    
    # 2.如果已生成模型，直接调用模型
    else:
        model = pickle.load(open(model_file,"rb"))
    
    # 选出YD15这一列做出时间序列分解
    ust_d1 = datetime.strptime(user_start_time, '%Y-%m-%d') + timedelta(days=-1)

    original_data = df[ust_d1.strftime('%Y-%m-%d') + " 04:45:00":user_end_time + " 04:45:00"]
    ts = original_data['YD15']
    
    # 3.调用模型，得到预测结果
    result =  model.predict(user_start_time + ' 05:00:00',user_end_time + ' 04:45:00')
    return result,ts

# SARIMA（Seasonal ARIMA）,SARIMA(p,d,q)(P,D,Q,s)总共7个参数，可以分成2类，3个非季节参数(p,d,q)，和4个季节参数(P,D,Q,s)。
def Traditional_SARIMA(n,user_start_time,user_end_time,order,seasonal_order):
    '''
    调用模型预测的函数
    :param n: 风机编号，主要这里为str格式
    :param start_time: 用户的开始时间（注意要先判断是否合法）
    :param end_time: 用户的结束结束
    :return: 预测结果，对应时间为用户填写的结束时间的前一天5五点到结束时间当天五点这24小时的分解结果
    '''
    # 得到完整的预测目标时间序列
    dates_between = get_dates_between(user_start_time, user_end_time)
    # ['2021-03-01 04:45:00', '2021-03-02 04:45:00']
    # print(dates_between)
    # 计算时间
    # 第一步，完成数据格式统一
    f = n + ".csv"
    # 获取csv文件路径
    data_file = os.path.join('data', f)
    if not os.path.exists('preprocess'):
        os.mkdir('preprocess')
    out_file = os.path.join('preprocess', n + '.csv')
    df = pd.read_csv(data_file,
                    parse_dates=['DATATIME'],
                    infer_datetime_format=True,
                    dayfirst=True)
    try: turbine_id = int(n)
    except: turbine_id=1    
    # 数据预处理
    df = LI_preprocess(df)
    # 特征工程
    df = feature_engineer(df)
    # 将处理后的数据保存到本地
    df.to_csv(out_file, index=False)
    df = df.set_index("DATATIME")

    # 模型部分
    # 1.判断是否已生成对应算法的模型，如果没有，先生成模型
    model_file = os.path.join('tradtitionalmodel',f'{user_start_time}_{user_end_time}_SARIMA({order}{seasonal_order})_'+ n + '.pkl')
    if not os.path.exists(model_file):
        if not os.path.exists('tradtitionalmodel'):
            os.mkdir('tradtitionalmodel')    
        # 生成模型
        # train_set, test_set = train_test_split(df['YD15'], test_size=0.2, random_state=42)
        train_set = df['YD15'][:user_start_time + " 04:45:00"]
        model = SARIMAX(train_set, order=order,seasonal_order=seasonal_order).fit()
        # 保存模型
        model.save(model_file)
    
    # 2.如果已生成模型，直接调用模型
    else:
        model = pickle.load(open(model_file,"rb"))
    
    # 选出YD15这一列做出时间序列分解
    ust_d1 = datetime.strptime(user_start_time, '%Y-%m-%d') + timedelta(days=-1)

    original_data = df[ust_d1.strftime('%Y-%m-%d') + " 04:45:00":user_end_time + " 04:45:00"]
    ts = original_data['YD15']
    
    # 3.调用模型，得到预测结果
    result =  model.predict(user_start_time + ' 05:00:00',user_end_time + ' 04:45:00')
    return result,ts

# select_cols：考虑的因素，difference：差分阶数,order：fit阶数
def Traditional_VAR(n,user_start_time,user_end_time,select_cols,difference,order):
    '''
    调用模型预测的函数
    :param n: 风机编号，主要这里为str格式
    :param start_time: 用户的开始时间（注意要先判断是否合法）
    :param end_time: 用户的结束结束
    :return: 预测结果，对应时间为用户填写的结束时间的前一天5五点到结束时间当天五点这24小时的分解结果
    '''
    # 得到完整的预测目标时间序列
    dates_between = get_dates_between(user_start_time, user_end_time)
    # ['2021-03-01 04:45:00', '2021-03-02 04:45:00']
    # print(dates_between)
    # 计算时间
    # 第一步，完成数据格式统一
    f = n + ".csv"
    # 获取csv文件路径
    data_file = os.path.join('data', f)
    if not os.path.exists('preprocess'):
        os.mkdir('preprocess')
    out_file = os.path.join('preprocess', n + '.csv')
    df = pd.read_csv(data_file,
                    parse_dates=['DATATIME'],
                    infer_datetime_format=True,
                    dayfirst=True)
    try: turbine_id = int(n)
    except: turbine_id=1    
    # 数据预处理
    df = LI_preprocess(df)
    # 特征工程
    df = feature_engineer(df)
    # 将处理后的数据保存到本地
    df.to_csv(out_file, index=False)
    df = df.set_index("DATATIME")

    # 模型部分
    train_set = df[select_cols][:user_start_time + " 04:45:00"]
    var_train_differenced = train_set.diff(difference).dropna()
    # 1.判断是否已生成对应算法的模型，如果没有，先生成模型
    model_file = os.path.join('tradtitionalmodel',f'{user_start_time}_{user_end_time}_VAR({select_cols,difference,order})_'+ n + '.pkl')
    if not os.path.exists(model_file):
        if not os.path.exists('tradtitionalmodel'):
            os.mkdir('tradtitionalmodel')    
        # 生成模型
        # train_set, test_set = train_test_split(df['YD15'], test_size=0.2, random_state=42)

        model = VAR(var_train_differenced).fit(order)
        # 保存模型
        model.save(model_file)
    
    # 2.如果已生成模型，直接调用模型
    else:
        model = pickle.load(open(model_file,"rb"))
    
    # 选出YD15这一列做出时间序列分解
    ust_d1 = datetime.strptime(user_start_time, '%Y-%m-%d') + timedelta(days=-1)

    original_data = df[ust_d1.strftime('%Y-%m-%d') + " 04:45:00":user_end_time + " 04:45:00"]
    ts = original_data['YD15']
    
    # 3.调用模型，得到预测结果
    lag_order = model.k_ar
    forecast_input = var_train_differenced.values[-lag_order:]
    # print(var_train_differenced)
    fc =  model.forecast(forecast_input, steps=4*24*(len(dates_between)-1))
    # 创建空的dataframe
    d = pd.DataFrame(columns=var_train_differenced.columns + '_d')
    for et in dates_between[:-1]:
        da = df[et:]
        # da = da.reset_index()
        df_forecast = pd.DataFrame(fc, index=da.index[:4*24*(len(dates_between)-1)], columns=var_train_differenced.columns + '_d')
        # 拼接不同时间段的预测结果的df_forecast进行行拼接
        df_forecast = pd.concat([d, df_forecast], axis=0)
    print(df_forecast)
    # difference阶差分还原
    for _ in range(difference):
        df_forecast['YD15_d'] = df_forecast['YD15_d'].cumsum() + train_set['YD15'].iloc[-difference]
    df_forecast['YD15'] = df_forecast['YD15_d']
    # result = df_forecast['YD15_d'].cumsum().add(train_set['YD15'].iloc[-lag_order])
    result = df_forecast['YD15']
    return result,ts

# select_cols：考虑的因素，difference：差分阶数,order：fit阶数
def Traditional_GARCH(n, user_start_time, user_end_time, p, q):
    '''
    调用GARCH模型预测的函数
    :param n: 风机编号，主要这里为str格式
    :param user_start_time: 用户的开始时间（注意要先判断是否合法）
    :param user_end_time: 用户的结束时间
    :param p: GARCH(p, q)模型中的p参数
    :param q: GARCH(p, q)模型中的q参数
    :return: 预测结果，对应时间为用户填写的结束时间的前一天5五点到结束时间当天五点这24小时的波动预测结果
    '''
    # 得到完整的预测目标时间序列
    dates_between = get_dates_between(user_start_time, user_end_time)

    # 计算时间
    f = n + ".csv"
    # 获取csv文件路径
    data_file = os.path.join('data', f)
    if not os.path.exists('preprocess'):
        os.mkdir('preprocess')
    out_file = os.path.join('preprocess', n + '.csv')
    df = pd.read_csv(data_file,
                     parse_dates=['DATATIME'],
                     infer_datetime_format=True,
                     dayfirst=True)
    try:
        turbine_id = int(n)
    except:
        turbine_id = 1

    # 数据预处理
    df = LI_preprocess(df)
    # 特征工程
    df = feature_engineer(df)
    # 将处理后的数据保存到本地
    df.to_csv(out_file, index=False)
    df = df.set_index("DATATIME")

    # 模型部分
    # 选出YD15这一列作为时间序列
    ust_d1 = datetime.strptime(user_start_time, '%Y-%m-%d') + timedelta(days=-1)
    original_data = df[user_start_time + " 05:00:00":user_end_time + " 04:45:00"]
    ts = original_data['YD15']
    date_range = pd.date_range(start=user_start_time + " 05:00:00",
                               end=user_end_time + " 04:45:00", freq='15T')
    # 3. 调用模型，得到预测结果
    n = len(ts)
    mu = np.mean(ts)
    returns = ts - mu

    omega = np.var(returns)
    alpha = np.zeros(p)
    beta = np.zeros(q)

    for i in range(p):
        alpha[i] = 0.8  # Modify as needed

    for i in range(q):
        beta[i] = 0.1  # Modify as needed

    sigma_sq = np.zeros(n)
    sigma_sq[:max(p, q)] = omega

    for t in range(max(p, q), n):
        sigma_t = omega
        for i in range(p):
            sigma_t += alpha[i] * returns[t - i - 1] ** 2
        for i in range(q):
            sigma_t += beta[i] * sigma_sq[t - i - 1]
        sigma_sq[t] = sigma_t*0.6


    result = sigma_sq[-n:]* (10 ** -5)
    result = pd.Series(result, index=date_range)

    return result, ts

if __name__=="__main__":
    # # 流程：1.用户先输入表格名称/风机号：
    # usn='18'
    # # 2.前端将该信息返回给后端，后端调用time_rang函数，
    # # 输出对应数据的时间范围，返回给前端，前端显示这一时间范围，指导用户填写合适的时间
    # 3.用户填写时间范围，前端返回给后端，后端调用predict_range算法，判断时间范围是否合法，
    # 并返回开始时间、预测目标开始时间、预测目标结束时间
    ust = "2021-03-03"
    uet = "2021-03-05"
    # 2-28 5:00 到3-02的5：00
    # # 4.在以上信息确认无误，参数全部合法后，调用后端predict函数，输出结果
    p = 6
    result,oridinal=Traditional_AR("1",ust,uet,p)
    q = 1
    # result,oridinal=Traditional_MA("1",ust,uet,q)
    # result,oridinal=Traditional_ARMA("1",ust,uet,p,q)
    d = 1
    # result,oridinal=Traditional_ARIMA("1",ust,uet,p,d,q)
    # result,oridinal=Traditional_SES("1",ust,uet)
    # result,oridinal=Traditional_DES("1",ust,uet)
    SEASONAL_PERIODS = 24*4
    # result,oridinal=Traditional_TES("1",ust,uet,SEASONAL_PERIODS)
    order=(0,1,0)
    seasonal_order=(0,1,1,12)
    # result,oridinal=Traditional_SARIMA("1",ust,uet,order,seasonal_order)
    select_cols=['WINDSPEED','PREPOWER','WINDDIRECTION','TEMPERATURE','HUMIDITY','PRESSURE','YD15']
    difference = 1
    order = 3
    # result,oridinal=Traditional_VAR("1",ust,uet,select_cols,difference,order)
    # print(result)
    # print(oridinal)
    # 将日期索引变成列，并给列分别命名为DATATIME,YD15
    # result_dict = result.reset_index()
    # result_dict = result_dict.rename(columns={'index':'DATATIME',0:'YD15'})
    
    # print(result_dict)
    # result_dict = result_dict.to_dict(orient='list')
    # print(result_dict)
    # data=original("1")
    # print(data)
    # oridinal_list = o.reset_index(drop=True)
    # oridinal_list = oridinal_list.tolist()
    # print(oridinal_list)



    # print(type(result_dict["YD15"][1]))

    # print(result)
    # dates_between = get_dates_between(ust, uet)
    # print(type(dates_between))
    # for date in dates_between:
    #     print(date)