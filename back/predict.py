import os
import paddle
import numpy as np
import pandas as pd
from datetime import datetime,timedelta
from env.data_preprocess import LI_preprocess, feature_engineer ,time_range
from env.data_loader import TSDataset, TSPredDataset
from env.model import MultiTaskLSTM
from env.utils import EarlyStopping, calc_acc, to_unix_time, from_unix_time
import warnings
warnings.filterwarnings('ignore')
from traditional import Traditional_AR,Traditional_MA,Traditional_ARMA,Traditional_ARIMA,Traditional_SES,Traditional_DES\
    ,Traditional_TES,Traditional_SARIMA,Traditional_VAR,Traditional_VAR,Traditional_GARCH

def calc_acc(y_true, y_pred):
    y_pred = np.array(y_pred)
    y_true = np.array(y_true)
    rmse = np.sqrt(np.mean((y_true - y_pred)**2))
    return 1 - rmse/201000

def calc_acc1(y_true, y_pred):
    rmse = np.sqrt(np.mean((y_true - y_pred)**2))
    return 1 - rmse/201000

def forecast(df, turbine_id, out_file ,et):
    '''
    模型的预测函数，不直接调用，在predict函数里调用
    :param df: pd直接读到的表格
    :param turbine_id: 风机id int格式
    :param out_file: 输出文件路径：pred/原数据名+out。csv
    :param st: 开始时间，具体不定
    :param et: 结束时间，最后的结果为这个时间点前一天5点到这个时间点当天5点
    :return: 会在pred文件夹里输出一个xxxout.csv表，也可以返回result (dataframe格式)，前端可以看看哪个方便
    '''
    # 数据预处理
    # df = LI_preprocess(df)

    df = df.set_index("DATATIME")
    df = df[:et]
    df = df.reset_index()
    # 特征工程
    # df = feature_engineer(df)
    # 准备数据加载器
    input_len = 120*4
    pred_len = 24*4
    pred_dataset = TSPredDataset(df, input_len = input_len, pred_len = pred_len)
    pred_loader = paddle.io.DataLoader(pred_dataset, shuffle=False, batch_size=1, drop_last=False)
    # 定义模型
    model = MultiTaskLSTM()
    # 导入模型权重文件
    # 18:0.61 #14：0.61
    # 15号重灾区，0.51,12号：0.56，13：0.59，16号0.22，15号0.51 #11：44
    # 17号0.603、
    # if turbine_id == 19:
    #     model.set_state_dict(paddle.load(f'model/model_checkpoint_windid_14.pdparams'))
    # elif turbine_id == 11:
    #     model.set_state_dict(paddle.load(f'model/model_checkpoint_windid_14.pdparams'))
    # elif turbine_id == 15:
    #     model.set_state_dict(paddle.load(f'model/model_checkpoint_windid_14.pdparams'))
    # elif turbine_id == 16:
    #     model.set_state_dict(paddle.load(f'model/model_checkpoint_windid_14.pdparams'))
    # elif turbine_id == 12:
    #     model.set_state_dict(paddle.load(f'model/model_checkpoint_windid_14.pdparams'))
    # else:
    #     model.set_state_dict(paddle.load(f'model/model_checkpoint_windid_{turbine_id}.pdparams'))

    model.set_state_dict(paddle.load(f'model/model_checkpoint_windid_{turbine_id}.pdparams'))
    model.eval() # 开启预测
    for batch_id, data in enumerate(pred_loader()):
        x = data[0]
        y = data[1]
        outputs = model(x)    
        # apower = [x for x in outputs[0].numpy().squeeze()]
        yd15 = [x for x in outputs[0].numpy().squeeze()]
        ts_x = [from_unix_time(x) for x in data[2].numpy().squeeze(0)]
        ts_y = [from_unix_time(x) for x in data[3].numpy().squeeze(0)]

    result = pd.DataFrame({'DATATIME':ts_y,  'YD15':yd15})
    result['TurbID'] = turbine_id
    result = result[['TurbID', 'DATATIME', 'YD15']]
    # result.to_csv(out_file, index=False)
    return result


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

