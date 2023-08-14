from flask import Flask, request
from flask_cors import CORS
import pandas as pd
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.dialects.mysql import LONGTEXT
# import uuid
import requests
import json
import os
import sys


from predict import predict_range,predict,original,var_uploader,Model_Ensemble,calc_acc,calc_acc1
from env.data_preprocess import LI_preprocess, feature_engineer ,time_range
from traditional import Traditional_AR,Traditional_MA,Traditional_ARMA,Traditional_ARIMA,Traditional_SES,Traditional_DES,Traditional_TES,Traditional_SARIMA,Traditional_VAR,Traditional_VAR,Traditional_GARCH
from TStest import diff, autocorrelation
'''
'code': 0,
'msg': '登录成功',

'code': 0,
'msg': '数据存在',

'code': 0,
'msg': '注册成功',

状态码
'code': 4000,
'msg': '用户名错误'

'code': 4001,
'msg': '密码错误'

'code': 4002,
'msg': '用户名不存在'

'code':4003,
'msg': '注册用户名已存在'

'code': 4004,
'msg': '确认密码错误'

'code': 4005,
'msg': '答案错误'

'''
# FB 为前后端交互部分
# DB 为后端与数据库交互部分



app = Flask(__name__)
# 设置可以跨域访问
CORS(app, supports_credentials=True)




@app.route('/Gettimerange', methods=['POST'])
def Gettimerange():
    # 获取客户端数据
    usn = request.json.get('usn')
    try:
        st, et = time_range(usn)
        # test = str(st)
        # print(test)
        # print(type(test))

        return {
        'code': 0,
        'data': {
            'st': str(st),
            'et': str(et)
        }
            }
    # st, et = time_range("18")
    except:
        return {
            'code': 4000,
            'data':{
                'msg': '不包含该风机数据'
            }
        }
    

@app.route('/modelpredict', methods=['POST'])
def modelpredict():
    # 获取客户端数据
    st = request.json.get('st')
    et = request.json.get('et')
    ust = request.json.get('ust')
    uet = request.json.get('uet')
    try:
        print(st)
        print(et)
        print(ust)
        print(uet)
        a = predict_range(ust, uet, st, et)
        # test = str(st)
        print('test')
        # print(type(test))

        return {
        'code': 0,
        'data': {
            'msg': '测试下看看',
            'answer': a
        }
            }
    # st, et = time_range("18")
    except Exception as e:
        return {
            'code': 4001,
            'data':{
                'msg': e
            }
        }

@app.route('/predict', methods=['POST'])
def LSTMpredict():
    # 获取客户端数据
    usn = request.json.get('usn')
    ust = request.json.get('ust')
    uet = request.json.get('uet')
    try:
        print(ust)
        print(uet)
        # 获取预测结果和原对应时间段的数据
        result,oridinal = predict(usn, ust, uet)
        # 将预测结果转为字典格式
        result_dict = result.reset_index(drop=True)
        result_dict = result_dict.to_dict(orient='list')
        rounded_values = [round(value, 2) for value in result_dict['YD15']]
        result_dict['YD15']=rounded_values
        # 日期格式变换，变为str
        for i in range(len(result_dict["DATATIME"])):
            result_dict["DATATIME"][i] = result_dict["DATATIME"][i].strftime('%Y-%m-%d %H:%M:%S')
        # 将原对应时间的数据转为list格式
        oridinal_list = oridinal.reset_index(drop=True)
        oridinal_list = oridinal_list.tolist()
        # 再多上传一份原数据的系统生成预测功率，用于双指标散点图
        sys_pre=var_uploader(usn,ust,uet,"PREPOWER")
        print(oridinal_list)
        print(len(oridinal_list))
        # print(result_dict["DATATIME"])
        print(len(result_dict["YD15"]))
        print(sys_pre)
        result_json = result.to_json(orient='records', date_format='iso')
        # print(result_dict)
        # print(result_json)
        print('收到一条模型预测请求')
        # print('ok')
        acc = calc_acc(y_true=oridinal_list,y_pred=result_dict["YD15"])
        print('ok')
        return {
            'code': 0,
            'data': result_dict,
            'original':oridinal_list,
            'sys_pre':sys_pre,
            'acc':acc
        }
    except Exception as e:
        return {
            'code': 4001,
            'data': {
                'msg': str(e)
            }
        }

