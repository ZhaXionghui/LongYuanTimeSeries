<script setup>
import ProductService from '@/service/ProductService';
import PhotoService from '@/service/PhotoService';
import { useLayout } from '@/layout/composables/layout';
import NodeService from '@/service/NodeService';
import { onMounted, onUnmounted, ref, watch}  from 'vue';
import * as echarts from 'echarts'
import {
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  MarkLineComponent,
  MarkPointComponent
} from 'echarts/components';
import { LineChart } from 'echarts/charts';
import { UniversalTransition } from 'echarts/features';
import { CanvasRenderer } from 'echarts/renderers';
import swal from "sweetalert";
import axios from "axios";


const { layoutConfig } = useLayout();
let documentStyle = getComputedStyle(document.documentElement);
let textColor = documentStyle.getPropertyValue('--text-color');
let textColorSecondary = documentStyle.getPropertyValue('--text-color-secondary');
let surfaceBorder = documentStyle.getPropertyValue('--surface-border');

const { isDarkTheme } = useLayout();
const products = ref([]);
const images = ref([]);
const lineOptions = ref(null);
const productService = new ProductService();
const photoService = new PhotoService();
const treeTableValue = ref(null);
const model1Value = ref(null);
const selectedTreeTableValue = ref(null);
const nodeService = new NodeService();
const lineData = ref(null);
const pieData = ref(null);
const polarData = ref(null);
const barData = ref(null);
const radarData = ref(null);

const pieOptions = ref(null);
const polarOptions = ref(null);
const barOptions = ref(null);
const radarOptions = ref(null);

const chart1 = ref();
const chart2 = ref();
const setColorOptions = () => {
  documentStyle = getComputedStyle(document.documentElement);
  textColor = documentStyle.getPropertyValue('--text-color');
  textColorSecondary = documentStyle.getPropertyValue('--text-color-secondary');
  surfaceBorder = documentStyle.getPropertyValue('--surface-border');
};
const setChart = () => {
  barData.value = {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
    datasets: [
      {
        label: 'My First dataset',
        backgroundColor: documentStyle.getPropertyValue('--primary-500'),
        borderColor: documentStyle.getPropertyValue('--primary-500'),
        data: [65, 59, 80, 81, 56, 55, 40]
      },
      {
        label: 'My Second dataset',
        backgroundColor: documentStyle.getPropertyValue('--primary-200'),
        borderColor: documentStyle.getPropertyValue('--primary-200'),
        data: [28, 48, 40, 19, 86, 27, 90]
      }
    ]
  };
  barOptions.value = {
    plugins: {
      legend: {
        labels: {
          fontColor: textColor
        }
      }
    },
    scales: {
      x: {
        ticks: {
          color: textColorSecondary,
          font: {
            weight: 500
          }
        },
        grid: {
          display: false,
          drawBorder: false
        }
      },
      y: {
        ticks: {
          color: textColorSecondary
        },
        grid: {
          color: surfaceBorder,
          drawBorder: false
        }
      }
    }
  };

  pieData.value = {
    labels: ['A', 'B', 'C'],
    datasets: [
      {
        data: [540, 325, 702],
        backgroundColor: [documentStyle.getPropertyValue('--indigo-500'), documentStyle.getPropertyValue('--purple-500'), documentStyle.getPropertyValue('--teal-500')],
        hoverBackgroundColor: [documentStyle.getPropertyValue('--indigo-400'), documentStyle.getPropertyValue('--purple-400'), documentStyle.getPropertyValue('--teal-400')]
      }
    ]
  };

  pieOptions.value = {
    plugins: {
      legend: {
        labels: {
          usePointStyle: true,
          color: textColor
        }
      }
    }
  };

  lineData.value = {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
    datasets: [
      {
        label: 'First Dataset',
        data: [65, 59, 80, 81, 56, 55, 40],
        fill: false,
        backgroundColor: documentStyle.getPropertyValue('--primary-500'),
        borderColor: documentStyle.getPropertyValue('--primary-500'),
        tension: 0.4
      },
      {
        label: 'Second Dataset',
        data: [28, 48, 40, 19, 86, 27, 90],
        fill: false,
        backgroundColor: documentStyle.getPropertyValue('--primary-200'),
        borderColor: documentStyle.getPropertyValue('--primary-200'),
        tension: 0.4
      }
    ]
  };

  lineOptions.value = {
    plugins: {
      legend: {
        labels: {
          fontColor: textColor
        }
      }
    },
    scales: {
      x: {
        ticks: {
          color: textColorSecondary
        },
        grid: {
          color: surfaceBorder,
          drawBorder: false
        }
      },
      y: {
        ticks: {
          color: textColorSecondary
        },
        grid: {
          color: surfaceBorder,
          drawBorder: false
        }
      }
    }
  };

  polarData.value = {
    datasets: [
      {
        data: [10, 16, 7, 3],
        backgroundColor: [documentStyle.getPropertyValue('--indigo-500'), documentStyle.getPropertyValue('--purple-500'), documentStyle.getPropertyValue('--teal-500'), documentStyle.getPropertyValue('--orange-500')],
        label: 'My dataset'
      }
    ],
    labels: ['Indigo', 'Purple', 'Teal', 'Orange']
  };

  polarOptions.value = {
    plugins: {
      legend: {
        labels: {
          color: textColor
        }
      }
    },
    scales: {
      r: {
        grid: {
          color: surfaceBorder
        }
      }
    }
  };

  radarData.value = {
    labels: ['Eating', 'Drinking', 'Sleeping', 'Designing', 'Coding', 'Cycling', 'Running'],
    datasets: [
      {
        label: 'My First dataset',
        borderColor: documentStyle.getPropertyValue('--indigo-400'),
        pointBackgroundColor: documentStyle.getPropertyValue('--indigo-400'),
        pointBorderColor: documentStyle.getPropertyValue('--indigo-400'),
        pointHoverBackgroundColor: textColor,
        pointHoverBorderColor: documentStyle.getPropertyValue('--indigo-400'),
        data: [65, 59, 90, 81, 56, 55, 40]
      },
      {
        label: 'My Second dataset',
        borderColor: documentStyle.getPropertyValue('--purple-400'),
        pointBackgroundColor: documentStyle.getPropertyValue('--purple-400'),
        pointBorderColor: documentStyle.getPropertyValue('--purple-400'),
        pointHoverBackgroundColor: textColor,
        pointHoverBorderColor: documentStyle.getPropertyValue('--purple-400'),
        data: [28, 48, 40, 19, 96, 27, 100]
      }
    ]
  };

  radarOptions.value = {
    plugins: {
      legend: {
        labels: {
          fontColor: textColor
        }
      }
    },
    scales: {
      r: {
        grid: {
          color: textColorSecondary
        }
      }
    }
  };
};

