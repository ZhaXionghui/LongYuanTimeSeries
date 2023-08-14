from sklearn.impute import KNNImputer
import numpy as np
import pandas as pd
import os

def time_range(csv_name):
    '''
    读取对应表格，并返回对应表格的时间范围
    :param csv_name: 数据名称，即读取csv_name.csv表格
    :return: 如果存在该表格，返回表格的开始时间和结束时间；如果不存在返回txt
    '''
    # 计算时间
    files = os.listdir('data')
    # print(files)

    if not os.path.exists('pred'):
        os.mkdir('pred')
    # 第一步，完成数据格式统一
    f = csv_name + ".csv"
    # 获取文件路径
    data_file = os.path.join('data', f)
    # print(data_file)
    out_file = os.path.join('pred', csv_name + 'out.csv')
    # print(out_file)
    try:
        df = pd.read_csv(data_file,
                         parse_dates=['DATATIME'],
                         infer_datetime_format=True,
                         dayfirst=True)
    except:
        print("无法读取到表格，请检查名称填写是否正确")
        return 0
    df = df.sort_values(by='DATATIME', ascending=True)
    print('df.shape:', df.shape)
    print(f"Time range from {df.iloc[0]['DATATIME']} to {df.iloc[-1]['DATATIME']}")
    return df.iloc[0]["DATATIME"],df.iloc[-1]["DATATIME"]


def LI_preprocess(df):
    """数据预处理：线性插值补充缺失值
        1、读取数据
        2、数据排序
        3、去除重复值
        4、重采样（可选）
        5、缺失值处理:线性插值法 Linear interpolation
        6、异常值处理
    """
    # ===========读取数据===========
    df = df.sort_values(by='DATATIME', ascending=True)
    print('df.shape:', df.shape)
    print(f"Time range from {df['DATATIME'].values[0]} to {df['DATATIME'].values[-1]}")

    # ===========去除重复值===========
    df = df.drop_duplicates(subset='DATATIME', keep='first')
    print('After Dropping dulicates:', df.shape)

    # ===========重采样（可选） + 线性插值补充缺失值===========
    df = df.set_index('DATATIME')
    # 重采样（可选）：比如04风机缺少2022-04-10和2022-07-25两天的数据，重采样会把这两天数据补充进来
    # df = df.resample(rule=to_offset('15T').freqstr, label='right', closed='right').interpolate(method='linear', limit_direction='both').reset_index()
    # TODO 尝试一些其他缺失值处理方式，比如，用同时刻附近风机的值求均值填补缺失值
    # 优先使用同时刻的ROUND(A.POWER,0)去弥补YD15的空值
    df["YD15"].fillna(value=df["ROUND(A.POWER,0)"], inplace=True)
    # 余下的用插值方法补充
    df = df.interpolate(method='linear', limit_direction='both').reset_index()
    print('After Resampling:', df.shape)

    # ===========异常值处理==============
    # 当实际风速为0时，功率置为0
    df.loc[df['ROUND(A.WS,1)'] == 0, 'YD15'] = 0

    # TODO 当YD15或ROUND(A.WS,1)为负时，改为0处理（实际为风速过小时，发电机和工作人员用电情况，不太好预测）

    # TODO 风速过大但功率为0的异常：先设计函数拟合出：实际功率=f(风速)，
    # 然后代入异常功率的风速获取理想功率，替换原异常功率

    # TODO 对于在特定风速下的离群功率（同时刻用IQR检测出来），做功率修正（如均值修正）
    return df