@app.route('/getdata', methods=['POST'])
def getdata():
    # 获取客户端数据
    usn = request.json.get('usn')
    try:
        data = original(usn)
        print('收到一条数据获取请求')
        # 计算data字典的相关系数
        # data_corr = data.corr()
        # print(data)
        return {
            'code': 0,
            'data': data
            # 'data_corr': data_corr
        }
    except Exception as e:
        return {
            'code': 4001,
            'data': {
                'msg': str(e)
            }
        }

@app.route('/Upload', methods=['POST'])
def Upload():
    # 获取客户端上传的Form-data格式的csv文件
    # print(request.files)
    # print(request.files['file'])
    # print(request.files['file'].filename)
    # print(request.files['file'].content_type)
    # print(request.files['file'].stream)
    # print(request.files['file'].stream.read())
    try:
        #  将得到的csv文件保存到本地./data/user文件夹中
        request.files['file'].save('./data/user/'+request.files['file'].filename)
        # 读取csv文件
        # data = pd.read_csv('./data/user/'+request.files['file'].filename)
        # print(data)
        return {
        'code': 0,
        'data': {
            'msg': '上传成功'
        }
        }
    except Exception as e:
        return {
            'code': 4003,
            'data': {
                'msg': str(e)
            }
        }


@app.route('/TraditionalPred', methods=['POST'])
def TraditionalPred():
    # 获取客户端数据
    method = request.json.get('method')
    usn = request.json.get('usn')
    ust = request.json.get('ust')
    uet = request.json.get('uet')
    try:
        print(method)
        print(usn)
        print(ust)
        print(uet)
        # 根据所选择的方法，是用对应的方法进行预测
        if method == "AR":
            ar_p = request.json.get('ar_p')
            ar_p = eval(ar_p)
            # 获取预测结果和原对应时间段的数据
            # print('ok')
            result,original = Traditional_AR(usn, ust, uet,ar_p)
            result = pd.DataFrame({0:result})
        
        elif method == "MA":
            # print('ok')
            ma_q = request.json.get('ma_q')
            ma_q = eval(ma_q)
            # print(type(ma_q))
            # 获取预测结果和原对应时间段的数据
            result,original = Traditional_MA(usn, ust, uet,ma_q)
            result = pd.DataFrame({0:result})
            
        elif method == "ARMA":
            arma_p = request.json.get('arma_p')
            arma_q = request.json.get('arma_q')
            arma_p = eval(arma_p)
            arma_q = eval(arma_q)
            # 获取预测结果和原对应时间段的数据
            result,original = Traditional_ARMA(usn, ust, uet,arma_p,arma_q)
            result = pd.DataFrame({0:result})

        elif method == "ARIMA":
            arima_p = request.json.get('arima_p')
            arima_q = request.json.get('arima_q')
            arima_d = request.json.get('arima_d')
            arima_p = eval(arima_p)
            arima_q = eval(arima_q)
            arima_d = eval(arima_d)
            # 获取预测结果和原对应时间段的数据
            result,original = Traditional_ARIMA(usn, ust, uet,arima_p,arima_q,arima_d)
            result = pd.DataFrame({0:result})

        elif method == "SES":
            # 获取预测结果和原对应时间段的数据
            result,original = Traditional_SES(usn, ust, uet)

        elif method == "DES":
            # 获取预测结果和原对应时间段的数据
            result,original = Traditional_DES(usn, ust, uet)
        
        elif method == "TES":
            tes_seasonal_period = request.json.get('tes_seasonal_period')
            tes_seasonal_period = eval(tes_seasonal_period)
            # 获取预测结果和原对应时间段的数据
            result,original = Traditional_TES(usn, ust, uet,tes_seasonal_period)

        elif method == "SARIMA":
            sarima_order = request.json.get('sarima_order')
            sarima_seasonal_order = request.json.get('sarima_seasonal_order')
            sarima_order = eval(sarima_order)
            sarima_seasonal_order = eval(sarima_seasonal_order)
            # 获取预测结果和原对应时间段的数据
            result,original = Traditional_SARIMA(usn, ust, uet,sarima_order,sarima_seasonal_order)
            # print(result)
            # print(type(result))
            # print(result['predicted_mean'])
            # result.rename(index={'predicted_mean':'0'}, inplace = True)
            result = pd.DataFrame({0:result})

        elif method == "VAR":
            var_select_cols = request.json.get('var_select_cols')
            var_difference = request.json.get('var_difference')
            var_order = request.json.get('var_order')
            var_select_cols = eval(var_select_cols)
            var_difference = eval(var_difference)
            var_order = eval(var_order)
            # 获取预测结果和原对应时间段的数据
            result,original = Traditional_VAR(usn, ust, uet,var_select_cols,var_difference,var_order)

        elif method == "GARCH":
            garch_p=request.json.get("garch_p")
            garch_q=request.json.get("garch_p")
            garch_p=eval(garch_p)
            garch_q=eval(garch_q)
            result,original=Traditional_GARCH(usn,ust,uet,garch_p,garch_q)


        # 将预测结果转为字典格式
        result_dict = result.reset_index()
        # print(result_dict)
        result_dict = result_dict.rename(columns={'index':'DATATIME',0:'YD15'})
        print(result_dict)
        result_dict = result_dict.to_dict(orient='list')
        rounded_values = [round(value, 2) for value in result_dict['YD15']]
        result_dict['YD15']=rounded_values
        # 日期格式变换，变为str
        for i in range(len(result_dict["DATATIME"])):
            result_dict["DATATIME"][i] = result_dict["DATATIME"][i].strftime('%Y-%m-%d %H:%M:%S')
        # 将原对应时间的数据转为list格式
        oridinal_list = original.reset_index(drop=True)
        oridinal_list = oridinal_list.tolist()
        # 再多上传一份原数据的系统生成预测功率，用于双指标散点图
        # sys_pre=var_uploader(usn,ust,uet,"PREPOWER")
        # print(oridinal_list)
        # print(type(oridinal_list))
        # print(type(result_dict))
        print(oridinal_list)
        print(len(oridinal_list))
        print(result_dict["YD15"])
        # print(result_dict)
        print(len(result_dict["YD15"]))
        result_json = result.to_json(orient='records', date_format='iso')
        # print(result_dict)
        # print(result_json)
        print('收到一条模型预测请求')
        # print('ok')
        if len(result_dict["YD15"])==len(oridinal_list):
            acc=calc_acc(y_true=oridinal_list,y_pred=result_dict["YD15"])
        if len(result_dict["YD15"])!=len(oridinal_list):
            acc=calc_acc(y_true=oridinal_list[97:],y_pred=result_dict["YD15"])
        return {
            'code': 0,
            'data': result_dict,
            'original':oridinal_list,
            'acc':acc
            # 'sys_pre':sys_pre
        }
    except Exception as e:
        return {
            'code': 4001,
            'data': {
                'msg': str(e)
            }
        }