const applyLightTheme = () => {
  lineOptions.value = {
    plugins: {
      legend: {
        labels: {
          color: '#495057'
        }
      }
    },
    scales: {
      x: {
        ticks: {
          color: '#495057'
        },
        grid: {
          color: '#ebedef'
        }
      },
      y: {
        ticks: {
          color: '#495057'
        },
        grid: {
          color: '#ebedef'
        }
      }
    }
  };
};
const applyDarkTheme = () => {
  lineOptions.value = {
    plugins: {
      legend: {
        labels: {
          color: '#ebedef'
        }
      }
    },
    scales: {
      x: {
        ticks: {
          color: '#ebedef'
        },
        grid: {
          color: 'rgba(160, 167, 181, .3)'
        }
      },
      y: {
        ticks: {
          color: '#ebedef'
        },
        grid: {
          color: 'rgba(160, 167, 181, .3)'
        }
      }
    }
  };
};

echarts.use([
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  MarkLineComponent,
  MarkPointComponent,
  LineChart,
  CanvasRenderer,
  UniversalTransition
]);

onMounted(() => {
  productService.getProductsSmall().then((data) => (products.value = data));
  photoService.getImages().then((data) => (images.value = data));
  nodeService.getTreeTableNodes().then((data) => (treeTableValue.value = data));
  nodeService.getModel1Nodes().then((data) => (model1Value.value = data));
});

// const r1 = localStorage.getItem('result')
var read=function(name){
  return  JSON.parse(localStorage.getItem(name))//把本地存储的my转成数组
}
onMounted(()=>{
  var myChart = echarts.init(chart1.value);
  var option = {
    title: {
      text: '实际功率预测结果'
    },
    tooltip: {
      trigger: 'axis'
    },
    legend: {},
    toolbox: {
      show: true,
      feature: {
        dataZoom: {
          yAxisIndex: 'none'
        },
        dataView: { readOnly: false },
        magicType: { type: ['line', 'bar'] },
        restore: {},
        saveAsImage: {}
      }
    },
    xAxis: {
      type: 'category',
      name: 'Time',
      boundaryGap: false,
      data: read("datatime")
    },
    yAxis: {
      type: 'value',
      name: 'Power',
      axisLabel: {
        formatter: '{value} KW'
      }
    },
    dataZoom: [
      {
        type: 'inside'
      },
      {
        type: 'slider',
        height: 10
      }
    ],
    series: [
      {
        name: 'Original',
        type: 'line',
        //   data: localStorage.getItem("pYD15"),
        data: read("oYD15"),
        markPoint: {
          data: [
            { type: 'max', name: 'Max' },
            { type: 'min', name: 'Min' }
          ]
        },
        markLine: {
          data: [{ type: 'average', name: 'Avg' }]
        }
      },
      {
        name: 'Predicted',
        type: 'line',
        //   data: localStorage.getItem("pYD15"),
        data: read("pYD15"),
        markPoint: {
          data: [
            { type: 'max', name: 'Max' },
            { type: 'min', name: 'Min' }
          ]
        },
        markLine: {
          data: [{ type: 'average', name: 'Avg' }]
        }
      }
    ]
  };

  option && myChart.setOption(option);
})


