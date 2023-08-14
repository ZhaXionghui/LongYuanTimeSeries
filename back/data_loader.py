import paddle
import pickle
from sklearn.preprocessing import StandardScaler
import datetime

def to_unix_time(dt):
    # timestamp to unix
    epoch = datetime.datetime.utcfromtimestamp(0)
    return int((dt - epoch).total_seconds())

class TSDataset(paddle.io.Dataset):
    """时序DataSet
    划分数据集、适配dataloader所需的dataset格式
    ref: https://github.com/thuml/Autoformer/blob/main/data_provider/data_loader.py
    """
    def __init__(self, data, 
                 ts_col='DATATIME',
                 use_cols =['WINDSPEED', 'PREPOWER', 'WINDDIRECTION', 'TEMPERATURE', 'HUMIDITY', 
                 'PRESSURE', 'ROUND(A.WS,1)', 'ROUND(A.POWER,0)', 'YD15',
                 'month', 'day', 'weekday', 'hour', 'minute'],
                 labels = ['ROUND(A.POWER,0)', 'YD15'], 
                 input_len = 24*4*5, pred_len = 24*4, stride=19*4, data_type='train',
                 train_ratio = 0.7, val_ratio = 0.15):
        super(TSDataset, self).__init__()
        self.ts_col = ts_col        # 时间戳列
        self.use_cols = use_cols    # 训练时使用的特征列
        self.labels = labels        # 待预测的标签列
        self.input_len = input_len  # 模型输入数据的样本点长度，15分钟间隔，一个小时14个点，近5天的数据就是24*4*5
        self.pred_len = pred_len    # 预测长度，预测次日00:00至23:45实际功率，即1天：24*4
        self.data_type = data_type  # 需要加载的数据类型
        self.scale = True           # 是否需要标准化
        self.train_ratio = train_ratio # 训练集划分比例
        self.val_ratio = val_ratio  # 验证集划分比例
        # 由于赛题要求利用当日05:00之前的数据，预测次日00:00至23:45实际功率
        # 所以x和label要间隔19*4个点
        self.stride = stride
        assert data_type in ['train', 'val', 'test']    # 确保data_type输入符合要求
        type_map = {'train': 0, 'val': 1, 'test': 2}
        self.set_type = type_map[self.data_type]
          
        self.transform(data)

    def transform(self, df):
        # 获取unix时间戳、输入特征和预测标签
        time_stamps, x_values, y_values = df[self.ts_col].apply(lambda x:to_unix_time(x)).values, df[self.use_cols].values, df[self.labels].values
        # 划分数据集
        # 这里可以按需设置划分比例
        num_train = int(len(df) * self.train_ratio)
        num_vali = int(len(df) * self.val_ratio)
        num_test = len(df) - num_train - num_vali
        border1s = [0, num_train-self.input_len-self.stride, len(df)-num_test-self.input_len-self.stride]
        border2s = [num_train, num_train + num_vali, len(df)]
        # 获取data_type下的左右数据截取边界
        border1 = border1s[self.set_type]
        border2 = border2s[self.set_type]    

        # 标准化
        self.scaler = StandardScaler()
        if self.scale:
            # 使用训练集得到scaler对象
            train_data = x_values[border1s[0]:border2s[0]]
            self.scaler.fit(train_data)
            data = self.scaler.transform(x_values)
            # 保存scaler
            pickle.dump(self.scaler, open('model/scaler.pkl', 'wb'))
        else:
            data = x_values

        # array to paddle tensor
        self.time_stamps = paddle.to_tensor(time_stamps[border1:border2], dtype='int64')
        self.data_x = paddle.to_tensor(data[border1:border2], dtype='float32')
        self.data_y = paddle.to_tensor(y_values[border1:border2], dtype='float32')  

    def __getitem__(self, index):
        """
        实现__getitem__方法，定义指定index时如何获取数据，并返回单条数据（训练数据）
        """
        # 由于赛题要求利用当日05:00之前的数据，预测次日00:00至23:45实际功率
        # 所以x和label要间隔19*4个点
        s_begin = index
        s_end = s_begin + self.input_len
        r_begin = s_end + self.stride
        r_end = r_begin + self.pred_len

        # TODO 可以增加对未来可见数据的获取
        seq_x = self.data_x[s_begin:s_end]
        seq_y = self.data_y[r_begin:r_end]
        ts_x = self.time_stamps[s_begin:s_end]
        ts_y = self.time_stamps[r_begin:r_end]
        return seq_x, seq_y, ts_x, ts_y

    def __len__(self):
        """
        实现__len__方法，返回数据集总数目
        """
        return len(self.data_x) - self.input_len - self.stride - self.pred_len  + 1


