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
      data: read("GARCHdatatime")
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
        data: read("GARCHoYD15"),
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
        data: read("GARCHpYD15"),
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
      data: read("GARCHdatatime")
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
        data: read("GARCHabs"),
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

const GARCHPredict = () => {
  const method = 'GARCH';
  const usn = localStorage.getItem("usn");
  const ust = localStorage.getItem("ust");
  const uet = localStorage.getItem("uet");
  //  获取填写的p值
  const garch_p = document.getElementById("garch_p").value;
  const garch_q = document.getElementById("garch_q").value;
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
      garch_p,
      garch_q
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
        save("GARCHoYD15",oYD15)
        save("GARCHpYD15",pYD15);
        save("GARCHdatatime",datatime)
        // save("sysYD15",sysYD15)
        var subtractedList = [];
        for (var i = 0; i < oYD15.length; i++) {
          var diff = oYD15[i] - pYD15[i];
          subtractedList.push(Math.abs(diff));
        }
        save("GARCHabs", subtractedList);
        localStorage.setItem("garch_p", garch_p);
        localStorage.setItem("garch_q", garch_q);

        var garch_acc = ret.acc;
        localStorage.setItem("garch_acc", garch_acc);
        {
          document.getElementById("GARCHACC").innerHTML = 'GARCHACC模型的准确率为：' + garch_acc;
        }
      }
    }).catch(err => {
      console.log(err);
    });
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
          data: read("GARCHdatatime")
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
            data: read("UserModelparam"),
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
            data: read("GARCHpYD15"),
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
          data: read("GARCHdatatime")
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
            data: read("GARCHabs"),
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
  }

};

onMounted(() => {
  const garch_p = localStorage.getItem("garch_p");
  const garch_q = localStorage.getItem("garch_q");
  if (garch_p){
    document.getElementById("garch_p").value = garch_p;
    document.getElementById("garch_q").value = garch_q;
  }
});

onMounted(() => {
  const garch_acc = localStorage.getItem("garch_acc");
  if (garch_acc){
    document.getElementById("GARCHACC").innerHTML = 'GARCHACC模型的准确率为：' + garch_acc;
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
              广义自回归条件异方差（Generalized Autoregressive Conditional Heteroskedasticity，GARCH）模型是一种用于建模和预测金融时间序列波动性的统计方法。GARCH模型旨在捕捉时间序列数据中的异方差性，即波动性在不同时期可能会发生变化的特征。它在金融学领域广泛应用于波动性建模、风险管理和期权定价等问题。<br>
              GARCH模型的核心特点包括：<br>
                异方差性建模： GARCH模型的主要目标是建立波动性的模型，即变量的方差在不同时期可能会变化。这种异方差性可能是金融市场中常见的，例如在市场动荡或重要事件发生时，波动性可能会显著增加。<br>
                自回归结构： GARCH模型基于自回归结构，即当前时刻的波动性受到过去时刻波动性的影响。不同的GARCH模型可能具有不同的自回归阶数和滞后项。<br>
                条件异方差性： GARCH模型中的异方差性是条件异方差性，即波动性的变化取决于过去的观测值和模型参数。这使得GARCH模型能够适应数据中的变化波动性。                模型参数估计： GARCH模型的参数通常使用极大似然估计等统计方法来进行估计。这些参数可以用来推断波动性的动态模式。
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
        <h5>GARCH</h5>
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
                  <label for="garch_p" >p</label>
                  <InputText  id="garch_p" type="text" />
                </div>
                <div class="field">
                  <label for="garch_q" >q</label>
                  <InputText  id="garch_q" type="text" />
                </div>
                <Button label="确认" @click="GARCHPredict" />
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
            p = 5
          </p>
          <p class="line-height-3 m-0" id="TimeRange">
            q = 5
          </p>
<!--          <p class="line-height-3 m-0" id="UserTimeRange">-->
<!--            用户选择的时间范围为：-->
<!--          </p>-->
          <p>
          </p>
        </Panel>
      </div>
    </div>

    <div class="col-12">
      <div class="card">
        <Panel header="日准确率" :toggleable="true">
          <p class="line-height-3 m-0" id="GARCHACC">

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