onMounted(()=>{
  var myChart = echarts.init(chart2.value);
  var option = {
    title: {
      text: '残差图'
    },
    tooltip: {
      trigger: 'axis'
    },
    legend: {},
    toolbox: {
      show: true,
      feature: {
        dataZoom: {
          yAxisIndex: 'none'
        },
        dataView: { readOnly: false },
        magicType: { type: ['line', 'bar'] },
        restore: {},
        saveAsImage: {}
      }
    },
    xAxis: {
      type: 'category',
      name: ' 时间 ',
      boundaryGap: false,
      data: read("datatime")
    },
    yAxis: {
      type: 'value',
      name:' 残差值 ',
      axisLabel: {
        formatter: '{value} KW'
      }
    },
    dataZoom: [
      {
        type: 'inside'
      },
      {
        type: 'slider',
        height: 10
      }
    ],

    series: [
      {
        name: '残差',
        type: 'line',
        data: read("abs"),
        markPoint: {
          data: [
            { type: 'max', name: 'Max' },
            { type: 'min', name: 'Min' }
          ]
        },
        markLine: {
          data: [{ type: 'average', name: 'Avg' }]
        }
      },
    ]
  };

  option && myChart.setOption(option);
})

// 在Vue3中，渲染完后执行函数
onMounted(() => {
  //调用需要执行的方法
  const ust = localStorage.getItem("ust");
  // console.log(ust);
  if (ust){
    let usn = localStorage.getItem("usn");
    let st = localStorage.getItem("st");
    let et = localStorage.getItem("et");
    let ust = localStorage.getItem("ust");
    let uet = localStorage.getItem("uet");
    // console.log(usn);
    document.getElementById("Fan").innerHTML = '已选择的风机代号为：'+ usn;
    document.getElementById("TimeRange").innerHTML = '对应的时间范围为：' + st + '~' + et;
    document.getElementById("UserTimeRange").innerHTML = '用户选择的时间范围为：' + ust + '~' + uet;
  }
});

watch(
    isDarkTheme,
    (val) => {
      if (val) {
        applyDarkTheme();
      } else {
        applyLightTheme();
      }
    },
    { immediate: true }
);

watch(
    layoutConfig.theme,
    () => {
      setColorOptions();
      setChart();
    },
    { immediate: true }
);

// 发送请求到后端进行预测
// 根据风机代号从后端获取时间范围