class TSPredDataset(paddle.io.Dataset):
    """时序Pred DataSet
    划分数据集、适配dataloader所需的dataset格式
    ref: https://github.com/thuml/Autoformer/blob/main/data_provider/data_loader.py
    """
    def __init__(self, data, 
                 ts_col='DATATIME',
                 use_cols =['WINDSPEED', 'PREPOWER', 'WINDDIRECTION', 'TEMPERATURE', 'HUMIDITY', 
                 'PRESSURE', 'ROUND(A.WS,1)', 'ROUND(A.POWER,0)', 'YD15',
                 'month', 'day', 'weekday', 'hour', 'minute'],
                 labels = ['ROUND(A.POWER,0)', 'YD15'],  
                 input_len = 24*4*5, pred_len = 24*4, stride=19*4):
        super(TSPredDataset, self).__init__()
        self.ts_col = ts_col        # 时间戳列
        self.use_cols = use_cols    # 训练时使用的特征列
        self.labels = labels        # 待预测的标签列
        self.input_len = input_len  # 模型输入数据的样本点长度，15分钟间隔，一个小时14个点，近5天的数据就是24*4*5
        self.pred_len = pred_len    # 预测长度，预测次日00:00至23:45实际功率，即1天：24*4
        # 由于赛题要求利用当日05:00之前的数据，预测次日00:00至23:45实际功率
        # 所以x和label要间隔19*4个点
        self.stride = stride        
        self.scale = True           # 是否需要标准化
       
        self.transform(data)

    def transform(self, df):
        # 获取unix时间戳、输入特征和预测标签
        time_stamps, x_values, y_values = df[self.ts_col].apply(lambda x:to_unix_time(x)).values, df[self.use_cols].values, df[self.labels].values
        # 截取边界
        border1 = len(df) - self.input_len - self.stride - self.pred_len
        border2 = len(df)   

        # 标准化
        self.scaler = StandardScaler()
        if self.scale:
            # 读取预训练好的scaler
            self.scaler = pickle.load(open('model/scaler.pkl', 'rb'))
            data = self.scaler.transform(x_values)
        else:
            data = x_values

        # array to paddle tensor
        self.time_stamps = paddle.to_tensor(time_stamps[border1:border2], dtype='int64')
        self.data_x = paddle.to_tensor(data[border1:border2], dtype='float32')
        self.data_y = paddle.to_tensor(y_values[border1:border2], dtype='float32')  

    def __getitem__(self, index):
        """
        实现__getitem__方法，定义指定index时如何获取数据，并返回单条数据（训练数据）
        """
        # 由于赛题要求利用当日05:00之前的数据，预测次日00:00至23:45实际功率
        # 所以x和label要间隔19*4个点
        s_begin = index
        s_end = s_begin + self.input_len
        r_begin = s_end + self.stride
        r_end = r_begin + self.pred_len

        # TODO 可以增加对未来可见数据的获取
        seq_x = self.data_x[s_begin:s_end]
        seq_y = self.data_y[r_begin:r_end]
        ts_x = self.time_stamps[s_begin:s_end]
        ts_y = self.time_stamps[r_begin:r_end]
        return seq_x, seq_y, ts_x, ts_y

    def __len__(self):
        """
        实现__len__方法，返回数据集总数目
        """
        return len(self.data_x) - self.input_len - self.stride - self.pred_len  + 1