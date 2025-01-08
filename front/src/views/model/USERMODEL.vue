<script setup>
import ProductService from '@/service/ProductService';
import PhotoService from '@/service/PhotoService';
import { useLayout } from '@/layout/composables/layout';
import NodeService from '@/service/NodeService';
import { onMounted, ref, watch }  from 'vue';
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
import {useToast} from "primevue/usetoast";


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

const USERMODELchart1 = ref();
const USERMODELchart2 = ref();
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

const toast = useToast();
const onUpload =(csvfile) => {
  toast.add({ severity: 'info', summary: 'Success', detail: 'File Uploaded', life: 3000 });
  // 获取上传的文件，并打印
  const file = csvfile.files[0];
  let formData = new FormData();
  formData.append('file', file);
  formData.append('filename', file.name);
  //    将Upload标签上传的文件传给后端
  axios.post('http://81.70.183.201:5000/GetUserModel', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }).then(res => {
    const ret = res.data
    if (ret.code){ // 错误
      toast.add({ severity: 'error', summary: 'Error', detail: ret.data.msg, life: 3000 });
    }else { // 成功
      toast.add({ severity: 'success', summary: 'Success', detail: ret.data.msg, life: 3000 });
    }
  }).catch(err => {
    toast.add({ severity: 'error', summary: 'Error', detail: err, life: 3000 });
  });
};
var read=function(name){
  return  JSON.parse(localStorage.getItem(name))//把本地存储的my转成数组
}
var save = function (name,arr) {
  localStorage.setItem(name,JSON.stringify(arr))
}
onMounted(()=>{
  var myChart = echarts.init(USERMODELchart1.value);
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
      data: read("USERMODELdatatime")
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
        data: read("USERMODELoYD15"),
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
        data: read("USERMODELpYD15"),
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
  var myChart = echarts.init(USERMODELchart2.value);
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
      data: read("USERMODELdatatime")
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
        data: read("USERMODELabs"),
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

// 初始化看是否要添加用户模型


const ADDUSERMODEL = () => {
  // localStorage.removeItem("usermodelListCode");
  let usermodeList = read("usermodeList");
  let usermodelListCode = read("usermodelListCode");
  console.log(usermodelListCode);
  // console.log(usermodelListCode.length);
  // localStorage.removeItem("usermodelListCode");
  // save("usermodelListCode",usermodelListCode);
  // localStorage.removeItem("usermodelListCode");
  // console.log(usermodelListCode);
  if(!usermodelListCode){
    usermodelListCode = [1];
    usermodeList = [{ name: 'usermodel1', code: '1' }];
  }
  else {
    usermodelListCode[usermodelListCode.length] = usermodelListCode[usermodelListCode.length-1] + 1;
    usermodeList.push({ name: 'usermodel' + usermodelListCode[usermodelListCode.length-1], code: usermodelListCode[usermodelListCode.length-1].toString() });
  }
  console.log(usermodelListCode);
  console.log(usermodeList);

  // // 重置selectusermodels.value
  selectusermodels.value = [];
  for (var i in usermodeList){
    // console.log(usermodeList[i]);
    //重置selectusermodels.value
    selectusermodels.value.push(usermodeList[i]);
  }
  // selectusermodels.value.push(usermodeList[i]);
  save("usermodeList",usermodeList);
  save("usermodelListCode",usermodelListCode);

};

const DELETEUSERMODEL = () => {
  let usermodeList = read("usermodeList");
  let usermodelListCode = read("usermodelListCode");
  let code = selectedusermodels.value.code;
  console.log(code);
  code = parseInt(code);
  // save("usermodelListCode",usermodelListCode);
  console.log(usermodelListCode);
  // let code = 8;
//  删除usermodelListCode中与code相同的元素
  for (let i in usermodelListCode) {
    // console.log(usermodelListCode[i]);
    if (usermodelListCode[i] === code) {
      //  删除usermodelListCode中与code相同的值
      usermodelListCode.splice(i, 1);
      usermodeList.splice(i, 1);
    }
  }

  selectusermodels.value = [];
  for (var i in usermodeList){
    // console.log(usermodeList[i]);
    //重置selectusermodels.value
    selectusermodels.value.push(usermodeList[i]);
  }
  // selectusermodels.value.push(usermodeList[i]);
  save("usermodeList",usermodeList);
  save("usermodelListCode",usermodelListCode);
};


const USERMODELPRED = () => {
  const method = selectedusermodels.value.code;
  const usn = localStorage.getItem("usn");
  const ust = localStorage.getItem("ust");
  const uet = localStorage.getItem("uet");
  //  获取填写的p值
  const UserModelparam = document.getElementById("UserModelparam").value;
  function show(cfg){
    swal({
      closeOnClickOutside: false,
      closeOnEsc: false,
      // 解构cfg对象，展开cfg对象所有属性
      ...cfg
    })
  }
  if (ust){

    axios.post('http://81.70.183.201:5000/USERMODELPRED', {
      method,
      usn,
      ust,
      uet,
      UserModelparam
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
        save("USERMODELoYD15",oYD15)
        save("USERMODELpYD15",pYD15);
        save("USERMODELdatatime",datatime)
        // save("sysYD15",sysYD15)
        var subtractedList = [];
        for (var i = 0; i < oYD15.length; i++) {
          var diff = oYD15[i] - pYD15[i];
          subtractedList.push(Math.abs(diff));
        }
        save("USERMODELabs", subtractedList);
        localStorage.setItem("UserModelparam", UserModelparam);

        var usermodel_acc = ret.acc;
        localStorage.setItem("usermodel_acc", usermodel_acc);
        {
          document.getElementById("USERMODELACC").innerHTML = '用户模型的准确率为：' + usermodel_acc;
        }
        {
          var myChart = echarts.init(USERMODELchart1.value);
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
              data: read("USERMODELdatatime")
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
                data: read("USERMODELoYD15"),
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
                data: read("USERMODELpYD15"),
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
          var myChart = echarts.init(USERMODELchart2.value);
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
              data: read("USERMODELdatatime")
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
                data: read("USERMODELabs"),
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

// const UserModelChoose = ref();


let usermodeList = read("usermodeList");
//
const selectusermodels = ref(usermodeList);
// // console.log(selectusermodels.value)
const selectedusermodels = ref(null);

onMounted(() => {
  const UserModelparam = localStorage.getItem("UserModelparam");
  if (UserModelparam){
    document.getElementById("UserModelparam").value = UserModelparam;
  }
});

onMounted(() => {
  const usermodel_acc = localStorage.getItem("usermodel_acc");
  if (usermodel_acc){
    document.getElementById("USERMODELACC").innerHTML = '用户模型的准确率为：' + usermodel_acc;
  }
});
</script>


<template>
  <div class="grid p-fluid">

    <div class="col-12 md:col-6">
      <div class="card">
<!--        <h5>AR</h5>-->
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

    <!-- 文本 -->
    <div class="col-12 md:col-6">
      <div class="card">
        <h5>用户模型</h5>
        <div  class="card">
          <Button label="添加模型" class="mr-2 mb-2" @click="ADDUSERMODEL" />
<!--          <Button label="增加模型" class="mr-2 mb-2" @click="ADDUSERMODEL" />-->
        </div>

<!--        <Accordion :activeIndex="0">-->
<!--          <AccordionTab header="Introduction">-->
<!--            <p class="line-height-3 m-0">-->
<!--              模型简介-->
<!--            </p>-->
<!--          </AccordionTab>-->
<!--          <AccordionTab header="Reference">-->
<!--            <p class="line-height-3 m-0">-->
<!--              参考文献-->
<!--            </p>-->
<!--          </AccordionTab>-->
<!--        </Accordion>-->
      </div>
    </div>

    <!-- 列表 -->
    <div class="col-12">
      <div class="card">
        <h5>Parameter details</h5>
        <TreeTable :value="model1Value"  v-model:selectionKeys="selectedTreeTableValue">
          <Column field="name" header="Parameter"></Column>
<!--          <Column field="size" header="Size"></Column>-->
          <Column field="type" header="Introduction"></Column>
        </TreeTable>
      </div>
    </div>

<!--    模型的上传、选择和参数输入-->
    <div class="col-12">
      <div class="card">
        <div>
          <!--   添加div选择风机的选项-->
          <div class="fj-grid" id="Fj">
            <div class="card" id="FjSelect">
              <h5>用户模型选择</h5>
              <!--      使用main.js中的Dropdown来选择1~20号风机-->
              <!--令选择框和按钮居中-->
              <div class="p-d-flex p-jc-center">
                <Dropdown v-model="selectedusermodels"
                          :options="selectusermodels"
                          optionLabel="name"
                          placeholder="请选择一个模型"
                ></Dropdown>
                <!--          令Dropdown与Button在同一行间存在少许间隙-->
                <br>
                <br>
<!--                <Button label="确定" @click="onSelect"></Button>-->
              </div>
            </div>
          </div>
          <h5>请上传python文件</h5>
          <FileUpload name="demo[]" @uploader="onUpload" :multiple="true" customUpload>
            <template #empty>
              <p>拖拽文件到此处上传</p>
            </template>
          </FileUpload>

<!--          <form id="UploadUserModelFile" action="http://81.70.183.201:5000/TraditionalPred" method="post" enctype="multipart/form-data">-->
<!--            <input type="file" id="UserModelFile" name="UserModelFile"/>-->
<!--            <input type="button" value="上传" onclick="submitform" />-->
<!--          </form>-->
<!--          <button type="button" class="ml-2" icon="pi pi-search" @click="submitform">上传</button>-->
        </div>
        <br>

        <div class="card">
<!--          <input type="checkbox"-->
<!--                 v-model="UserModelChoose"-->
<!--                 id="UserModel1"-->
<!--                 name="UserModelChoose"-->
<!--                 value="UserModel1"-->
<!--          >-->

          <InputText id="UserModelparam"
                     v-model="UserModelparam"
                     placeholder="请输入参数"
          ></InputText>
          <br>
          <br>

          <Button label="模型预测" class="mr-2 mb-2" @click="USERMODELPRED" />
          <Button label="删除模型" class="mr-2 mb-2" @click="DELETEUSERMODEL" />
<!--          <input class="ml-2" type="text"-->
<!--                 id="UserModelparam"-->
<!--                 placeholder="请输入param值">-->
<!--          <button type="button" class="ml-2" icon="pi pi-search" @click="USERMODELPRED">模型预测</button>-->
<!--          <button type="button" class="ml-2" icon="pi pi-search" @click="DELETEUSERMODEL">删除模型</button>-->
        </div>
      </div>
    </div>

    <div class="col-12">
      <div class="card">
        <Panel header="日准确率" :toggleable="true">
          <p class="line-height-3 m-0" id="USERMODELACC">

          </p>
        </Panel>
      </div>
    </div>

    <!-- 图表 -->
    <div class="col-12">
      <div class="card">
        <div ref="USERMODELchart1" style="width: 1000px; height: 400px;"></div>
      </div>
    </div>
    <div class="col-12">
      <div class="card">
        <div ref="USERMODELchart2" style="width: 1000px; height: 400px;"></div>
      </div>
    </div>

  </div>


</template>

<style lang="scss" scoped>
@import '@/assets/demo/styles/badges.scss';
@import '@/assets/demo/styles/items.scss';
</style>