const ChooseM = ref();
const UpdateCM = () => {
    const ChooseMvalue = ChooseM.value;
    // console.log(ChooseMvalue)

    function show(cfg){
        swal({
            closeOnClickOutside: false,
            closeOnEsc: false,
            // 解构cfg对象，展开cfg对象所有属性
            ...cfg
        })
    }

    if (ChooseMvalue){
    // 将Choosevalue字典转换为列表
    var ChooseValue = Object.values(ChooseMvalue);
    console.log(ChooseValue)
    }
  var USERMODELCHOOSE = document.getElementsByName("USERMODELCHOOSE");
  var USERMODELCHOOSED=[];
  for(var i=0;i<USERMODELCHOOSE.length;i++){
    if(USERMODELCHOOSE[i].checked)
      USERMODELCHOOSED.push(USERMODELCHOOSE[i].value);
  }
  console.log(USERMODELCHOOSED)
    document.getElementById("Models").innerHTML = '已选择的模型有：'+ ChooseValue + ',' + USERMODELCHOOSED;
    const usn = localStorage.getItem("usn");
    const ust = localStorage.getItem("ust");
    const uet = localStorage.getItem("uet");
    // 获取权重
    // var WeightAR = 0;
    // var WeightMA = 0;
    // var WeightARMA = 0;
    // var WeightARIMA = 0;
    // var WeightSES = 0;
    // var WeightDES = 0;
    // var WeightTES = 0;
    // var WeightSARIMA = 0;
    // var WeightVAR = 0;
    // var WeightGARCH = 0;
    // var WeigthLSTM = 0;

    const WeightAR = document.getElementById("AR").value;
    const WeightMA = document.getElementById("MA").value;
    const WeightARMA = document.getElementById("ARMA").value;
    const WeightARIMA = document.getElementById("ARIMA").value;
    const WeightSES = document.getElementById("SES").value;
    const WeightDES = document.getElementById("DES").value;
    const WeightTES = document.getElementById("TES").value;
    const WeightSARIMA = document.getElementById("SARIMA").value;
    const WeightVAR = document.getElementById("VAR").value;
    const WeightGARCH = document.getElementById("GARCH").value;
    const WeigthLSTM = document.getElementById("LSTM").value



    document.getElementById("Weights").innerHTML = '对应的权重为：'+WeigthLSTM +''+  WeightAR +' '+ WeightMA +' '+ WeightARMA+' ' +WeightARIMA+' ' + WeightSES+' ' +WeightDES+' ' + WeightTES+' ' + WeightSARIMA+' ' +WeightVAR+' ' +WeightGARCH+' ';
    
// AR
  const method_ar = 'AR';
  //  获取填写的p值
  const ar_p = document.getElementById("ar_p").value;

//MA
  const method_ma = 'MA';
  //  获取填写的p值
  const ma_q = document.getElementById("ma_q").value;

//ARMA
  const method_arma = 'ARMA';
  //  获取填写的p值
  const arma_p = document.getElementById("arma_p").value;
  const arma_q = document.getElementById("arma_q").value;
 
//ARIMA
  const method_arima = 'ARIMA';
  //  获取填写的p值
  const arima_p = document.getElementById("arima_p").value;
  const arima_q = document.getElementById("arima_q").value;
  const arima_d = document.getElementById("arima_d").value;
  
  //TES
  const method_tes = 'TES';
  //  获取填写的p值
  const tes_seasonal_period = document.getElementById("tes_seasonal_period").value;
  function show(cfg){
    swal({
      closeOnClickOutside: false,
      closeOnEsc: false,
      // 解构cfg对象，展开cfg对象所有属性
      ...cfg
    })
  }
  

//SARIMA
  const method_sarima = 'SARIMA';
  //  获取填写的p值
  const sarima_order = document.getElementById("sarima_order").value;
  const sarima_seasonal_order = document.getElementById("sarima_seasonal_order").value;

  function show(cfg){
    swal({
      closeOnClickOutside: false,
      closeOnEsc: false,
      // 解构cfg对象，展开cfg对象所有属性
      ...cfg
    })
  }

//VAR
  const method_var = 'VAR';
  //  获取填写的p值
  const var_select_cols = document.getElementById("var_select_cols").value;
  const var_difference = document.getElementById("var_difference").value;
  const var_order = document.getElementById("var_order").value;
  function show(cfg){
    swal({
      closeOnClickOutside: false,
      closeOnEsc: false,
      // 解构cfg对象，展开cfg对象所有属性
      ...cfg
    })
  }


//GARCH
  const method_garch = 'GARCH';
  //  获取填写的p值
  const garch_p = document.getElementById("garch_p").value;
  const garch_q = document.getElementById("garch_q").value;
  var weights = [WeigthLSTM ,WeightAR, WeightMA, WeightARMA, WeightARIMA,
  WeightSES, WeightDES, WeightTES, WeightSARIMA,
  WeightVAR, WeightGARCH] 
  for (var w in weights){ 
    if (weights[w] == ""){
      weights[w]='0';
    } }

  var parameters = [[],[ar_p],[ma_q],[arma_p,arma_q],[arima_p,arima_q,arima_d],
                      [],[],[tes_seasonal_period],[sarima_order,sarima_seasonal_order],[var_select_cols,var_difference,var_order],
                      [garch_p,garch_q]]
    for (var list in parameters){ 
    for(var p in parameters[list]){
      if(parameters[list][p]==""){
        parameters[list][p]='0';
      }
       } } 

  console.log(weights)
  console.log(parameters)                    
  if (ust){
    axios.post('http://81.70.183.201:5000/ensemble', {
      usn,
      ust,
      uet,
      weights,
      parameters
    }).then(res => {
      const ret = res.data
      console.log(ret)
      if (ret.code){ // 错误
        show({
          title: '错误',
          text: ret.data.msg,
          icon: 'error',
          button: {
            text: '好的'
          }
        })
      }else { // 成功
        console.log(ret.data);
        var oYD15 = ret.original
        var datatime= ret.data["DATATIME"];
        var pYD15 =ret.data['YD15'];
        var acc = ret.data['acc']
        // var sysYD15=ret.sys_pre
        var save = function (name,arr) {
          localStorage.setItem(name,JSON.stringify(arr))
        }
        // var read=function(name){
        //   return  JSON.parse(localStorage.getItem(name))//把本地存储的my转成数组
        // }
        save("oYD15",oYD15)
        save("pYD15",pYD15);
        save("datatime",datatime)
        save("acc",acc)
        // save("sysYD15",sysYD15)
        var subtractedList = [];
        for (var i = 0; i < oYD15.length; i++) {
          var diff = oYD15[i] - pYD15[i];
          subtractedList.push(Math.abs(diff));
        }
        save("abs", subtractedList);

        var esemble_acc = ret.acc;
        localStorage.setItem("ar_acc", esemble_acc);
        {
          document.getElementById("ESEMBLEACC").innerHTML = '集成模型的准确率为：' + esemble_acc;
        }
        {
          var myChart = echarts.init(chart1.value);
          var option = {
            title: {
              text: '实际功率预测结果'
            },
            tooltip: {
              trigger: 'axis'
            },
            legend: {},
            toolbox: {
              show: true,
              feature: {
                dataZoom: {
                  yAxisIndex: 'none'
                },
                dataView: { readOnly: false },
                magicType: { type: ['line', 'bar'] },
                restore: {},
                saveAsImage: {}
              }
            },
            xAxis: {
              type: 'category',
              name: 'Time',
              boundaryGap: false,
              data: read("datatime")
            },
            yAxis: {
              type: 'value',
              name: 'Power',
              axisLabel: {
                formatter: '{value} KW'
              }
            },
            dataZoom: [
              {
                type: 'inside'
              },
              {
                type: 'slider',
                height: 10
              }
            ],
            series: [
              {
                name: 'Original',
                type: 'line',
                //   data: localStorage.getItem("pYD15"),
                data: read("oYD15"),
                markPoint: {
                  data: [
                    { type: 'max', name: 'Max' },
                    { type: 'min', name: 'Min' }
                  ]
                },
                markLine: {
                  data: [{ type: 'average', name: 'Avg' }]
                }
              },
              {
                name: 'Predicted',
                type: 'line',
                //   data: localStorage.getItem("pYD15"),
                data: read("pYD15"),
                markPoint: {
                  data: [
                    { type: 'max', name: 'Max' },
                    { type: 'min', name: 'Min' }
                  ]
                },
                markLine: {
                  data: [{ type: 'average', name: 'Avg' }]
                }
              }
            ]
          };

          option && myChart.setOption(option);
        }

        {
          var myChart = echarts.init(chart2.value);
          var option = {
            title: {
              text: '残差图'
            },
            tooltip: {
              trigger: 'axis'
            },
            legend: {},
            toolbox: {
              show: true,
              feature: {
                dataZoom: {
                  yAxisIndex: 'none'
                },
                dataView: { readOnly: false },
                magicType: { type: ['line', 'bar'] },
                restore: {},
                saveAsImage: {}
              }
            },
            xAxis: {
              type: 'category',
              name: ' 时间 ',
              boundaryGap: false,
              data: read("datatime")
            },
            yAxis: {
              type: 'value',
              name:' 残差值 ',
              axisLabel: {
                formatter: '{value} KW'
              }
            },
            dataZoom: [
              {
                type: 'inside'
              },
              {
                type: 'slider',
                height: 10
              }
            ],

            series: [
              {
                name: '残差',
                type: 'line',
                data: read("abs"),
                markPoint: {
                  data: [
                    { type: 'max', name: 'Max' },
                    { type: 'min', name: 'Min' }
                  ]
                },
                markLine: {
                  data: [{ type: 'average', name: 'Avg' }]
                }
              },
            ]
          };

          option && myChart.setOption(option);
        }
      }
    }).catch(err => {
      console.log(err);
    });
  }
}





