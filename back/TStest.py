import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime,timedelta

from env.data_preprocess import LI_preprocess, feature_engineer
from predict import get_dates_between

from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller as ADF
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
plt.rcParams['font.sans-serif'] = ['SimHei']


wind_id = '1'
df = pd.read_csv(f'./data/{wind_id}.csv', parse_dates=['DATATIME'], infer_datetime_format=True, dayfirst=True)
df = df.sort_values(by='DATATIME', ascending=True)
# df.set_index('DATATIME', inplace=True)
# def decomposing(timeseries):
#     decomposition = seasonal_decompose(timeseries,freq=24*4)
#     trend = decomposition.trend
#     print(trend)
#     seasonal = decomposition.seasonal
#     residual = decomposition.resid

#     plt.figure(figsize=(16, 12))
#     plt.subplot(411)
#     plt.plot(timeseries, label='Original')
#     plt.legend(loc='best')
#     plt.subplot(412)
#     plt.plot(trend, label='Trend')
#     plt.legend(loc='best')
#     plt.subplot(413)
#     plt.plot(seasonal, label='Seasonarity')
#     plt.legend(loc='best')
#     plt.subplot(414)
#     plt.plot(residual, label='Residual')
#     plt.legend(loc='best')
#     plt.show()

def decomposing(n,user_start_time,user_end_time):
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
    # 获取文件路径
    data_file = os.path.join('data', f)
    if not os.path.exists('preprocess'):
        os.mkdir('preprocess')
    out_file = os.path.join('preprocess', n + 'out.csv')
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

    # 分解部分
    # 1.判断是否已生成对应算法的模型，如果没有，先生成模型
    
    Original_file = os.path.join('static','img',f'Original_{user_start_time}_decomposing_'+ n + '.png')
    print(Original_file)
    if not os.path.exists(Original_file):
        if not os.path.exists('static/img'):
            os.mkdir('static/img')   
    # train_set, test_set = train_test_split(df['YD15'], test_size=0.2, random_state=42)
    train_set = df['YD15'][:user_start_time + " 04:45:00"]
    ts = train_set
    # 分解时间序列
    decomposition = seasonal_decompose(ts,freq=24*4)
    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid

    plt.figure(figsize=(4, 2))
    plt.plot(ts, label='Original')
    plt.legend(loc='best')
    plt.savefig(Original_file,dpi=500)
        # 重置plt
        # plt.clf()
        # Trend_file = os.path.join('img',f'Original_{user_end_time}_decomposing_'+ n + '.png')
        # plt.figure(figsize=(3, 2))
        # plt.plot(trend, label='Trend')
        # plt.legend(loc='best')
        # plt.savefig(Trend_file,dpi=100)
        
        # Seasonarity_file = os.path.join('img',f'Original_{user_end_time}_decomposing_'+ n + '.png')
        # plt.figure(figsize=(3, 2))
        # plt.plot(seasonal, label='Seasonarity')
        # plt.legend(loc='best')
        # plt.savefig(Seasonarity_file,dpi=100)

        # Residual_file = os.path.join('img',f'Original_{user_end_time}_decomposing_'+ n + '.png')
        # plt.figure(figsize=(3, 2))
        # plt.plot(residual, label='Residual')
        # plt.legend(loc='best')
        # plt.savefig(Residual_file,dpi=100)

    # 2.如果已生成模型，直接调用模型
    # else:
    #     print("已进行分解")
    # 选出YD15这一列做出时间序列分解
    # ust_d1 = datetime.strptime(user_start_time, '%Y-%m-%d') + timedelta(days=-1)

    # original_data = df[ust_d1.strftime('%Y-%m-%d') + " 04:45:00":user_end_time + " 04:45:00"]
    # ts = original_data['YD15']
    # decomposition = seasonal_decompose(ts,freq=24*4)
    # trend = decomposition.trend
    # seasonal = decomposition.seasonal
    # residual = decomposition.resid
    
    # return ts,trend,seasonal,residual