def KNN_preprocess(df, n=8):
    """数据预处理：KNN方法补充缺失值
                1、读取数据
                2、数据排序
                3、去除重复值
                4、重采样（可选）
                5、缺失值处理
                6、异常值处理
            """
    # ===========读取数据===========
    df = df.sort_values(by='DATATIME', ascending=True)
    print('df.shape:', df.shape)
    print(f"Time range from {df['DATATIME'].values[0]} to {df['DATATIME'].values[-1]}")

    # ===========去除重复值===========
    df = df.drop_duplicates(subset='DATATIME', keep='first')
    print('After Dropping duplicates:', df.shape)

    # ===========重采样（可选）+ 缺失值处理==========
    df = df.set_index('DATATIME')

    # 重采样（可选）：比如04风机缺少2022-04-10和2022-07-25两天的数据，重采样会把这两天数据补充进来
    # df = df.resample(rule=to_offset('15T').freqstr, label='right', closed='right').interpolate(method='linear', limit_direction='both').reset_index()
    # TODO 尝试一些其他缺失值处理方式，比如，用同时刻附近风机的值求均值填补缺失值
    # 优先使用同时刻的ROUND(A.POWER,0)去弥补YD15的空值
    df["YD15"].fillna(value=df["ROUND(A.POWER,0)"], inplace=True)

    # KNN补充余下的空值
    imputer = KNNImputer(n_neighbors=n)
    imputer.fit_transform(df["YD15"].values.reshape(-1, 1))
    imputed_data = imputer.fit_transform(df["YD15"].values.reshape(-1, 1))
    # print(imputed_data)
    df["YD15"] = imputed_data
    print('After Resampling:', df.shape)

    # 余下其他数据的用插值方法补充
    df = df.interpolate(method='linear', limit_direction='both').reset_index()
    print('After Resampling:', df.shape)

    # ===========异常值处理==============
    # 当实际风速为0时，功率置为0
    df.loc[df['ROUND(A.WS,1)'] == 0, 'YD15'] = 0
    # TODO 当YD15或ROUND(A.WS,1)为负时，改为0处理（实际为风速过小时，发电机和工作人员用电情况，不太好预测）

    # TODO 风速过大但功率为0的异常：先设计函数拟合出：实际功率=f(风速)，
    # 然后代入异常功率的风速获取理想功率，替换原异常功率

    # TODO 对于在特定风速下的离群功率（同时刻用IQR检测出来），做功率修正（如均值修正）
    return df


def D_preprocess(df):
    """数据预处理：丢弃法，直接扔去缺失值
                1、读取数据
                2、数据排序
                3、去除重复值
                4、重采样（可选）
                5、缺失值处理
                6、异常值处理
            """
    # ===========读取数据===========
    df = df.sort_values(by='DATATIME', ascending=True)
    print('df.shape:', df.shape)
    print(f"Time range from {df['DATATIME'].values[0]} to {df['DATATIME'].values[-1]}")

    # ===========去除重复值===========
    df = df.drop_duplicates(subset='DATATIME', keep='first')
    print('After Dropping dulicates:', df.shape)
    # 优先使用同时刻的ROUND(A.POWER,0)去弥补YD15的空值
    df["YD15"].fillna(value=df["ROUND(A.POWER,0)"], inplace=True)
    # ===========直接删除余下的YD15存在缺失的数据===========
    df = df.set_index('DATATIME')
    df = df.dropna(subset=['YD15'])
    print('Dropped data:', df.shape)
    df['DATATIME'] = pd.date_range(start=df.index[0], periods=len(df), freq='15T')
    df = df.set_index("DATATIME")
    # 余下的用插值方法补充
    df = df.interpolate(method='linear', limit_direction='both').reset_index()
    print('After Resampling:', df.shape)

    # ===========异常值处理==============
    # 当实际风速为0时，功率置为0
    df.loc[df['ROUND(A.WS,1)'] == 0, 'YD15'] = 0
    print(f"Time range from {df['DATATIME'].values[0]} to {df['DATATIME'].values[-1]}")
    return df


def feature_engineer(df):
    """特征工程：时间戳特征"""
    # 时间戳特征
    df['month'] = df.DATATIME.apply(lambda row: row.month, 1)
    df['day'] = df.DATATIME.apply(lambda row: row.day, 1)
    df['weekday'] = df.DATATIME.apply(lambda row: row.weekday(), 1)
    df['hour'] = df.DATATIME.apply(lambda row: row.hour, 1)
    df['minute'] = df.DATATIME.apply(lambda row: row.minute, 1)

    # TODO 挖掘更多特征：差分序列、同时刻风场/邻近风机的特征均值/标准差等
    return df