@app.route('/AdfAcfPacfTest', methods=['POST'])
def AdfAcfPacfTest():
    # 获取客户端数据
    method = request.json.get('method')
    usn = request.json.get('usn')
    ust = request.json.get('ust')
    uet = request.json.get('uet')
    try:
        print(method)
        print(usn)
        print(ust)
        print(uet)
        # 根据所选择的方法，是用对应的方法进行预测
        if method == "ADF":
            result = diff(usn, ust, uet)
            return {
            'code': 0,
            'data': result,
            'msg': 'ADF检验完成'
        }
        if method == "ACFPACF":
           acfpacf_d = request.json.get('acfpacf_d')
           acfpacf_d = eval(acfpacf_d)
           autocorrelation(usn, ust, uet,acfpacf_d)
           return {
            'code': 0,
            'data': '请求发送成功',
        }
        
        print('收到一条测试请求')
        
    except Exception as e:
        return {
            'code': 4001,
            'data': {
                'msg': str(e)
            }
        }



@app.route('/ensemble', methods=['POST'])
def ENSEMBLEpredict():
    # 获取客户端数据
    usn = request.json.get('usn')
    ust = request.json.get('ust')
    uet = request.json.get('uet')
    '''
    参数格式参考：
    weight=[1,1,0,8,0,0,0,5,666,0,0]
    参数是一个嵌套的列表
    parameter=[[],[7],[1],[6,1],[6,1,1],  # 这行是五个模型的参数
               [],[],[24*4],[0,1,0,0,1,1,12], #这行是四个模型的参数
               [['WINDSPEED','PREPOWER','WINDDIRECTION','TEMPERATURE','HUMIDITY','PRESSURE','YD15'],1,3], #这行是1个模型的参数
               [5，5]]  #这个最后那个模型的参数
    '''
    weight = request.json.get("weights")
    parameter=request.json.get("parameters")
    for i in range(len(weight)): weight[i]=eval(weight[i])
    for list in parameter :
        for p in range(len(list)) :
            list[p]=eval(list[p])
    print(usn)
    print(ust)
    print(uet)
    print(weight)
    print(parameter)
    # weight = eval(weight)
    # parameter=eval(parameter)

    try:
        print(ust)
        print(uet)
        # 获取预测结果和原对应时间段的数据
        result,oridinal = Model_Ensemble(usn, ust, uet,weight=weight,parameter=parameter)
        # 将预测结果转为字典格式
        result_dict = result.reset_index(drop=True)
        result_dict = result_dict.to_dict(orient='list')
        rounded_values = [round(value, 2) for value in result_dict['YD15']]
        result_dict['YD15']=rounded_values
        # 日期格式变换，变为str
        for i in range(len(result_dict["DATATIME"])):
            result_dict["DATATIME"][i] = result_dict["DATATIME"][i].strftime('%Y-%m-%d %H:%M:%S')
        # 将原对应时间的数据转为list格式
        oridinal_list = oridinal.reset_index(drop=True)
        oridinal_list = oridinal_list.tolist()
        # 再多上传一份原数据的系统生成预测功率，用于双指标散点图
        sys_pre=var_uploader(usn,ust,uet,"PREPOWER")
        acc=calc_acc1(y_true=oridinal_list,y_pred=result["YD15"])
        print(oridinal_list)
        print(result_dict["DATATIME"])
        print(result_dict["YD15"])
        print(sys_pre)
        result_json = result.to_json(orient='records', date_format='iso')
        # print(result_dict)
        # print(result_json)
        print('收到一条模型预测请求')
        return {
            'code': 0,
            'data': result_dict,
            'original':oridinal_list,
            'sys_pre':sys_pre,
            'acc':acc
        }
    except Exception as e:
        return {
            'code': 4001,
            'data': {
                'msg': str(e)
            }
        }