onMounted(() => {
  let usermodelListCode = read("usermodelListCode");
  if (usermodelListCode){
  //  添加html内容
    const USERMODELCHOOSE = document.getElementById("USERMODELCHOOSE");
    for (var i in usermodelListCode){
      USERMODELCHOOSE.innerHTML += '<div><input type="checkbox"v-model="ChooseM"' +
          'id="UserModel' + usermodelListCode[i] +
          '"name="USERMODELCHOOSE" value="UserModel' + usermodelListCode[i] +
          '"><input class="ml-2" type="text"id="usermodel' + usermodelListCode[i] +
          'param"placeholder="请输入usermodel' + usermodelListCode[i] +
          'param值">' + '<input class="ml-2" type="text"id="usermodel' + usermodelListCode[i] +
      'weight"placeholder="请输入usermodel' + usermodelListCode[i] +
      '权重值">'
    }
  }
});

onMounted(() => {
  

  const ar_p = localStorage.getItem("ar_p");
  if (ar_p){
    document.getElementById("ar_p").value = ar_p;
  }
  const ma_q = localStorage.getItem("ma_q");
  if (ma_q){
    document.getElementById("ma_q").value = ma_q;
  }
  const arma_p = localStorage.getItem("arma_p");
  const arma_q = localStorage.getItem("arma_q");
  if (arma_p){
    document.getElementById("arma_p").value = arma_p;
    document.getElementById("arma_q").value = arma_q;
  }
  const arima_p = localStorage.getItem("arima_p");
  const arima_q = localStorage.getItem("ma_q");
  const arima_d = localStorage.getItem("ma_q");
  if (arima_p){
    document.getElementById("arima_p").value = arima_p;
    document.getElementById("arima_q").value = arima_q;
    document.getElementById("arima_d").value = arima_d;
  }
  const tes_seasonal_period = localStorage.getItem("tes_seasonal_period")
  if (tes_seasonal_period){
    document.getElementById("tes_seasonal_period").value = tes_seasonal_period
  }
  const sarima_order = localStorage.getItem("sarima_order")
  const sarima_seasonal_order = localStorage.getItem("sarima_seasonal_order")
  if (sarima_order){
    document.getElementById("sarima_order").value = sarima_order
    document.getElementById("sarima_seasonal_order").value = sarima_seasonal_order
  }
  const var_select_cols = localStorage.getItem("var_select_cols")
  const var_difference = localStorage.getItem("var_difference")
  const var_order = localStorage.getItem("var_order")
  if (var_select_cols){
    document.getElementById("var_select_cols").value = var_select_cols
    document.getElementById("var_difference").value = var_difference
    document.getElementById("var_order").value = var_order
  }
  const garch_p = localStorage.getItem("garch_p")
  const garch_q = localStorage.getItem("garch_q")
  if (garch_p){
    document.getElementById("garch_p").value = garch_p
    document.getElementById("garch_q").value = garch_q
  }

});