def predict_range(user_start_time,user_end_time,start_time,end_time):
    '''
    判断用户输入时间是否合法
    :param user_start_time: 用户填写开始的时间
    :param user_end_time: 用户填写的结束时间
    :param start_time: 数据的开始时间
    :param end_time: 数据的结束时间
    :return: 若合法就返回用户的开始，结束时间，格式为str，不合法就返回对应的txt
    '''
    try:
        range = pd.date_range(start=user_start_time, end=user_end_time, freq='15T')
    except:
        # return "There is something error with your time range"
        return 0
    # print(range)
    # print(len(range))
    if len(range) < 160:
        return "The datatime range is too short!"
    else:
        user_start_time=datetime.strptime(user_start_time, '%Y-%m-%d')
        start_time=datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        user_end_time=datetime.strptime(user_end_time, '%Y-%m-%d')
        end_time=datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        pre_start_time=user_end_time + timedelta(days=-1)
        if user_start_time<start_time or user_end_time>end_time:
            return "Setting time out of range!"
        else:
            return user_start_time.strftime('%Y-%m-%d'),pre_start_time.strftime('%Y-%m-%d'),user_end_time.strftime('%Y-%m-%d')



def predict(n,user_start_time,user_end_time):
    '''
    调用模型预测的函数
    :param n: 风机编号，主要这里为str格式
    :param start_time: 用户的开始时间（注意要先判断是否合法）
    :param end_time: 用户的结束结束
    :return: 预测结果，对应时间为用户填写的结束时间的前一天5五点到结束时间当天五点这24小时的预测结果
    '''
    # 得到完整的预测目标时间序列
    dates_between = get_dates_between(user_start_time, user_end_time)
    # ['2021-03-01 04:45:00', '2021-03-02 04:45:00']
    print(dates_between)
    # 计算时间

    files = os.listdir('data')
    # print(files)

    if not os.path.exists('pred'):
        os.mkdir('pred')
    # 第一步，完成数据格式统一
    f = n + ".csv"
    # 获取文件路径
    data_file = os.path.join('data', f)
    # print(data_file)
    out_file = os.path.join('pred', n + 'out.csv')
    # print(out_file)
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
    # print(df.info())
    df = df.set_index("DATATIME")
    ust_d1 = datetime.strptime(user_start_time, '%Y-%m-%d') + timedelta(days=-1)

    original_data = df[ust_d1.strftime('%Y-%m-%d') + " 05:00:00":user_end_time + " 04:45:00"]["YD15"]
    df = df.reset_index()

    r_list=[]
    for et in dates_between:
        r=forecast(df, turbine_id, out_file, et)
        r_list.append(r)
        result=pd.concat(r_list, axis=0)
    # result.to_csv(out_file, index=False)
    return result,original_data

def original(usn):
    f = usn + ".csv"
    # 获取文件路径
    data_file = os.path.join('data', f)
    df = pd.read_csv(data_file,
                     parse_dates=['DATATIME'],
                     infer_datetime_format=True,
                     dayfirst=True)
    # 数据预处理
    df = LI_preprocess(df)
    # 特征工程
    df = feature_engineer(df)
    df_dict = df.reset_index(drop=True)
    df_dict = df.to_dict(orient='list')
    return df_dict

def var_uploader(usn,ust,uet,varname):
    f = usn + ".csv"
    # 获取文件路径
    data_file = os.path.join('data', f)
    df = pd.read_csv(data_file,
                     parse_dates=['DATATIME'],
                     infer_datetime_format=True,
                     dayfirst=True)
    # 数据预处理
    df = LI_preprocess(df)
    # 特征工程
    df = feature_engineer(df)
    df_dict = df.reset_index(drop=True)
    df_dict = df.to_dict(orient='list')
    df = df.set_index("DATATIME")
    ust_d1 = datetime.strptime(ust, '%Y-%m-%d') + timedelta(days=-1)
    var = df[ust_d1.strftime('%Y-%m-%d') + " 04:45:00": uet + " 04:45:00"][varname]
    var_list = var.reset_index(drop=True)
    var_list = var_list.tolist()
    return var_list