@app.route('/GetUserModel', methods=['POST'])
def GetUserModel():
    # 获取客户端上传的Form-data格式的csv文件
    print('get user model success')
    # print(request.files['file'])
    # print(request.files['file'].filename)
    # print(request.files['file'].content_type)
    # print(request.files['file'].stream)
    # print(request.files['file'].stream.read())
    try:
        #  将得到的csv文件保存到本地./data/user文件夹中
        request.files['file'].save('./'+request.files['file'].filename)
        # 读取csv文件
        # data = pd.read_csv('./data/user/'+request.files['file'].filename)
        print('get user model success')
        return {
        'code': 0,
        'data': {
            'msg': '上传成功'
        }
        }
    except Exception as e:
        return {
            'code': 4003,
            'data': {
                'msg': str(e)
            }
        }


@app.route('/USERMODELPRED', methods=['POST'])
def USERMODELPRED():
    # 获取客户端数据
    method = request.json.get('method')
    usn = request.json.get('usn')
    ust = request.json.get('ust')
    uet = request.json.get('uet')
    UserModelparam = request.json.get('UserModelparam')
    UserModelparam = eval(UserModelparam)
    try:
        print(method)
        print(usn)
        print(ust)
        print(uet)
        # 根据所选择的方法，是用对应的方法进行预测
        # if method == "1":
        #     from usermodel.usermodel1 import Usermodel1
        #     result,original = Usermodel1(usn, ust, uet,UserModelparam)


        # if method == "2":
        #     from usermodel.usermodel2 import Usermodel2
        #     result,original = Usermodel2(usn, ust, uet,UserModelparam)

        # if method == "3":
        #     from usermodel.usermodel3 import Usermodel3
        #     result,original = Usermodel3(usn, ust, uet,UserModelparam)

        # if method == "4":
        #     from usermodel.usermodel4 import Usermodel4
        #     result,original = Usermodel4(usn, ust, uet,UserModelparam)
        
        # if method == "5":
        #     from usermodel.usermodel5 import Usermodel5
        #     result,original = Usermodel5(usn, ust, uet,UserModelparam)
        
        # if method == "6":
        #     from usermodel.usermodel6 import Usermodel6
        #     result,original = Usermodel6(usn, ust, uet,UserModelparam)
        
        # if method == "7":
        #     from usermodel.usermodel7 import Usermodel7
        #     result,original = Usermodel7(usn, ust, uet,UserModelparam)

        # if method == "8":
        #     from usermodel.usermodel8 import Usermodel8
        #     result,original = Usermodel8(usn, ust, uet,UserModelparam)
        
        # if method == "9":
        #     from usermodel.usermodel9 import Usermodel9
        #     result,original = Usermodel9(usn, ust, uet,UserModelparam)
        
        # if method == "10":
        #     from usermodel.usermodel10 import Usermodel10
        #     result,original = Usermodel10(usn, ust, uet,UserModelparam)

        if method == "1":
            from usermodel1 import usermodel1
            result,original = usermodel1(usn, ust, uet,UserModelparam)


        if method == "2":
            from usermodel2 import usermodel2
            result,original = usermodel2(usn, ust, uet,UserModelparam)

        if method == "3":
            from usermodel3 import usermodel3
            result,original = usermodel3(usn, ust, uet,UserModelparam)

        if method == "4":
            from usermodel4 import usermodel4
            result,original = usermodel4(usn, ust, uet,UserModelparam)
        
        if method == "5":
            from usermodel5 import usermodel5
            result,original = usermodel5(usn, ust, uet,UserModelparam)
        
        if method == "6":
            from usermodel6 import usermodel6
            result,original = usermodel6(usn, ust, uet,UserModelparam)
        
        if method == "7":
            from usermodel7 import usermodel7
            result,original = usermodel7(usn, ust, uet,UserModelparam)

        if method == "8":
            from usermodel8 import usermodel8
            result,original = usermodel8(usn, ust, uet,UserModelparam)
        
        if method == "9":
            from usermodel9 import usermodel9
            result,original = usermodel9(usn, ust, uet,UserModelparam)
        
        if method == "10":
            from usermodel10 import usermodel10
            result,original = usermodel10(usn, ust, uet,UserModelparam)

            

        # 将预测结果转为字典格式
        result_dict = result.reset_index()
        print(result_dict)
        result_dict = result_dict.rename(columns={'index':'DATATIME',0:'YD15'})
        print(result_dict)
        result_dict = result_dict.to_dict(orient='list')
        rounded_values = [round(value, 2) for value in result_dict['YD15']]
        result_dict['YD15']=rounded_values
        # 日期格式变换，变为str
        for i in range(len(result_dict["DATATIME"])):
            result_dict["DATATIME"][i] = result_dict["DATATIME"][i].strftime('%Y-%m-%d %H:%M:%S')
        # 将原对应时间的数据转为list格式
        oridinal_list = original.reset_index(drop=True)
        oridinal_list = oridinal_list.tolist()
        # 再多上传一份原数据的系统生成预测功率，用于双指标散点图
        # sys_pre=var_uploader(usn,ust,uet,"PREPOWER")
        print(oridinal_list)
        print(result_dict["DATATIME"])
        print(result_dict["YD15"])
        # print(sys_pre)
        result_json = result.to_json(orient='records', date_format='iso')
        # print(result_dict)
        # print(result_json)
        print('收到一条模型预测请求')
        acc=calc_acc(y_true=oridinal_list[97:],y_pred=result_dict["YD15"])
        return {
            'code': 0,
            'data': result_dict,
            'original':oridinal_list,
            'acc':acc
        }
    except Exception as e:
        return {
            'code': 4001,
            'data': {
                'msg': str(e)
            }
        }


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    app.run(host='0.0.0.0', port=5000,debug=True)