onMounted(() => {
  const esemble_acc = localStorage.getItem("esemble_acc");
  if (esemble_acc){
    document.getElementById("ESEMBLEACC").innerHTML = '集成模型的准确率为：' + esemble_acc;
  }
});

</script>


<template>
  <div class="grid p-fluid">

    <!-- 文本 -->
    <div class="col-12 md:col-6">
      <div class="card">
        <h5>Model Introduction</h5>
        <Accordion :activeIndex="0">
          <AccordionTab header="Introduction">
            <p class="line-height-3 m-0">
              当涉及到时间序列分析和预测时，多种模型的集成可以提供更强大、更灵活的预测工具。我们引入了一个创新的集成模型，让您能够将各种经典的时间序列预测方法和自定义上传的模型相结合。这个集成模型不仅充分发挥了不同模型的优势，还赋予了您以前所未有的预测自主性和灵活性。<br>
              我们的集成模型融合了自回归（AR）、移动平均（MA）、差分积分移动平均自回归（ARIMA）、简单指数平滑（SES）、双指数平滑（DES）、三指数平滑（TES）、季节性自回归移动平均（SARIMA）、广义自回归条件异方差（GARCH）等多种经典模型，和深度学习LSTM模型，同时还为您提供了上传自定义模型的功能。您可以根据龙源风电数据特点和预测需求，自由调整各模型的权重和参数，从而实现定制化的预测解决方案。
            </p>
          </AccordionTab>
          <AccordionTab header="Reference">
            <p class="line-height-3 m-0">
              参考文献
            </p>
          </AccordionTab>
        </Accordion>
      </div>
    </div>

    <div class="col-12 md:col-6">
      <div class="card">
        <h5>集成模型</h5>
        <Panel header="参数确认" :toggleable="true">
          <p class="line-height-3 m-0" id="Fan">
            已选择的风机代号为：
          </p>
          <p class="line-height-3 m-0" id="TimeRange">
            对应的时间范围为：
          </p>
          <p class="line-height-3 m-0" id="UserTimeRange">
            用户选择的时间范围为：
          </p>
          <p>
          </p>
        </Panel>
      </div>
    </div>
 

    <div class="col-12 md:col-6">
      <div class="card ">
        <h5>Chooseing models and weights</h5>
        <!-- LSTM -->
        <div class="card flex flex-wrap justify-content-center gap-5">
          
          <div class="flex align-items-center">
            <Checkbox v-model="ChooseM" inputId="MODEL0" name="LSTM" value="LSTM" />
            <label for="LSTM" class="ml-2"> LSTM </label>
          </div>
          
          <div class="col-span-1 ">
            <div class="grid grid-cols-1">
              <div class="card p-fluid">
                <h5>参数输入</h5>
                
                <div class="field">
                  <label for="LSTM">weight</label>
                  <InputText  id="LSTM" type="text" />
                </div>

              <!-- <Button label="确认" @click="ARPredict" /> -->
              </div>
            </div>
          </div>

        </div>

    
        <!-- AR -->
        <div class="card flex flex-wrap justify-content-center gap-5">
          
          <div class="flex align-items-center">
            <Checkbox v-model="ChooseM" inputId="MODEL1" name="AR" value="AR" />
            <label for="AR" class="ml-2"> AR </label>
          </div>
          
          <div class="col-span-1 ">
            <div class="grid grid-cols-1">
              <div class="card p-fluid">
                <h5>参数输入</h5>
                
                <div class="field">
                  <label for="AR">weight</label>
                  <InputText  id="AR" type="text" />
                </div>

                <div class="field">
                  <label for="ar_p" >p</label>
                  <InputText  id="ar_p" type="text" />
                </div>

              <!-- <Button label="确认" @click="ARPredict" /> -->
              </div>
            </div>
          </div>

        </div>

        <!-- MA -->
        <div class="card flex flex-wrap justify-content-center gap-5">

          <div class="flex align-items-center">
            <Checkbox v-model="ChooseM" inputId="MODEL2" name="MA" value="MA" />
            <label for="MA" class="ml-2"> MA </label>
          </div>

          <div class="col-span-1 ">
            <div class="grid grid-cols-1">
              <div class="card p-fluid">
                <h5>参数输入</h5>
                
                <div class="field">
                  <label for="MA">weight</label>
                  <InputText  id="MA" type="text" />
                </div>

                <div class="field">
                  <label for="ma_q" >q</label>
                  <InputText  id="ma_q" type="text" />
                </div>

              <!-- <Button label="确认" @click="ARPredict" /> -->
              </div>
            </div>
          </div>
        </div>

        <!-- ARMA -->
        <div class="card flex flex-wrap justify-content-center gap-5">
          
          <div class="flex align-items-center">
            <Checkbox v-model="ChooseM" inputId="MODEL3" name="ARMA" value="ARMA" />
            <label for="ARMA" class="ml-2"> ARMA </label>
          </div>

          <div class="col-span-1 ">
            <div class="grid grid-cols-1">
              <div class="card p-fluid">
                <h5>参数输入</h5>
                
                <div class="field">
                  <label for="ARMA">weight</label>
                  <InputText  id="ARMA" type="text" />
                </div>

                <div class="field">
                  <label for="arma_p" >p</label>
                  <InputText  id="arma_p" type="text" />
                </div>
                <div class="field">
                  <label for="arma_q" >q</label>
                  <InputText  id="arma_q" type="text" />
                </div>

              <!-- <Button label="确认" @click="ARPredict" /> -->
              </div>
            </div>
          </div>
        </div>

        <!-- ARIMA -->
        <div class="card flex flex-wrap justify-content-center gap-5"> 
          
          <div class="flex align-items-center">
            <Checkbox v-model="ChooseM" inputId="MODEL4" name="ARIMA" value="ARIMA" />
            <label for="ARIMA" class="ml-2"> ARIMA </label>
          </div>
          
          <div class="col-span-1 ">
            <div class="grid grid-cols-1">
              <div class="card p-fluid">
                <h5>参数输入</h5>
                
                <div class="field">
                  <label for="ARIMA">weight</label>
                  <InputText  id="ARIMA" type="text" />
                </div>

                <div class="field">
                  <label for="arima_p" >p</label>
                  <InputText  id="arima_p" type="text" />
                </div>
                <div class="field">
                  <label for="arima_q" >q</label>
                  <InputText  id="arima_q" type="text" />
                </div>
                <div class="field">
                  <label for="arima_d" >d</label>
                  <InputText  id="arima_d" type="text" />
                </div>

              <!-- <Button label="确认" @click="ARPredict" /> -->
              </div>
            </div>
          </div>
          
        </div>        
        
        <!-- SES -->
        <div class="card flex flex-wrap justify-content-center gap-5"> 
          <div class="flex align-items-center">
            <Checkbox v-model="ChooseM" inputId="MODEL5" name="SES" value="SES" />
            <label for="SES" class="ml-2"> SES </label>
          </div>
          <div class="col-span-1 ">
            <div class="grid grid-cols-1">
              <div class="card p-fluid">
                <h5>参数输入</h5>
                
                <div class="field">
                  <label for="SES">weight</label>
                  <InputText  id="SES" type="text" />
                </div>
              <!-- <Button label="确认" @click="ARPredict" /> -->
              </div>
            </div>
          </div>
        </div>
         
        </div>
    </div>

    <div class="col-12 md:col-6">
      <div class="card ">
        <!-- <h5>Chooseing models and parameters</h5>          -->

        <!-- DES -->
        <div class="card flex flex-wrap justify-content-center gap-5"> 
          <div class="flex align-items-center">
            <Checkbox v-model="ChooseM" inputId="MODEL6" name="DES" value="DES" />
            <label for="DES" class="ml-2"> DES </label>
          </div>
          <div class="col-span-1 ">
            <div class="grid grid-cols-1">
              <div class="card p-fluid">
                <h5>参数输入</h5>
                
                <div class="field">
                  <label for="DES">weight</label>
                  <InputText  id="DES" type="text" />
                </div>

              <!-- <Button label="确认" @click="ARPredict" /> -->
              </div>
            </div>
          </div>
        </div>

        <!-- TES -->
        <div class="card flex flex-wrap justify-content-center gap-5"> 
          
          <div class="flex align-items-center">
            <Checkbox v-model="ChooseM" inputId="MODEL7" name="TES" value="TES" />
            <label for="TES" class="ml-2"> TES </label>
          </div>
          
          <div class="col-span-1 ">
            <div class="grid grid-cols-1">
              <div class="card p-fluid">
                <h5>参数输入</h5>
                
                <div class="field">
                  <label for="TES">weight</label>
                  <InputText  id="TES" type="text" />
                </div>

                <div class="field">
                  <label for="tes_seasonal_period" >Seasonal Period</label>
                  <InputText  id="tes_seasonal_period" type="text" />
                </div>
                
              <!-- <Button label="确认" @click="ARPredict" /> -->
              </div>
            </div>
          </div>
        </div>
        
        <!-- SARIMA -->
        <div class="card flex flex-wrap justify-content-center gap-5"> 
          
          <div class="flex align-items-center">
            <Checkbox v-model="ChooseM" inputId="MODEL8" name="SARIMA" value="SARIMA" />
            <label for="SARIMA" class="ml-2"> SARIMA </label>
          </div>
          
          <div class="col-span-1 ">
            <div class="grid grid-cols-1">
              <div class="card p-fluid">
                <h5>参数输入</h5>
                
                <div class="field">
                  <label for="SARIMA">weight</label>
                  <InputText  id="SARIMA" type="text" />
                </div>

                <div class="field">
                  <label for="sarima_order" >(p,d,q)</label>
                  <InputText  id="sarima_order" type="text" />
                </div>
                <div class="field">
                  <label for="sarima_seasonal_order" >(P,D,Q,s)</label>
                  <InputText  id="sarima_seasonal_order" type="text" />
                </div>
                
              <!-- <Button label="确认" @click="ARPredict" /> -->
              </div>
            </div>
          </div>
        </div>

        <!-- VAR -->
        <div class="card flex flex-wrap justify-content-center gap-5"> 
          <div class="flex align-items-center">
            <Checkbox v-model="ChooseM" inputId="MODEL9" name="VAR" value="VAR" />
            <label for="VAR" class="ml-2"> VAR </label>
          </div>
          <div class="col-span-1 ">
            <div class="grid grid-cols-1">
              <div class="card p-fluid">
                <h5>参数输入</h5>
                
                <div class="field">
                  <label for="VAR">weight</label>
                  <InputText  id="VAR" type="text" />
                </div>

                <div class="field">
                  <label for="var_select_cols" >Selected columns</label>
                  <InputText  id="var_select_cols" type="text" />
                </div>
                <div class="field">
                  <label for="var_difference" >d</label>
                  <InputText  id="var_difference" type="text" />
                </div>
                <div class="field">
                  <label for="var_order" >order</label>
                  <InputText  id="var_order" type="text" />
                </div>
                
              <!-- <Button label="确认" @click="ARPredict" /> -->
              </div>
            </div>
          </div>
        </div>

        <!-- GARCH -->
        <div class="card flex flex-wrap justify-content-center gap-5">   
          <div class="flex align-items-center">
            <Checkbox v-model="ChooseM" inputId="MODEL10" name="GARCH" value="GARCH" />
            <label for="GARCH" class="ml-2"> GARCH </label>
          </div>

          <div class="col-span-1 ">
            <div class="grid grid-cols-1">
              <div class="card p-fluid">
                <h5>参数输入</h5>
                
                <div class="field">
                  <label for="GARCH">weight</label>
                  <InputText  id="GARCH" type="text" />
                </div>

                <div class="field">
                  <label for="garch_p" >p</label>
                  <InputText  id="garch_p" type="text" />
                </div>
                <div class="field">
                  <label for="garch_q" >q</label>
                  <InputText  id="garch_q" type="text" />
                </div>
                
              <!-- <Button label="确认" @click="ARPredict" /> -->
              </div>
            </div>
          </div>
        </div>

        <div class="flex align-items-center">
          <Button label="更新" @click="UpdateCM"></Button>
        </div>
      </div>
    </div>

    <!-- 用户模型参数选择 -->
    <div class="col-12">
        <div class="card" id="USERMODELCHOOSE">