def Model_Ensemble(n,user_start_time,user_end_time,weight,parameter):
    '''
        调用模型预测的函数
        :param n: 风机编号，主要这里为str格式
        :param start_time: 用户的开始时间（注意要先判断是否合法）
        :param end_time: 用户的结束结束
        :param weight:维度为11，对应11种不同的方法，各个预测方法的权重列顺序为：LSTM,AR,MA,ARMA,ARIMA,SES,DES,TES,SARIMA,VAR,ARMR-GARCH
        :param parameter:各个预测方法的参数值，顺序同上格式为嵌套的列表：[[],[],[]...]
        :return: 预测结果，对应时间为用户填写的结束时间的前一天5五点到结束时间当天五点这24小时的预测结果
        '''
    # 得到完整的预测目标时间序列
    dates_between = get_dates_between(user_start_time, user_end_time)
    # 计算时间

    files = os.listdir('data')
    # print(files)

    if not os.path.exists('pred'):
        os.mkdir('pred')
    # 第一步，完成数据格式统一
    f = n + ".csv"
    # 获取文件路径
    data_file = os.path.join('data', f)
    # print(data_file)
    out_file = os.path.join('pred', n + 'out.csv')
    # print(out_file)
    df = pd.read_csv(data_file,
                     parse_dates=['DATATIME'],
                     infer_datetime_format=True,
                     dayfirst=True)
    turbine_id = int(n)
    # 数据预处理
    df = LI_preprocess(df)
    # 特征工程
    df = feature_engineer(df)
    df = df.set_index("DATATIME")
    # 读取原数据来返回给前端
    # ust_d1 = datetime.strptime(user_start_time, '%Y-%m-%d') + timedelta(days=-1)
    original_data = df[user_start_time + " 05:00:00":user_end_time + " 04:45:00"]["YD15"]
    df = df.reset_index()

    # 创建日期范围
    date_range = pd.date_range(start=user_start_time + " 05:00:00",
                               end=user_end_time + " 04:45:00", freq='15T')

    # 创建 DataFrame
    reset_data = {'TurbID': [n] * len(date_range),
            'DATATIME': date_range,
            'YD15': [0] * len(date_range)}

    reset_data = pd.DataFrame(reset_data)
    # 创建用于补充传统模型空值的空序列
    zero_series = pd.Series([0] * len(date_range), index=date_range)

    # LSTM模型
    if weight[0]!=0:
        r_list = []
        for et in dates_between:
            r = forecast(df, turbine_id, out_file, et)
            r_list.append(r)
            r1 = pd.concat(r_list, axis=0)
        r1.set_index('DATATIME', inplace=True)
        r1=r1[pd.to_datetime(user_start_time + " 05:00:00"):pd.to_datetime(user_end_time + " 04:45:00")]
        r1=r1.reset_index()
    else:r1 = reset_data
    # AR模型
    if weight[1]!=0:
        r2,ts=Traditional_AR(n,user_start_time,user_end_time,p=parameter[1][0])
    else:r2=zero_series
    # MA模型
    if weight[2]!=0:
        r3,ts=Traditional_MA(n,user_start_time,user_end_time,q=parameter[2][0])
    else:r3=zero_series
    # ARMA模型
    if weight[3]!=0:
        r4,ts=Traditional_ARMA(n,user_start_time,user_end_time,p=parameter[3][0],q=parameter[3][1])
    else:r4=zero_series
    # ARIMA模型
    if weight[4]!=0:
        r5,ts=Traditional_ARIMA(n,user_start_time,user_end_time,p=parameter[4][0],q=parameter[4][1],d=parameter[4][2])
    else:r5=zero_series
    # SES模型
    if weight[5]!=0:
        r6,ts=Traditional_SES(n,user_start_time,user_end_time)
    else:r6=zero_series
    # DES模型
    if weight[6]!=0:
        r7,ts=Traditional_DES(n,user_start_time,user_end_time)
    else:r7=zero_series
    # TES模型
    if weight[7]!=0:
        r8,ts=Traditional_TES(n,user_start_time,user_end_time,SEASONAL_PERIODS=parameter[7][0])
    else:r8=zero_series
    # SARIMA模型
    if weight[8]!=0:
        r9,ts=Traditional_SARIMA(n,user_start_time,user_end_time,order=parameter[8][0],seasonal_order=parameter[8][1])
    else:r9=zero_series
    # VAR模型
    if weight[9]!=0:
        r10,ts=Traditional_VAR(n,user_start_time,user_end_time,select_cols=parameter[9][0],difference=parameter[9][1],order=parameter[9][2])
    else:r10=zero_series
    #
    if weight[10]!=0:
        r11,ts=Traditional_GARCH(n,user_start_time,user_end_time,p=parameter[10][0],q=parameter[10][1])
    else:r11=zero_series
    # print(zero_series)
    total_weight = sum(weight)
    # print("r1:",r1)
    # print("r2:",r2)
    # 对权重进行归一化
    normalized_weight = [w / total_weight for w in weight]
    print(normalized_weight)
    # 计算 YD15 乘以权重，并将结果汇总
    r1['YD15'] = r1['YD15'] * normalized_weight[0]
    r1['YD15'] += r2.values * normalized_weight[1]
    r1['YD15'] += r3.values * normalized_weight[2]
    r1['YD15'] += r4.values * normalized_weight[3]
    r1['YD15'] += r5.values * normalized_weight[4]
    r1['YD15'] += r6.values * normalized_weight[5]
    r1['YD15'] += r7.values * normalized_weight[6]
    r1['YD15'] += r8.values * normalized_weight[7]
    r1['YD15'] += r9.values * normalized_weight[8]
    print("test")
    print(len(r10))
    r1['YD15'] += r10.values * normalized_weight[9]
    print("test")
    r1['YD15'] += r11.values * normalized_weight[10]
    # print("test")
    # print("r11:",r11)

    # print("test2")
    # data['Weighted_YD15'] += data['YD15'].shift(2) * weights[2]
    result=r1
    # r_list.append(r)
    # result = pd.concat(r_list, axis=0)
    # result.to_csv(out_file, index=False)

    return result, original_data

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
    uet = "2021-03-08"
    weight=[1,1,1,1,1,1,1,1,1,1,1]
    parameter=[[],[7],[1],[6,1],[6,1,1],
               [],[],[24*4],[[0,1,0],[0,1,1,12]],
               [['WINDSPEED','PREPOWER','WINDDIRECTION','TEMPERATURE','HUMIDITY','PRESSURE','YD15'],1,3],
               [5,5]]


    # a = predict_range(ust, uet, st, et)
    # print(a)
    # # 4.在以上信息确认无误，参数全部合法后，调用后端predict函数，输出结果

    # r,o=predict("1",ust,uet)
    # print(r)
    # print(o)
    # R,o1=Model_Ensemble("1",ust,uet,weight,parameter)
    # print(R["YD15"])
    # print("test")
    # result_json = r.to_json(orient='records', date_format='iso')
    #
    result, oridinal = Model_Ensemble("1", ust, uet, weight=weight, parameter=parameter)
    # 将预测结果转为字典格式
    result_dict = result.reset_index(drop=True)
    result_dict = result_dict.to_dict(orient='list')
    rounded_values = [round(value, 2) for value in result_dict['YD15']]
    result_dict['YD15'] = rounded_values
    # 日期格式变换，变为str
    for i in range(len(result_dict["DATATIME"])):
        result_dict["DATATIME"][i] = result_dict["DATATIME"][i].strftime('%Y-%m-%d %H:%M:%S')
    # 将原对应时间的数据转为list格式
    oridinal_list = oridinal.reset_index(drop=True)
    oridinal_list = oridinal_list.tolist()
    # 再多上传一份原数据的系统生成预测功率，用于双指标散点图
    sys_pre = var_uploader("1", ust, uet, "PREPOWER")
    acc = calc_acc(y_true=oridinal_list, y_pred=result["YD15"])
    print(acc)