# KEY是用户名，value是token
# username_tokens = {}

# 数据库
# mysql+pymysql://用户名:密码@IP地址:端口号/数据库
# db_uri = 'mysql+pymysql://{}:{}@{}:{}/{}'.format('root', 'H20220901', '127.0.0.1', 3306, 'test')
# app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# # 创建数据库实例
# db = SQLAlchemy(app)
# 用来访问数据库
# engine = db.get_engine()


# 定义数据模型
# class AlarmEvent(db.Model):
#     __tablename__ = 'alarm_event'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     image = db.Column(LONGTEXT)
#     creat_time = db.Column(db.DateTime, server_default = db.text('CURRENT_TIMESTAMP'))
#     result = db.Column(db.Text)


# # 关联表信息
# db.create_all()

# '''
# FB/DB
# 登录接口
# '''
# # 登录接口
# @app.route('/login', methods=['POST', 'GET'])
# def login():
    
#     '''
#     DB
#     TODO 后期将username,与password的参数传到数据库进行对比
#     '''
#     # 获取客户端发送的用户名、密码参数
#     username = request.json.get('username')
#     password = request.json.get('password')
#     # print(type(username))
#     # print(password)
#     # ../DataBase/main.py 中数据库封装的函数
#     # x =DB.Judge('1','username', 'passwd','img')
#     # print(x)
#     # print(username)
#     # TODO 正确做法：去数据库中查询用户名、密码是否正确
#     x =DB.Judge(username,'username', 'passwd','img')
#     # print(x)
#     if x['code'] == 4002:
#         return x
#     else:
#         if x['msg'][0] == password:
#             return x
#         else:
#             return {
#             'code': 4001,
#             'msg': '密码错误'
#             }
#     # print('connect ok')