def diff(n,user_start_time,user_end_time):
    # 第一步，完成数据格式统一
    f = n + ".csv"
    # 获取文件路径
    data_file = os.path.join('data', f)
    if not os.path.exists('preprocess'):
        os.mkdir('preprocess')
    out_file = os.path.join('preprocess', n + 'out.csv')
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

    # 分解部分
    # 1.判断是否已生成对应算法的模型，如果没有，先生成模型
    # Diff_file = os.path.join('img',f'{user_start_time}_Diff_'+ n + '.png')
    Diff_file = os.path.join('static','img','ADF' + '.png')
    print(Diff_file)
    if not os.path.exists(Diff_file):
        if not os.path.exists('static/img'):
            os.mkdir('static/img')    
    # train_set, test_set = train_test_split(df['YD15'], test_size=0.2, random_state=42)
    train_set = df['YD15'][:user_start_time + " 04:45:00"]
    timeseries = train_set
    timeseries_diff1 = timeseries.diff(1)
    timeseries_diff2 = timeseries_diff1.diff(1)

    timeseries_diff1 = timeseries_diff1.fillna(0)
    timeseries_diff2 = timeseries_diff2.fillna(0)


    timeseries_adf = ADF(timeseries.tolist())
    timeseries_diff1_adf = ADF(timeseries_diff1.tolist())
    timeseries_diff2_adf = ADF(timeseries_diff2.tolist())

    print('timeseries_adf : ', timeseries_adf)
    print('timeseries_diff1_adf : ', timeseries_diff1_adf)
    print('timeseries_diff2_adf : ', timeseries_diff2_adf)
    
    plt.figure(figsize=(3.5, 2))
    plt.xticks([])
    plt.legend(loc='best')
    # 隐藏x轴刻度值
    plt.plot(timeseries, label='Original', color='blue')
    plt.plot(timeseries_diff1, label='Diff1', color='red')
    plt.plot(timeseries_diff2, label='Diff2', color='purple')
    plt.legend(loc='best')
    plt.savefig(Diff_file,dpi=100)
    plt.clf()
    # plt.show()
    result_dict = {}
    result_dict["timeseries_adf"] = timeseries_adf
    result_dict["timeseries_diff1_adf"] = timeseries_diff1_adf
    result_dict["timeseries_diff2_adf"] = timeseries_diff2_adf
    return result_dict

# 从ADF检验结果来看，不需要进行一阶差分便能得到较好的平稳性。我们查看序列查看差分后序列的 ACF、PACF
def autocorrelation(n,user_start_time,user_end_time,d):
    # 第一步，完成数据格式统一
    f = n + ".csv"
    # 获取文件路径
    data_file = os.path.join('data', f)
    if not os.path.exists('preprocess'):
        os.mkdir('preprocess')
    out_file = os.path.join('preprocess', n + 'out.csv')
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

    # 分解部分
    # 1.判断是否已生成对应算法的模型，如果没有，先生成模型
    ACF_file = os.path.join('static','img','ACF'+'.png')
    print(ACF_file)
    if not os.path.exists(ACF_file):
        if not os.path.exists('static/img'):
            os.mkdir('static/img')      
    # train_set, test_set = train_test_split(df['YD15'], test_size=0.2, random_state=42)
    train_set = df['YD15'][:user_start_time + " 04:45:00"]
    timeseries = train_set
    if d > 0:
        timeseries_diff = timeseries.diff(d)
    else:
        timeseries_diff = timeseries
    
    plt.figure(figsize=(3, 2))
    plot_acf(timeseries_diff)
    plt.savefig(ACF_file,dpi=100)
    plt.clf()
    PACF_file = os.path.join('static','img','PACF' + '.png')
    plot_pacf(timeseries)
    plt.savefig(PACF_file,dpi=100)
    plt.clf()


if __name__=="__main__":
        # # 流程：1.用户先输入表格名称/风机号：
    # usn='18'
    # # 2.前端将该信息返回给后端，后端调用time_rang函数，
    # # 输出对应数据的时间范围，返回给前端，前端显示这一时间范围，指导用户填写合适的时间
    # st, et = time_range("18")
    # st = str(st)
    # et = str(et)
    # 3.用户填写时间范围，前端返回给后端，后端调用predict_range算法，判断时间范围是否合法，
    # 并返回开始时间、预测目标开始时间、预测目标结束时间
    ust = "2021-03-01"
    uet = "2021-03-02"
    # 2-28 5:00 到3-02的5：00

    # a = predict_range(ust, uet, st, et)
    # print(a)
    # # 4.在以上信息确认无误，参数全部合法后，调用后端predict函数，输出结果

    # ts,trend,seasonal,residual=decomposing("1",ust,uet)
    # print(ts)
    # print(trend)
    # print(seasonal)
    # print(residual)

    # decomposing("1",ust,uet)
    # diff("1",ust,uet)
    d = 1
    autocorrelation("1",ust,uet,d)

    # print(type(result_dict["YD15"][1]))

    # print(result)
    # dates_between = get_dates_between(ust, uet)
    # print(type(dates_between))
    # for date in dates_between:
    #     print(date)