<!--          <div>-->
<!--            <input type="checkbox"-->
<!--                   v-model="ChooseM"-->
<!--                   inputId="UserModel1"-->
<!--                   name="ChooseM"-->
<!--                   value="UserModel1"-->
<!--            >-->
<!--            <input class="ml-2" type="text"-->
<!--                   id="usermodel1param"-->
<!--                   placeholder="请输入usermodel1param值">-->
<!--          <input class="ml-2" type="text"-->
<!--                             id="usermodel1weight"-->
<!--                             placeholder="请输入usermodel1权重">-->

<!--          </div>-->

<!--          <div>-->
<!--            <input type="checkbox"-->
<!--                   v-model="UserModelChoose"-->
<!--                   inputId="UserModel1"-->
<!--                   name="UserModelChoose"-->
<!--                   value="UserModel1"-->
<!--            >-->
<!--            <input class="ml-2" type="text"-->
<!--                   id="UserModelparam"-->
<!--                   placeholder="请输入param值">-->
<!--          </div>-->
        </div>
    </div>


    <!-- 模型参数选择示例 -->
    <div class="col-12">
      <div class="card">
        <Panel header="已选择的模型及其权重" :toggleable="true">
          <p class="line-height-3 m-0" id="Models">
            已选择的模型有：
          </p>
          <p class="line-height-3 m-0" id="Weights">
            对应的权重为：
          </p>
        </Panel>
      </div>
    </div>


    <div class="col-12">
      <div class="card">
        <Panel header="日准确率" :toggleable="true">
          <p class="line-height-3 m-0" id="ESEMBLEACC">

          </p>
        </Panel>
      </div>
    </div>



    <!-- 图表 -->
    <div class="col-12">
      <div class="card">
        <div ref="chart1" style="width: 1000px; height: 400px;"></div>
      </div>
    </div>
    <div class="col-12">
      <div class="card">
        <div ref="chart2" style="width: 1000px; height: 400px;"></div>
      </div>
    </div>

  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/demo/styles/badges.scss';
@import '@/assets/demo/styles/items.scss';
</style>