#     # 使用uuid作为token
#     # token = str(uuid.uuid1())
#     # username_tokens[username] = token
#     # print(token)
#     return {
#         'code': 0,
#         'msg': '登录成功',
#         'data': {
#             # 'token': token,
#             'nickname': 'ZXH',
#             'avatar': 'https://upload-bbs.mihoyo.com/upload/2021/02/24/73281682/9a634560776c9855d47bac0919332b4e_992042028649790081.jpg'
#         }
#     }


# '''
# FB/DB
# TODO 注册

# '''

# @app.route('/signup', methods=['POST'])
# def signup():
#     #首先获取用户注册时的用户名和密码，调用数据库中的Register_judge函数判断是否已经注册
#     #若已被注册，返回'code': 0，'msg': '用户名已存在'；
#     #若未被注册，判断密码和确认密码输入是否相同，若不相同，返回'code': 4004, 'msg': '确认密码错误'；
#     #若相同，调用数据库中的InserttDB函数，将用户输入的用户名，密码，密保信息存储到数据库中
#     username = request.json.get('username')
#     password = request.json.get('password')
#     mibao_question = request.json.get('mibao_question')
#     mibao_answer = request.json.get('mibao_answer')
#     img = ''

#     judge_username_exist = DB.Register_judge(username, 'username')
#     if judge_username_exist['code'] == 0:
#         return {
#             'code': 4003,
#             'msg': '用户名已存在'
#         }
#     else:
#         DB.InserttDB(username, password, img, mibao_question, mibao_answer)
#         return {
#             'code': 0,
#             'msg': '注册成功'
#         }


# '''
# FB\DB
# TODO 忘记密码
# '''
# @app.route('/pwdforget', methods=['POST'])
# def pwdforget():
#     #首先查询输入的用户名是否存在,调用数据库中的Register_judge函数
#     username = request.json.get('username_secret')
#     mibao_answer = request.json.get('mibao_answer')
#     # print(username)
#     secret_information = DB.Get_security_information(username, 'username', 'mibaoQ', 'mibaoA', 'passwd')
#     mibaoQ = secret_information['msg'][0]
#     mibaoA = secret_information['msg'][1]
#     passwd = secret_information['msg'][2]
#     print(secret_information)
#     if not mibao_answer:
#             if secret_information['code'] == 4002:
#                 return secret_information
#             if secret_information['code'] == 0:
#                 return {
#                     'code': 0,
#                     'msg': {
#                         'mibao_question': mibaoQ
#                     }
#                 }
#         #用户名存在，进而查询用户的密保问题，密保信息，以及密码
#         #将密保问题作为'msg'返回到前端，获取用户输入的密保答案，进行比较，若一致，返回密码；
#         #若不一致，返回'code': 4005, 'msg': '答案错误'
#     if mibao_answer:
#         if secret_information['code'] == 0:
#             if mibao_answer == mibaoA:
#                 return {
#                     'code': 0,
#                     'msg': passwd
#                 }
#             if mibao_answer != mibaoA:
#                 return {
#                     'code': 4005,
#                     'msg': '答案错误'
#                 }

        

'''
FB
TODO 调用算法
'''
# @app.route('/algo', methods=['POST'])
# def test():
#     # 获取客户端数据
#     message = request.json.get('message_info')
#     print(message)
    
#     return {
#         'code': 0,
#         'msg': 'okok'
#             }

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

