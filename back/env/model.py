import paddle


class MultiTaskLSTM(paddle.nn.Layer):
    """多任务LSTM时序预测模型
    LSTM为共享层网络，对两个预测目标分别有两个分支独立线性层网络

    TODO 其实该模型就是个Encoder，如果后续要引入天气预测未来的变量，补充个Decoder，
    然后Encoder负责历史变量的编码，Decoder负责将 编码后的历史编码结果 和 它编码未来变量的编码结果 合并后，做解码预测即可
    """

    def __init__(self, feat_num=14, hidden_size=64, num_layers=2, dropout_rate=0.7, input_len=120 * 4, pred_len=24 * 4):
        super(MultiTaskLSTM, self).__init__()
        # 增加1D卷积提取局部特征
        self.conv = paddle.nn.Conv1D(feat_num, hidden_size, 5, stride=1, padding=2, dilation=1, groups=1,
                                     padding_mode='zeros', weight_attr=None, bias_attr=None, data_format='NLC')
        self.act = paddle.nn.ReLU()
        self.norm = paddle.nn.BatchNorm1D(hidden_size, data_format='NLC')
        # LSTM为共享层网络
        self.lstm_layer = paddle.nn.LSTM(hidden_size, hidden_size,
                                         num_layers=num_layers,
                                         direction='forward',
                                         dropout=dropout_rate)
        # 为'ROUND(A.POWER,0)'构建分支网络
        #         self.linear1_1 = paddle.nn.Linear(in_features=input_len*hidden_size, out_features=hidden_size*2)
        #         self.act1 = paddle.nn.ReLU()
        #         self.norm1 = paddle.nn.BatchNorm1D(hidden_size*2, data_format='NLC')
        #         self.linear1_2 = paddle.nn.Linear(in_features=hidden_size*2, out_features=pred_len)
        # 为'YD15'构建分支网络
        self.linear2_1 = paddle.nn.Linear(in_features=input_len * hidden_size, out_features=hidden_size * 2)
        #         self.act2 = paddle.nn.ReLU()
        #         self.norm2 = paddle.nn.BatchNorm1D(hidden_size*2, data_format='NLC')
        self.linear2_2 = paddle.nn.Linear(in_features=hidden_size * 2, out_features=pred_len)
        self.dropout = paddle.nn.Dropout(dropout_rate)

    def forward(self, x):
        # x形状大小为[batch_size, input_len, feature_size]
        # output形状大小为[batch_size, input_len, hidden_size]
        # hidden形状大小为[num_layers, batch_size, hidden_size]
        x = self.conv(x)
        x = self.act(self.norm(x))
        output, (hidden, cell) = self.lstm_layer(x)
        # output: [batch_size, input_len, hidden_size] -> [batch_size, input_len*pred_len]
        output = paddle.reshape(output, [len(output), -1])

        #         output1 = self.linear1_1(output)
        #         output1 = self.dropout(self.act1(self.norm1(output1)))
        #         output1 = self.linear1_2(output1)
        # output1 = self.dropout(output1)
        # output1 = self.linear1_3(output1)

        output2 = self.linear2_1(output)
        output2 = self.dropout(output2)
        #         output2 = self.dropout(self.act2(self.norm2(output2)))
        output2 = self.linear2_2(output2)
        # output2 = self.dropout(output2)
        # output2 = self.linear2_3(output2)

        # outputs: ([batch_size, pre_len, 1], [batch_size, pre_len, 1])
        return output2


