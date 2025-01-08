<script setup>
import ProductService from '@/service/ProductService';
import PhotoService from '@/service/PhotoService';
import { useLayout } from '@/layout/composables/layout';
import NodeService from '@/service/NodeService';
import { onMounted, ref, watch}  from 'vue';
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
      data: read("TESdatatime")
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
        data: read("TESoYD15"),
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
        data: read("TESpYD15"),
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
      data: read("TESdatatime")
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
        data: read("TESabs"),
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

const TESPredict = () => {
  const method = 'TES';
  const usn = localStorage.getItem("usn");
  const ust = localStorage.getItem("ust");
  const uet = localStorage.getItem("uet");
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
  if (ust){
    axios.post('http://81.70.183.201:5000/TraditionalPred', {
      method,
      usn,
      ust,
      uet,
      tes_seasonal_period
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
        // console.log('test')
        // console.log(ret.data.msg);
      }else { // 成功
        console.log(ret.data);
        var oYD15 = ret.original
        var datatime= ret.data["DATATIME"];
        var pYD15 =ret.data['YD15'];
        // var sysYD15=ret.sys_pre
        var save = function (name,arr) {
          localStorage.setItem(name,JSON.stringify(arr))
        }
        // var read=function(name){
        //   return  JSON.parse(localStorage.getItem(name))//把本地存储的my转成数组
        // }
        save("TESoYD15",oYD15)
        save("TESpYD15",pYD15);
        save("TESdatatime",datatime)
        // save("sysYD15",sysYD15)
        var subtractedList = [];
        for (var i = 0; i < oYD15.length; i++) {
          var diff = oYD15[i] - pYD15[i];
          subtractedList.push(Math.abs(diff));
        }
        save("TESabs", subtractedList);
        if(localStorage.getItem('tes_seasonal_period')){
          localStorage.removeItem('tes_seasonal_period');
        }
        localStorage.setItem('tes_seasonal_period', tes_seasonal_period);

        var tes_acc = ret.acc;
        localStorage.setItem("tes_acc", tes_acc);
        {
          document.getElementById("TESACC").innerHTML = 'TES模型的准确率为：' + tes_acc;
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
              data: read("TESdatatime")
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
                data: read("TESoYD15"),
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
                data: read("TESpYD15"),
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
              data: read("TESdatatime")
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
                data: read("TESabs"),
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

};

onMounted(() => {
  const tes_seasonal_period = localStorage.getItem("tes_seasonal_period");
  if (tes_seasonal_period){
    document.getElementById("tes_seasonal_period").value = tes_seasonal_period;
  }
});

onMounted(() => {
  const tes_acc = localStorage.getItem("tes_acc");
  if (tes_acc){
    document.getElementById("TESACC").innerHTML = 'TES模型的准确率为：' + tes_acc;
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
              三指数平滑（Triple Exponential Smoothing，TES）模型是一种用于时间序列预测的方法，它是简单指数平滑（SES）和双指数平滑（DES）模型的扩展，专门用于处理具有趋势和季节性的数据。TES模型不仅考虑了数据的平滑和趋势，还引入了季节性的考虑，使其适用于具有季节性的时间序列数据。<br>
              TES模型的核心特点包括：<br>
                平滑处理： 类似于SES和DES模型，TES模型采用指数加权平均的方法，将较近时刻的观测值赋予较大的权重，以平滑时间序列数据。<br>
                趋势处理： TES模型引入了一个额外的指数加权平均来捕捉数据的线性趋势。<br>
                季节性处理： TES模型还引入了季节性因素，以捕捉数据中的季节性模式。这意味着TES模型可以更好地预测具有明显季节性波动的时间序列数据。<br>
                三个平滑参数： 与SES和DES模型不同，TES模型有三个平滑参数，分别用于平滑数据、趋势和季节性。
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
        <h5>TES</h5>
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
<!--          <Button label="开始预测" class="mr-2 mb-2" @click="LSTMPredict" />-->
        </Panel>
      </div>
    </div>
    <!-- 列表 -->
    <div class="col-12">
      <div class="card">
        <h5>Parameter details</h5>
        <TreeTable :value="model1Value"  v-model:selectionKeys="selectedTreeTableValue">
          <Column field="name" header="Parameter"></Column>
          <Column field="size" header="Size"></Column>
          <Column field="type" header="Introduction"></Column>
        </TreeTable>
      </div>
    </div>
    <!-- 模型参数选择 -->
    <div class="col-12 md:col-6">
      <div class="card">
        <!--        分成两列，左侧给出所需填写的参数的值，右侧确认-->
        <h5>参数输入</h5>
          <div class="col-span-1 ">
            <div class="grid grid-cols-1">
              <div class="card p-fluid">
                <div class="field">
                  <label for="tes_seasonal_period" >Seasonal Period</label>
                  <InputText  id="tes_seasonal_period" type="text" />
                </div>
                <Button label="确认" @click="TESPredict" />
              </div>
            </div>
          </div>
      </div>
    </div>

    <!-- 模型参数选择示例 -->
    <div class="col-12 md:col-6">
      <div class="card">
        <Panel header="示例" :toggleable="true">
          <p class="line-height-3 m-0" id="Fan">
            Seasonal Period = 24*4
          </p>
          <p>
          </p>
        </Panel>
      </div>
    </div>


    <div class="col-12">
      <div class="card">
        <Panel header="日准确率" :toggleable="true">
          <p class="line-height-3 m-0" id="TESACC">

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
