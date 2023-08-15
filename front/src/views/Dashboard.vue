<script setup>
// DBar start
import ProductService from '@/service/ProductService';
import PhotoService from '@/service/PhotoService';
import { useLayout } from '@/layout/composables/layout';
import NodeService from '@/service/NodeService';
import { onMounted, ref, watch}  from 'vue';
import * as echarts from 'echarts'
import {
  TitleComponent,
  GridComponent,
  LegendComponent,
  MarkLineComponent,
  MarkPointComponent,
  DatasetComponent,
  DataZoomComponent,
  TransformComponent,
  VisualMapComponent,
  BrushComponent,
  MarkAreaComponent,
  ToolboxComponent,
  TooltipComponent,
  ParallelComponent,
} from 'echarts/components';
import { 
    LineChart, 
    BoxplotChart, 
    ScatterChart,
    HeatmapChart, 
    ParallelChart,
    BarChart
} from 'echarts/charts';
import { UniversalTransition } from 'echarts/features';
import { CanvasRenderer } from 'echarts/renderers';
import { Bar3DChart } from 'echarts-gl/charts';
import { Grid3DComponent } from 'echarts-gl/components';
import swal from "sweetalert";
import axios from "axios";
// DBar end




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
const chart3 = ref();
// const chart4 = ref();
const chart6 = ref();
// DBar start
// 三维柱状图
const chart7 = ref();
// DBar end
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
  UniversalTransition,
  DatasetComponent,
  DataZoomComponent,
  TransformComponent,
  BoxplotChart,
  ScatterChart,
  VisualMapComponent,
  HeatmapChart,
  BrushComponent,
  MarkAreaComponent,
  ParallelComponent,
  ParallelChart,
  BarChart,
  Grid3DComponent,
  Bar3DChart
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

// 首先判断本地存储是否有数据，如果有数据就用本地存储的数据，如果没有就用默认的数据
//日历 function
function getVirtualData(year) {
  const date = +echarts.time.parse(year + '-01-01');
  const end = +echarts.time.parse(+year + 1 + '-01-01');
  const dayTime = 3600 * 24 * 1000;
  const data = [];
  for (let time = date; time < end; time += dayTime) {
    data.push([
      echarts.time.format(time, '{yyyy}-{MM}-{dd}', false),
      Math.floor(Math.random() * 1000)
    ]);
  }
  return data;
}
let haveData = localStorage.getItem('Home_usn')
if(haveData){
  // 有数据就用本地存储的数据
  // 各参数变化情况
  onMounted(()=>{
    var myChart = echarts.init(chart1.value);
    var option = {
      title: {
        text: '各参数变化情况'
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
        boundaryGap: false,
        data: read('HomepageDATATIME')
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          formatter: '{value}'
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
          name: 'PREPOWER',
          type: 'line',
          data: read('HomepagePREPOWER'),
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
        {
          name: 'PRESSURE',
          type: 'line',
          data: read('HomepagePRESSURE'),
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
        {
          name: 'ROUND(A.POWER,0)',
          type: 'line',
          data: read('HomepageROUND0'),
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
        {
          name: 'YD15',
          type: 'line',
          data: read('HomepageYD15'),
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
      ]
    };

    option && myChart.setOption(option);
  })
  onMounted(()=>{
    var myChart = echarts.init(chart6.value);
    var option = {
      title: {
        text: '各参数变化情况'
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
        boundaryGap: false,
        data: read('HomepageDATATIME')
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          formatter: '{value}'
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
          name: 'WINDSPEED',
          type: 'line',
          data: read('HomepageWINDSPEED'),
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
        {
          name: 'TEMPERATURE',
          type: 'line',
          data: read('HomepageTEMPERATURE'),
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
        {
          name: 'WINDDIRECTION',
          type: 'line',
          data: read('HomepageWINDDIRECTION'),
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
        {
          name: 'HUMIDITY',
          type: 'line',
          data: read('HomepageHUMIDITY'),
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
        {
          name: 'ROUND(A.WS,1)',
          type: 'line',
          data: read('HomepageROUND1'),
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
      ]
    };

    option && myChart.setOption(option);
  })
  // 箱线图
  onMounted(()=>{
    var myChart = echarts.init(chart2.value);
    var option = {
      title: [
        {
          text: '各参数箱线图',
          left: 'center'
        },
      ],
      dataset: [
        {
          // prettier-ignore
          source: [
            read('HomepageWINDSPEED'),
            read('HomepageWINDDIRECTION'),
            read('HomepagePREPOWER'),
            read('HomepageTEMPERATURE'),
            read('HomepagePRESSURE'),
            read('HomepageHUMIDITY'),
            read('HomepageROUND0'),
            read('HomepageROUND1'),
            read('HomepageYD15'),
          ]
        },
        {
          transform: {
            type: 'boxplot',
            config: {
              itemNameFormatter: function (params) {
                return ['WINDSPEED','WINDDIRECTION','PREPOWER','TEMPERATURE','PRESSURE','HUMIDITY','ROUND0','ROUND1','YD15'][params.value];
              }
            }
          }
        },
        {
          fromDatasetIndex: 1,
          fromTransformResult: 1
        }
      ],
      tooltip: {
        trigger: 'item',
        axisPointer: {
          type: 'shadow'
        }
      },
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
      grid: {
        left: '10%',
        right: '10%',
        bottom: '15%'
      },
      yAxis: {
        type: 'category',
        boundaryGap: true,
        nameGap: 30,
        splitArea: {
          show: false
        },
        splitLine: {
          show: false
        }
      },
      xAxis: {
        type: 'value',
        // name: 'km/s minus 299,000',
        splitArea: {
          show: true
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
          name: 'boxplot',
          type: 'boxplot',
          datasetIndex: 1
        },
        {
          name: 'outlier',
          type: 'scatter',
          encode: { x: 1, y: 0 },
          datasetIndex: 2
        }
      ]
    };

    option && myChart.setOption(option);
  })
  // 热力图
  const hours = [
    'PREPOWER','PRESSURE','TEMPERATURE','ROUND(A.POWER,0)','ROUND(A.WS,1)','WINDSPEED','WINDDIRECTION'
  ];
  const days = [
    'PREPOWER','PRESSURE','TEMPERATURE','ROUND(A.POWER,0)','ROUND(A.WS,1)','WINDSPEED','WINDDIRECTION','HUMIDITY'
  ];
  const data = [
    [0, 0, 1], [0, 1, read('HomepagePREPOWER_PRESURE')], [0, 2, read('HomepagePREPOWER_TEMPERATURE')], [0, 3, read('HomepagePREPOWER_ROUND0')], [0, 4, read('HomepagePREPOWER_ROUND1')], [0, 5, read('HomepagePREPOWER_WINDSPEED')], [0, 6, read('HomepagePREPOWER_WINDDIRECTION')],[0, 7, read('HomepagePREPOWER_HUMIDITY')],
    [1, 0, read('HomepagePREPOWER_PRESURE')], [1, 1, 1], [1, 2,  read('HomepagePRESSURE_ROUND0')], [1, 3, read('HomepagePRESSURE_ROUND0')], [1, 4, read('HomepagePRESSURE_ROUND1')], [1, 5, read('HomepagePRESSURE_WINDSPEED')], [1, 6, read('HomepagePRESSURE_WINDDIRECTION')],[7, 1, read('HomepagePRESSURE_HUMIDITY')],
    [2, 0, read('HomepagePREPOWER_TEMPERATURE')], [2, 1,  read('HomepagePRESSURE_TEMPERATURE')], [2, 2, 1], [2, 3, read('HomepageTEMPERATURE_ROUND0')], [2, 4, read('HomepageTEMPERATURE_ROUND1')], [2, 5, read('HomepageTEMPERATURE_WINDSPEED')], [2, 6, read('HomepageTEMPERATURE_WINDDIRECTION')],[2, 7, read('HomepageTEMPERATURE_HUMIDITY')],
    [3, 0, read('HomepagePREPOWER_ROUND0')], [3, 1,  read('HomepagePRESSURE_ROUND0')], [3, 2, read('HomepageTEMPERATURE_ROUND0')], [3, 3, 1], [3, 4, read('HomepageROUND0_ROUND1')], [3, 5, read('HomepageROUND0_WINDSPEED')], [3, 6, read('HomepageROUND0_WINDDIRECTION')],[3, 7, read('HomepageROUND0_HUMIDITY')],
    [4, 0, read('HomepagePREPOWER_ROUND1')], [4, 1,  read('HomepagePRESSURE_ROUND1')], [4, 2, read('HomepageTEMPERATURE_ROUND1')], [4, 3, read('HomepageROUND0_ROUND1')], [4, 4, 1], [4, 5, read('HomepageROUND1_WINDSPEED')], [4, 6, read('HomepageROUND1_WINDDIRECTION')],[4, 7, read('HomepageROUND1_HUMIDITY')],
    [5, 0, read('HomepagePREPOWER_WINDSPEED')], [5, 1,  read('HomepagePRESSURE_WINDSPEED')], [5, 2, read('HomepageTEMPERATURE_WINDSPEED')], [5, 3, read('HomepageROUND0_WINDSPEED')], [5, 4, read('HomepageROUND1_WINDSPEED')], [5, 5, 1], [5, 6, read('HomepageWINDSPEED_WINDDIRECTION')],[5, 7, read('HomepageWINDSPEED_HUMIDITY')],
    [6, 0, read('HomepagePREPOWER_WINDDIRECTION')], [6,  1, read('HomepagePRESSURE_WINDDIRECTION')], [6, 2, read('HomepageTEMPERATURE_WINDDIRECTION')], [6, 3, read('HomepageROUND0_WINDDIRECTION')], [6, 4, read('HomepageROUND1_WINDDIRECTION')], [6, 5, read('HomepageWINDSPEED_WINDDIRECTION')], [6,6,1],[6, 7, read('HomepageWINDDIRECTION_HUMIDITY')],
    [7, 0, read('HomepagePREPOWER_HUMIDITY')],[7, 1, read('HomepagePRESSURE_HUMIDITY')],[7, 2, read('HomepageTEMPERATURE_HUMIDITY')],[7, 3, read('HomepageROUND0_HUMIDITY')],[7, 4, read('HomepageROUND1_HUMIDITY')],[7, 5, read('HomepageWINDSPEED_HUMIDITY')],[7, 6, read('HomepageWINDDIRECTION_HUMIDITY')],[7,7,1]]
      .map(function (item) {
        return [item[1], item[0], item[2] || '-'];
      });
  onMounted(()=>{
    var myChart = echarts.init(chart3.value);
    var option = {
      tooltip: {
        position: 'top'
      },
      grid: {
        height: '50%',
        top: '10%'
      },
      xAxis: {
        type: 'category',
        data: hours,
        splitArea: {
          show: true
        }
      },
      yAxis: {
        type: 'category',
        data: days,
        splitArea: {
          show: true
        }
      },
      visualMap: {
        min: -1,
        max: 1,
        calculable: true,
        orient: 'horizontal',
        left: 'center',
        bottom: '15%'
      },
      series: [
        {
          name: 'Punch Card',
          type: 'heatmap',
          data: data,
          label: {
            show: true
          },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    }
    option && myChart.setOption(option);
  })

  // DBar start
  //  三维柱状图
  onMounted(()=>{
    var DBarChart = echarts.init(chart7.value);
// prettier-ignore
    var DBarChartX = read('HomepageDATATIME');
// prettier-ignore
//     var DBarChartY = ['PREPOWER', 'PRESSURE', 'TEMPERATURE','HUMIDITY', 'ROUND0', 'ROUND1', 'WINDSPEED', 'WINDDIRECTION', 'YD15'];
    var DBarChartY = ['PREPOWER', 'ROUND0', 'YD15'];
//     var DBarChartY = [ 'YD15'];
    // prettier-ignore[Y,X,Z]
    var data = [];
    var i,j,DBarChartYMax,DBarChartYMin;
    for (i of DBarChartY){
      console.log(i)
          var temp = read('Homepage'+i)
      DBarChartYMax = Math.max.apply(DBarChartYMax, temp);
      DBarChartYMin = Math.min.apply(DBarChartYMin, temp);
      // console.log(temp)
      for(j=0; j<temp.length; j++){
        // console.log(read('Homepage'+i)[j])
            data.push([DBarChartY.indexOf(i),j,temp[j]])
          }
    }
    // console.log(data)
    var option = {
      tooltip: {},
      visualMap: {
        max: DBarChartYMax,
        min: DBarChartYMin,
        inRange: {
          color: [
            '#313695',
            '#4575b4',
            '#74add1',
            '#abd9e9',
            '#e0f3f8',
            '#ffffbf',
            '#fee090',
            '#fdae61',
            '#f46d43',
            '#d73027',
            '#a50026'
          ]
        }
      },
      xAxis3D: {
        type: 'category',
        data: DBarChartX
      },
      yAxis3D: {
        type: 'category',
        data:  ['PREPOWER', 'ROUND0', 'YD15']
      },
      zAxis3D: {
        type: 'value'
      },
      grid3D: {
        boxWidth: 200,
        boxDepth: 80,
        viewControl: {
          // projection: 'orthographic'
        },
        light: {
          main: {
            intensity: 1.2,
            shadow: true
          },
          ambient: {
            intensity: 0.3
          }
        }
      },
      series: [
        {
          type: 'bar3D',
          data: data.map(function (item) {
            return {
              value: [item[1], item[0], item[2]]
            };
          }),
          shading: 'lambert',
          label: {
            fontSize: 16,
            borderWidth: 1
          },
          emphasis: {
            label: {
              fontSize: 20,
              color: '#900'
            },
            itemStyle: {
              color: '#900'
            }
          }
        }
      ]
    };
    option && DBarChart.setOption(option);
  })
  // DBar end
}else{ // 没有数据就用预设数据
       // 各参数变化情况
    onMounted(()=>{
    var myChart = echarts.init(chart1.value);
    var option = {
      title: {
        text: '各参数变化情况'
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
        boundaryGap: false,
        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          formatter: '{value}'
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
          name: 'WINDSPEED',
          type: 'line',
          data: [4.2,4.3,4.2,4.3,4.3,4.3,4.3],
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
        {
          name: 'PREPOWER',
          type: 'line',
          data: [8432,8177,7959,7740,7522,7267,6974],
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
          },
        {
          name: 'TEMPERATURE',
          type: 'line',
          data: [-5.9,-5.9,-6,-6,-6.1,-6.1,-6.2],
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
        {
          name: 'PRESSURE',
          type: 'line',
          data: [1014,1014,1014,1014,1014,1014,1014],
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        }
      ]
    };

    option && myChart.setOption(option);
    })
  // 箱线图
    onMounted(()=>{
    var myChart = echarts.init(chart2.value);
    var option = {
        title: [
        {
          text: '各参数箱线图',
          left: 'center'
        },
      ],
      dataset: [
        {
          // prettier-ignore
          source: [
                    [850, 740, 900, 1070, 930, 850, 950, 980, 980, 880, 1000, 980, 930, 650, 760, 810, 1000, 1000, 960, 960],
                    [960, 940, 960, 940, 880, 800, 850, 880, 900, 840, 830, 790, 810, 880, 880, 830, 800, 790, 760, 800],
                    [880, 880, 880, 860, 720, 720, 620, 860, 970, 950, 880, 910, 850, 870, 840, 840, 850, 840, 840, 840],
                    [890, 810, 810, 820, 800, 770, 760, 740, 750, 760, 910, 920, 890, 860, 880, 720, 840, 850, 850, 780],
                   ]
        },
        {
          transform: {
            type: 'boxplot',
            config: {
              itemNameFormatter: function (params) {
                return ['WINDSPEED','PREPOWER','TEMPERATURE','PRESSURE'][params.value];
              }
            }
          }
        },
        {
          fromDatasetIndex: 1,
          fromTransformResult: 1
        }
      ],
      tooltip: {
        trigger: 'item',
        axisPointer: {
          type: 'shadow'
        }
      },
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
      grid: {
        left: '10%',
        right: '10%',
        bottom: '15%'
      },
      yAxis: {
        type: 'category',
        boundaryGap: true,
        nameGap: 30,
        splitArea: {
          show: false
        },
        splitLine: {
          show: false
        }
      },
      xAxis: {
        type: 'value',
        // name: 'km/s minus 299,000',
        splitArea: {
          show: true
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
          name: 'boxplot',
          type: 'boxplot',
          datasetIndex: 1
        },
        {
          name: 'outlier',
          type: 'scatter',
          encode: { x: 1, y: 0 },
          datasetIndex: 2
        }
      ]
    };

    option && myChart.setOption(option);
    })
  // 热力图
    const hours = [
        '12a', '1a', '2a', '3a', '4a', '5a', '6a',
        '7a', '8a', '9a', '10a', '11a',
        '12p', '1p', '2p', '3p', '4p', '5p',
        '6p', '7p', '8p', '9p', '10p', '11p'
    ];
    const days = [
        'Saturday', 'Friday', 'Thursday',
        'Wednesday', 'Tuesday', 'Monday', 'Sunday'
    ];
    const data = [[0, 0, 5], [0, 1, 1], [0, 2, 0], [0, 3, 0], [0, 4, 0], [0, 5, 0], [0, 6, 0], [0, 7, 0], [0, 8, 0], [0, 9, 0], [0, 10, 0], [0, 11, 2], [0, 12, 4], [0, 13, 1], [0, 14, 1], [0, 15, 3], [0, 16, 4], [0, 17, 6], [0, 18, 4], [0, 19, 4], [0, 20, 3], [0, 21, 3], [0, 22, 2], [0, 23, 5], [1, 0, 7], [1, 1, 0], [1, 2, 0], [1, 3, 0], [1, 4, 0], [1, 5, 0], [1, 6, 0], [1, 7, 0], [1, 8, 0], [1, 9, 0], [1, 10, 5], [1, 11, 2], [1, 12, 2], [1, 13, 6], [1, 14, 9], [1, 15, 11], [1, 16, 6], [1, 17, 7], [1, 18, 8], [1, 19, 12], [1, 20, 5], [1, 21, 5], [1, 22, 7], [1, 23, 2], [2, 0, 1], [2, 1, 1], [2, 2, 0], [2, 3, 0], [2, 4, 0], [2, 5, 0], [2, 6, 0], [2, 7, 0], [2, 8, 0], [2, 9, 0], [2, 10, 3], [2, 11, 2], [2, 12, 1], [2, 13, 9], [2, 14, 8], [2, 15, 10], [2, 16, 6], [2, 17, 5], [2, 18, 5], [2, 19, 5], [2, 20, 7], [2, 21, 4], [2, 22, 2], [2, 23, 4], [3, 0, 7], [3, 1, 3], [3, 2, 0], [3, 3, 0], [3, 4, 0], [3, 5, 0], [3, 6, 0], [3, 7, 0], [3, 8, 1], [3, 9, 0], [3, 10, 5], [3, 11, 4], [3, 12, 7], [3, 13, 14], [3, 14, 13], [3, 15, 12], [3, 16, 9], [3, 17, 5], [3, 18, 5], [3, 19, 10], [3, 20, 6], [3, 21, 4], [3, 22, 4], [3, 23, 1], [4, 0, 1], [4, 1, 3], [4, 2, 0], [4, 3, 0], [4, 4, 0], [4, 5, 1], [4, 6, 0], [4, 7, 0], [4, 8, 0], [4, 9, 2], [4, 10, 4], [4, 11, 4], [4, 12, 2], [4, 13, 4], [4, 14, 4], [4, 15, 14], [4, 16, 12], [4, 17, 1], [4, 18, 8], [4, 19, 5], [4, 20, 3], [4, 21, 7], [4, 22, 3], [4, 23, 0], [5, 0, 2], [5, 1, 1], [5, 2, 0], [5, 3, 3], [5, 4, 0], [5, 5, 0], [5, 6, 0], [5, 7, 0], [5, 8, 2], [5, 9, 0], [5, 10, 4], [5, 11, 1], [5, 12, 5], [5, 13, 10], [5, 14, 5], [5, 15, 7], [5, 16, 11], [5, 17, 6], [5, 18, 0], [5, 19, 5], [5, 20, 3], [5, 21, 4], [5, 22, 2], [5, 23, 0], [6, 0, 1], [6, 1, 0], [6, 2, 0], [6, 3, 0], [6, 4, 0], [6, 5, 0], [6, 6, 0], [6, 7, 0], [6, 8, 0], [6, 9, 0], [6, 10, 1], [6, 11, 0], [6, 12, 2], [6, 13, 1], [6, 14, 3], [6, 15, 4], [6, 16, 0], [6, 17, 0], [6, 18, 0], [6, 19, 0], [6, 20, 1], [6, 21, 2], [6, 22, 2], [6, 23, 6]]
        .map(function (item) {
        return [item[1], item[0], item[2] || '-'];
    });
    onMounted(()=>{
    var myChart = echarts.init(chart3.value);
    var option = {
        tooltip: {
        position: 'top'
      },
      grid: {
        height: '50%',
        top: '10%'
      },
      xAxis: {
        type: 'category',
        data: hours,
        splitArea: {
          show: true
        }
      },
      yAxis: {
        type: 'category',
        data: days,
        splitArea: {
          show: true
        }
      },
      visualMap: {
        min: 0,
        max: 10,
        calculable: true,
        orient: 'horizontal',
        left: 'center',
        bottom: '15%'
      },
      series: [
        {
          name: 'Punch Card',
          type: 'heatmap',
          data: data,
          label: {
            show: true
          },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    }
    option && myChart.setOption(option);
    })


  // DBar start
//  三维柱状图
  onMounted(()=>{
    var DBarChart = echarts.init(chart7.value);
// prettier-ignore
    var DBarChartX = ['12a', '1a', '2a', '3a', '4a', '5a', '6a',
      '7a', '8a', '9a', '10a', '11a',
      '12p', '1p', '2p', '3p', '4p', '5p',
      '6p', '7p', '8p', '9p', '10p', '11p'];
// prettier-ignore
    var DBarChartY = ['Saturday', 'Friday', 'Thursday',
      'Wednesday', 'Tuesday', 'Monday', 'Sunday'];
// prettier-ignore[Y,X,Z]
    var data = [
        [0, 0, .5], [0, 1, 1], [0, 2, 0], [0, 3, 0], [0, 4, 0], [0, 5, 0], [0, 6, 0], [0, 7, 0],
        [0, 8, 0], [0, 9, 0], [0, 10, 0], [0, 11, 2], [0, 12, 4], [0, 13, 1], [0, 14, 1], [0, 15, 3],
      [0, 16, 4], [0, 17, 6], [0, 18, 4], [0, 19, 4], [0, 20, 3], [0, 21, 3], [0, 22, 2], [0, 23, 5],
      [1, 0, 7], [1, 1, 0], [1, 2, 0], [1, 3, 0], [1, 4, 0], [1, 5, 0], [1, 6, 0], [1, 7, 0], [1, 8, 0], [1, 9, 0], [1, 10, 5], [1, 11, 2], [1, 12, 2], [1, 13, 6], [1, 14, 9], [1, 15, 11], [1, 16, 6], [1, 17, 7], [1, 18, 8], [1, 19, 12], [1, 20, 5], [1, 21, 5], [1, 22, 7], [1, 23, 2], [2, 0, 1], [2, 1, 1], [2, 2, 0], [2, 3, 0], [2, 4, 0], [2, 5, 0], [2, 6, 0], [2, 7, 0], [2, 8, 0], [2, 9, 0], [2, 10, 3], [2, 11, 2], [2, 12, 1], [2, 13, 9], [2, 14, 8], [2, 15, 10], [2, 16, 6], [2, 17, 5], [2, 18, 5], [2, 19, 5], [2, 20, 7], [2, 21, 4], [2, 22, 2], [2, 23, 4], [3, 0, 7], [3, 1, 3], [3, 2, 0], [3, 3, 0], [3, 4, 0], [3, 5, 0], [3, 6, 0], [3, 7, 0], [3, 8, 1], [3, 9, 0], [3, 10, 5], [3, 11, 4], [3, 12, 7], [3, 13, 14], [3, 14, 13], [3, 15, 12], [3, 16, 9], [3, 17, 5], [3, 18, 5], [3, 19, 10], [3, 20, 6], [3, 21, 4], [3, 22, 4], [3, 23, 1], [4, 0, 1], [4, 1, 3], [4, 2, 0], [4, 3, 0], [4, 4, 0], [4, 5, 1], [4, 6, 0], [4, 7, 0], [4, 8, 0], [4, 9, 2], [4, 10, 4], [4, 11, 4], [4, 12, 2], [4, 13, 4], [4, 14, 4], [4, 15, 14], [4, 16, 12], [4, 17, 1], [4, 18, 8], [4, 19, 5], [4, 20, 3], [4, 21, 7], [4, 22, 3], [4, 23, 0], [5, 0, 2], [5, 1, 1], [5, 2, 0], [5, 3, 3], [5, 4, 0], [5, 5, 0], [5, 6, 0], [5, 7, 0], [5, 8, 2], [5, 9, 0], [5, 10, 4], [5, 11, 1], [5, 12, 5], [5, 13, 10], [5, 14, 5], [5, 15, 7], [5, 16, 11], [5, 17, 6], [5, 18, 0], [5, 19, 5], [5, 20, 3], [5, 21, 4], [5, 22, 2], [5, 23, 0], [6, 0, 1], [6, 1, 0], [6, 2, 0], [6, 3, 0], [6, 4, 0], [6, 5, 0], [6, 6, 0], [6, 7, 0], [6, 8, 0], [6, 9, 0], [6, 10, 1], [6, 11, 0], [6, 12, 2], [6, 13, 1], [6, 14, 3], [6, 15, 4], [6, 16, 0], [6, 17, 0], [6, 18, 0], [6, 19, 0], [6, 20, 1], [6, 21, 2], [6, 22, 2], [6, 23, 6]];
    var option = {
      tooltip: {},
      visualMap: {
        max: 20,
        inRange: {
          color: [
            '#313695',
            '#4575b4',
            '#74add1',
            '#abd9e9',
            '#e0f3f8',
            '#ffffbf',
            '#fee090',
            '#fdae61',
            '#f46d43',
            '#d73027',
            '#a50026'
          ]
        }
      },
      xAxis3D: {
        type: 'category',
        data: DBarChartX
      },
      yAxis3D: {
        type: 'category',
        data: DBarChartY
      },
      zAxis3D: {
        type: 'value'
      },
      grid3D: {
        boxWidth: 200,
        boxDepth: 80,
        viewControl: {
          // projection: 'orthographic'
        },
        light: {
          main: {
            intensity: 1.2,
            shadow: true
          },
          ambient: {
            intensity: 0.3
          }
        }
      },
      series: [
        {
          type: 'bar3D',
          data: data.map(function (item) {
            return {
              value: [item[1], item[0], item[2]]
            };
          }),
          shading: 'lambert',
          label: {
            fontSize: 16,
            borderWidth: 1
          },
          emphasis: {
            label: {
              fontSize: 20,
              color: '#900'
            },
            itemStyle: {
              color: '#900'
            }
          }
        }
      ]
    };
    option && DBarChart.setOption(option);
  })
  // DBar end
}





// 提供给Dropdown组件使用的数据
const selectedfjs = ref([
  { name: '1号风机', code: '1' },
  { name: '2号风机', code: '2' },
  { name: '3号风机', code: '3' },
  { name: '4号风机', code: '4' },
  { name: '5号风机', code: '5' },
  { name: '6号风机', code: '6' },
  { name: '7号风机', code: '7' },
  { name: '8号风机', code: '8' },
  { name: '9号风机', code: '9' },
  { name: '10号风机', code: '10' },
  { name: '11号风机', code: '11' },
  { name: '12号风机', code: '12' },
  { name: '13号风机', code: '13' },
  { name: '14号风机', code: '14' },
  { name: '15号风机', code: '15' },
  { name: '16号风机', code: '16' },
  { name: '17号风机', code: '17' },
  { name: '18号风机', code: '18' },
  { name: '19号风机', code: '19' },
  { name: '20号风机', code: '20' }
]);
const selectedfj = ref(null);

// 获取选择的风机代号，并打印
// const getSelectedfj = () => {
//   console.log(selectedfj.value);
//   // console.log(selectedfj.value.code);
// };

// 根据风机代号发送请求到后端获取数据信息
const onSelect = () => {
  const fj = selectedfj.value;
  function show(cfg){
    swal({
      closeOnClickOutside: false,
      closeOnEsc: false,
      // 解构cfg对象，展开cfg对象所有属性
      ...cfg
    })
  }
  function pearson(a, b) {
    var n = a.length;
    if (n !== b.length) {
      throw new Error('两组数据的个数不相等');
    }
    var i;
    var sqSumA = 0;
    var sqSumB = 0;
    var pSum = 0;
    var sumA = 0;
    var sumB = 0;
    for (i = 0; i < n; i++) {
      sumA += a[i];
      sumB += b[i];
      sqSumA += Math.pow(a[i], 2);
      sqSumB += Math.pow(b[i], 2);
      pSum += a[i] * b[i];
    }
    var numerator = pSum - (sumA * sumB) / n;
    var denominator = Math.sqrt(
        (sqSumA - Math.pow(sumA, 2) / n) * (sqSumB - Math.pow(sumB, 2) / n)
    );
    if (denominator === 0) {
      return 0;
    } else {
      return numerator / denominator;
    }
  }
  if (fj) {
    console.log(fj);
    const Home_usn = fj.code;
    localStorage.setItem("Home_usn", Home_usn);
    let usn = Home_usn;
    axios.post('http://81.70.183.201:5000/getdata', {
      usn
    }).then(res => {
      const ret = res.data
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
        // console.log(ret.datacorr);
        var HomepageDATATIME = ret.data["DATATIME"];
        var HomepagePREPOWER = ret.data["PREPOWER"];
        var HomepagePRESSURE = ret.data["PRESSURE"];
        var HomepageTEMPERATURE = ret.data["TEMPERATURE"];
        var HomepageHUMIDITY = ret.data["HUMIDITY"];
        var HomepageROUND0 = ret.data["ROUND(A.POWER,0)"];
        var HomepageROUND1 = ret.data["ROUND(A.WS,1)"];
        var HomepageWINDSPEED = ret.data["WINDSPEED"];
        var HomepageWINDDIRECTION = ret.data["WINDDIRECTION"];
        var HomepageYD15 = ret.data["YD15"];
        // 计算上面变量的相关系数
        var HomepagePREPOWER_PRESURE = Math.round(10000 * pearson(HomepagePREPOWER, HomepagePRESSURE)) / 10000;
        var HomepagePREPOWER_TEMPERATURE = Math.round(10000 * pearson(HomepagePREPOWER, HomepageTEMPERATURE)) / 10000;
        var HomepagePREPOWER_ROUND0 = Math.round(10000 * pearson(HomepagePREPOWER, HomepageROUND0)) / 10000;
        var HomepagePREPOWER_ROUND1 = Math.round(10000 * pearson(HomepagePREPOWER, HomepageROUND1)) / 10000;
        var HomepagePREPOWER_HUMIDITY = Math.round(10000 * pearson(HomepagePREPOWER, HomepageHUMIDITY)) / 10000;
        var HomepagePREPOWER_WINDSPEED = Math.round(10000 * pearson(HomepagePREPOWER, HomepageWINDSPEED)) / 10000;
        var HomepagePREPOWER_WINDDIRECTION = Math.round(10000 * pearson(HomepagePREPOWER, HomepageWINDDIRECTION)) / 10000;

        var HomepagePRESSURE_TEMPERATURE = Math.round(10000 * pearson(HomepagePRESSURE, HomepageTEMPERATURE)) / 10000;
        var HomepagePRESSURE_ROUND0 = Math.round(10000 * pearson(HomepagePRESSURE, HomepageROUND0)) / 10000;
        var HomepagePRESSURE_ROUND1 = Math.round(10000 * pearson(HomepagePRESSURE, HomepageROUND1)) / 10000;
        var HomepagePRESSURE_HUMIDITY = Math.round(10000 * pearson(HomepagePRESSURE, HomepageHUMIDITY)) / 10000;
        var HomepagePRESSURE_WINDSPEED = Math.round(10000 * pearson(HomepagePRESSURE, HomepageWINDSPEED)) / 10000;
        var HomepagePRESSURE_WINDDIRECTION = Math.round(10000 * pearson(HomepagePRESSURE, HomepageWINDDIRECTION)) / 10000;

        var HomepageTEMPERATURE_ROUND0 = Math.round(10000 * pearson(HomepageTEMPERATURE, HomepageROUND0)) / 10000;
        var HomepageTEMPERATURE_ROUND1 = Math.round(10000 * pearson(HomepageTEMPERATURE, HomepageROUND1)) / 10000;
        var HomepageTEMPERATURE_WINDSPEED = Math.round(10000 * pearson(HomepageTEMPERATURE, HomepageWINDSPEED)) / 10000;
        var HomepageTEMPERATURE_WINDDIRECTION = Math.round(10000 * pearson(HomepageTEMPERATURE, HomepageWINDDIRECTION)) / 10000;
        var HomepageTEMPERATURE_HUMIDITY = Math.round(10000 * pearson(HomepageTEMPERATURE, HomepageHUMIDITY)) / 10000;

        var HomepageROUND0_ROUND1 = Math.round(10000 * pearson(HomepageROUND0, HomepageROUND1)) / 10000;
        var HomepageROUND0_WINDSPEED = Math.round(10000 * pearson(HomepageROUND0, HomepageWINDSPEED)) / 10000;
        var HomepageROUND0_WINDDIRECTION = Math.round(10000 * pearson(HomepageROUND0, HomepageWINDDIRECTION)) / 10000;
        var HomepageROUND0_HUMIDITY = Math.round(10000 * pearson(HomepageROUND0, HomepageHUMIDITY)) / 10000;

        var HomepageROUND1_WINDSPEED = Math.round(10000 * pearson(HomepageROUND1, HomepageWINDSPEED)) / 10000;
        var HomepageROUND1_WINDDIRECTION = Math.round(10000 * pearson(HomepageROUND1, HomepageWINDDIRECTION)) / 10000;
        var HomepageROUND1_HUMIDITY = Math.round(10000 * pearson(HomepageROUND1, HomepageHUMIDITY)) / 10000;

        var HomepageWINDSPEED_WINDDIRECTION = Math.round(10000 * pearson(HomepageWINDSPEED, HomepageWINDDIRECTION)) / 10000;
        var HomepageWINDSPEED_HUMIDITY = Math.round(10000 * pearson(HomepageWINDSPEED, HomepageHUMIDITY)) / 10000;

        var HomepageWINDDIRECTION_HUMIDITY = Math.round(10000 * pearson(HomepageWINDDIRECTION, HomepageHUMIDITY)) / 10000;

        var save = function (name,arr) {
          localStorage.setItem(name,JSON.stringify(arr))
        }
        // 先判断本地是否有数据，有的话就先删除再存储
        if (localStorage.getItem("HomepageDATATIME")){
          localStorage.removeItem("HomepageDATATIME");
          localStorage.removeItem("HomepagePREPOWER");
          localStorage.removeItem("HomepagePRESSURE");
          localStorage.removeItem("HomepageHUMIDITY");
          localStorage.removeItem("HomepageYD15");
          localStorage.removeItem("HomepageTEMPERATURE");
          localStorage.removeItem("HomepageROUND0");
          localStorage.removeItem("HomepageROUND1");
          localStorage.removeItem("HomepageWINDSPEED");
          localStorage.removeItem("HomepageWINDDIRECTION");

          localStorage.removeItem("HomepagePREPOWER_PRESURE");
          localStorage.removeItem("HomepagePREPOWER_HUMIDITY");
          localStorage.removeItem("HomepagePREPOWER_TEMPERATURE");
          localStorage.removeItem("HomepagePREPOWER_ROUND0");
          localStorage.removeItem("HomepagePREPOWER_ROUND1");
          localStorage.removeItem("HomepagePREPOWER_WINDSPEED");
          localStorage.removeItem("HomepagePREPOWER_WINDDIRECTION");
          localStorage.removeItem("HomepagePREPOWER_HUMIDITY");

          localStorage.removeItem("HomepagePRESSURE_TEMPERATURE");
          localStorage.removeItem("HomepagePRESSURE_ROUND0");
          localStorage.removeItem("HomepagePRESSURE_ROUND1");
          localStorage.removeItem("HomepagePRESSURE_WINDSPEED");
          localStorage.removeItem("HomepagePRESSURE_WINDDIRECTION");
          localStorage.removeItem("HomepagePRESSURE_HUMIDITY");

          localStorage.removeItem("HomepageTEMPERATURE_ROUND0");
          localStorage.removeItem("HomepageTEMPERATURE_ROUND1");
          localStorage.removeItem("HomepageTEMPERATURE_WINDSPEED");
          localStorage.removeItem("HomepageTEMPERATURE_WINDDIRECTION");
          localStorage.removeItem("HomepageTEMPERATURE_HUMIDITY");

          localStorage.removeItem("HomepageROUND0_ROUND1");
          localStorage.removeItem("HomepageROUND0_WINDSPEED");
          localStorage.removeItem("HomepageROUND0_WINDDIRECTION");
          localStorage.removeItem("HomepageROUND0_HUMIDITY");

          localStorage.removeItem("HomepageROUND1_WINDSPEED");
          localStorage.removeItem("HomepageROUND1_WINDDIRECTION");
          localStorage.removeItem("HomepageROUND1_HUMIDITY");

          localStorage.removeItem("HomepageWINDSPEED_WINDDIRECTION");
          localStorage.removeItem("HomepageWINDSPEED_HUMIDITY");

          localStorage.removeItem("HomepageWINDDIRECTION_HUMIDITY");
        }
        save("HomepageDATATIME",HomepageDATATIME);
        save("HomepagePREPOWER",HomepagePREPOWER);
        save("HomepagePRESSURE",HomepagePRESSURE);
        save("HomepageTEMPERATURE",HomepageTEMPERATURE);
        save("HomepageROUND0",HomepageROUND0);
        save("HomepageROUND1",HomepageROUND1);
        save("HomepageWINDSPEED",HomepageWINDSPEED);
        save("HomepageWINDDIRECTION",HomepageWINDDIRECTION);
        save("HomepageHUMIDITY",HomepageHUMIDITY);
        save("HomepageYD15",HomepageYD15);

        save("HomepagePREPOWER_PRESURE",HomepagePREPOWER_PRESURE);
        save("HomepagePREPOWER_TEMPERATURE",HomepagePREPOWER_TEMPERATURE);
        save("HomepagePREPOWER_ROUND0",HomepagePREPOWER_ROUND0);
        save("HomepagePREPOWER_ROUND1",HomepagePREPOWER_ROUND1);
        save("HomepagePREPOWER_WINDSPEED",HomepagePREPOWER_WINDSPEED);
        save("HomepagePREPOWER_WINDDIRECTION",HomepagePREPOWER_WINDDIRECTION);
        save("HomepagePREPOWER_HUMIDITY",HomepagePREPOWER_HUMIDITY);

        save("HomepagePRESSURE_TEMPERATURE",HomepagePRESSURE_TEMPERATURE);
        save("HomepagePRESSURE_ROUND0",HomepagePRESSURE_ROUND0);
        save("HomepagePRESSURE_ROUND1",HomepagePRESSURE_ROUND1);
        save("HomepagePRESSURE_WINDSPEED",HomepagePRESSURE_WINDSPEED);
        save("HomepagePRESSURE_WINDDIRECTION",HomepagePRESSURE_WINDDIRECTION);
        save("HomepagePRESSURE_HUMIDITY",HomepagePRESSURE_HUMIDITY);

        save("HomepageTEMPERATURE_ROUND0",HomepageTEMPERATURE_ROUND0);
        save("HomepageTEMPERATURE_ROUND1",HomepageTEMPERATURE_ROUND1);
        save("HomepageTEMPERATURE_WINDSPEED",HomepageTEMPERATURE_WINDSPEED);
        save("HomepageTEMPERATURE_WINDDIRECTION",HomepageTEMPERATURE_WINDDIRECTION);
        save("HomepageTEMPERATURE_HUMIDITY",HomepageTEMPERATURE_HUMIDITY);

        save("HomepageROUND0_ROUND1",HomepageROUND0_ROUND1);
        save("HomepageROUND0_WINDSPEED",HomepageROUND0_WINDSPEED);
        save("HomepageROUND0_WINDDIRECTION",HomepageROUND0_WINDDIRECTION);
        save("HomepageROUND0_HUMIDITY",HomepageROUND0_HUMIDITY);

        save("HomepageROUND1_WINDSPEED",HomepageROUND1_WINDSPEED);
        save("HomepageROUND1_WINDDIRECTION",HomepageROUND1_WINDDIRECTION);
        save("HomepageROUND1_HUMIDITY",HomepageROUND1_HUMIDITY);

        save("HomepageWINDSPEED_WINDDIRECTION",HomepageWINDSPEED_WINDDIRECTION);
        save("HomepageWINDSPEED_HUMIDITY",HomepageWINDSPEED_HUMIDITY);

        save("HomepageWINDDIRECTION_HUMIDITY",HomepageWINDDIRECTION_HUMIDITY);
      }
    }).catch(err => {
      console.log(err);
    });
  }else {
    show({
      title: '错误',
      text: "请先选择风机",
      icon: 'error',
      button: {
        text: '好的'
      }
    })
  }

  // 各参数变化情况
  {
    var myChart = echarts.init(chart1.value);
    var option = {
      title: {
        text: '各参数变化情况'
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
        boundaryGap: false,
        data: read('HomepageDATATIME')
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          formatter: '{value}'
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
          name: 'PREPOWER',
          type: 'line',
          data: read('HomepagePREPOWER'),
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
        {
          name: 'PRESSURE',
          type: 'line',
          data: read('HomepagePRESSURE'),
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
        {
          name: 'ROUND(A.POWER,0)',
          type: 'line',
          data: read('HomepageROUND0'),
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
        {
          name: 'YD15',
          type: 'line',
          data: read('HomepageYD15'),
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
      ]
    };

    option && myChart.setOption(option);
  }
  {
    myChart = echarts.init(chart6.value);
    option = {
      title: {
        text: '各参数变化情况'
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
        boundaryGap: false,
        data: read('HomepageDATATIME')
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          formatter: '{value}'
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
          name: 'WINDSPEED',
          type: 'line',
          data: read('HomepageWINDSPEED'),
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
        {
          name: 'TEMPERATURE',
          type: 'line',
          data: read('HomepageTEMPERATURE'),
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
        {
          name: 'WINDDIRECTION',
          type: 'line',
          data: read('HomepageWINDDIRECTION'),
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
        {
          name: 'HUMIDITY',
          type: 'line',
          data: read('HomepageHUMIDITY'),
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
        {
          name: 'ROUND(A.WS,1)',
          type: 'line',
          data: read('HomepageROUND1'),
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
        },
      ]
    };

    option && myChart.setOption(option);
  }
  // 箱线图
  {
    var myChart = echarts.init(chart2.value);
    var option = {
      title: [
        {
          text: '各参数箱线图',
          left: 'center'
        },
      ],
      dataset: [
        {
          // prettier-ignore
          source: [
            read('HomepageWINDSPEED'),
            read('HomepageWINDDIRECTION'),
            read('HomepagePREPOWER'),
            read('HomepageTEMPERATURE'),
            read('HomepagePRESSURE'),
            read('HomepageHUMIDITY'),
            read('HomepageROUND0'),
            read('HomepageROUND1'),
            read('HomepageYD15'),
          ]
        },
        {
          transform: {
            type: 'boxplot',
            config: {
              itemNameFormatter: function (params) {
                return ['WINDSPEED','WINDDIRECTION','PREPOWER','TEMPERATURE','PRESSURE','HUMIDITY','ROUND0','ROUND1','YD15'][params.value];
              }
            }
          }
        },
        {
          fromDatasetIndex: 1,
          fromTransformResult: 1
        }
      ],
      tooltip: {
        trigger: 'item',
        axisPointer: {
          type: 'shadow'
        }
      },
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
      grid: {
        left: '10%',
        right: '10%',
        bottom: '15%'
      },
      yAxis: {
        type: 'category',
        boundaryGap: true,
        nameGap: 30,
        splitArea: {
          show: false
        },
        splitLine: {
          show: false
        }
      },
      xAxis: {
        type: 'value',
        // name: 'km/s minus 299,000',
        splitArea: {
          show: true
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
          name: 'boxplot',
          type: 'boxplot',
          datasetIndex: 1
        },
        {
          name: 'outlier',
          type: 'scatter',
          encode: { x: 1, y: 0 },
          datasetIndex: 2
        }
      ]
    };

    option && myChart.setOption(option);
  }
  // 热力图
  const hours = [
    'PREPOWER','PRESSURE','TEMPERATURE','ROUND(A.POWER,0)','ROUND(A.WS,1)','WINDSPEED','WINDDIRECTION'
  ];
  const days = [
    'PREPOWER','PRESSURE','TEMPERATURE','ROUND(A.POWER,0)','ROUND(A.WS,1)','WINDSPEED','WINDDIRECTION','HUMIDITY'
  ];
  const data = [
    [0, 0, 1], [0, 1, read('HomepagePREPOWER_PRESURE')], [0, 2, read('HomepagePREPOWER_TEMPERATURE')], [0, 3, read('HomepagePREPOWER_ROUND0')], [0, 4, read('HomepagePREPOWER_ROUND1')], [0, 5, read('HomepagePREPOWER_WINDSPEED')], [0, 6, read('HomepagePREPOWER_WINDDIRECTION')],[0, 7, read('HomepagePREPOWER_HUMIDITY')],
    [1, 0, read('HomepagePREPOWER_PRESURE')], [1, 1, 1], [1, 2,  read('HomepagePRESSURE_ROUND0')], [1, 3, read('HomepagePRESSURE_ROUND0')], [1, 4, read('HomepagePRESSURE_ROUND1')], [1, 5, read('HomepagePRESSURE_WINDSPEED')], [1, 6, read('HomepagePRESSURE_WINDDIRECTION')],[7, 1, read('HomepagePRESSURE_HUMIDITY')],
    [2, 0, read('HomepagePREPOWER_TEMPERATURE')], [2, 1,  read('HomepagePRESSURE_TEMPERATURE')], [2, 2, 1], [2, 3, read('HomepageTEMPERATURE_ROUND0')], [2, 4, read('HomepageTEMPERATURE_ROUND1')], [2, 5, read('HomepageTEMPERATURE_WINDSPEED')], [2, 6, read('HomepageTEMPERATURE_WINDDIRECTION')],[2, 7, read('HomepageTEMPERATURE_HUMIDITY')],
    [3, 0, read('HomepagePREPOWER_ROUND0')], [3, 1,  read('HomepagePRESSURE_ROUND0')], [3, 2, read('HomepageTEMPERATURE_ROUND0')], [3, 3, 1], [3, 4, read('HomepageROUND0_ROUND1')], [3, 5, read('HomepageROUND0_WINDSPEED')], [3, 6, read('HomepageROUND0_WINDDIRECTION')],[3, 7, read('HomepageROUND0_HUMIDITY')],
    [4, 0, read('HomepagePREPOWER_ROUND1')], [4, 1,  read('HomepagePRESSURE_ROUND1')], [4, 2, read('HomepageTEMPERATURE_ROUND1')], [4, 3, read('HomepageROUND0_ROUND1')], [4, 4, 1], [4, 5, read('HomepageROUND1_WINDSPEED')], [4, 6, read('HomepageROUND1_WINDDIRECTION')],[4, 7, read('HomepageROUND1_HUMIDITY')],
    [5, 0, read('HomepagePREPOWER_WINDSPEED')], [5, 1,  read('HomepagePRESSURE_WINDSPEED')], [5, 2, read('HomepageTEMPERATURE_WINDSPEED')], [5, 3, read('HomepageROUND0_WINDSPEED')], [5, 4, read('HomepageROUND1_WINDSPEED')], [5, 5, 1], [5, 6, read('HomepageWINDSPEED_WINDDIRECTION')],[5, 7, read('HomepageWINDSPEED_HUMIDITY')],
    [6, 0, read('HomepagePREPOWER_WINDDIRECTION')], [6,  1, read('HomepagePRESSURE_WINDDIRECTION')], [6, 2, read('HomepageTEMPERATURE_WINDDIRECTION')], [6, 3, read('HomepageROUND0_WINDDIRECTION')], [6, 4, read('HomepageROUND1_WINDDIRECTION')], [6, 5, read('HomepageWINDSPEED_WINDDIRECTION')], [6,6,1],[6, 7, read('HomepageWINDDIRECTION_HUMIDITY')],
    [7, 0, read('HomepagePREPOWER_HUMIDITY')],[7, 1, read('HomepagePRESSURE_HUMIDITY')],[7, 2, read('HomepageTEMPERATURE_HUMIDITY')],[7, 3, read('HomepageROUND0_HUMIDITY')],[7, 4, read('HomepageROUND1_HUMIDITY')],[7, 5, read('HomepageWINDSPEED_HUMIDITY')],[7, 6, read('HomepageWINDDIRECTION_HUMIDITY')],[7,7,1]]
      .map(function (item) {
        return [item[1], item[0], item[2] || '-'];
      });
  {
    var myChart = echarts.init(chart3.value);
    var option = {
      tooltip: {
        position: 'top'
      },
      grid: {
        height: '50%',
        top: '10%'
      },
      xAxis: {
        type: 'category',
        data: hours,
        splitArea: {
          show: true
        }
      },
      yAxis: {
        type: 'category',
        data: days,
        splitArea: {
          show: true
        }
      },
      visualMap: {
        min: -1,
        max: 1,
        calculable: true,
        orient: 'horizontal',
        left: 'center',
        bottom: '15%'
      },
      series: [
        {
          name: 'Punch Card',
          type: 'heatmap',
          data: data,
          label: {
            show: true
          },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    }
    option && myChart.setOption(option);
  }

  // DBar start
  //  三维柱状图
  {
    var DBarChart = echarts.init(chart7.value);
// prettier-ignore
    var DBarChartX = read('HomepageDATATIME');
// prettier-ignore
//     var DBarChartY = ['PREPOWER', 'PRESSURE', 'TEMPERATURE','HUMIDITY', 'ROUND0', 'ROUND1', 'WINDSPEED', 'WINDDIRECTION', 'YD15'];
    var DBarChartY = ['PREPOWER', 'ROUND0', 'YD15'];
//     var DBarChartY = [ 'YD15'];
    const data = [];
    var i,j,DBarChartYMax,DBarChartYMin;
    for (i of DBarChartY){
      // console.log(i)
      var temp = read('Homepage'+i)
      DBarChartYMax = Math.max.apply(DBarChartYMax, temp);
      DBarChartYMin = Math.min.apply(DBarChartYMin, temp);
      // console.log(temp)
      for(j=0; j<temp.length; j++){
        // console.log(read('Homepage'+i)[j])
        data.push([DBarChartY.indexOf(i),j,temp[j]])
      }
    }
    // console.log(data)


    var option = {
      tooltip: {},
      visualMap: {
        max: DBarChartYMax,
        min: DBarChartYMin,
        inRange: {
          color: [
            '#313695',
            '#4575b4',
            '#74add1',
            '#abd9e9',
            '#e0f3f8',
            '#ffffbf',
            '#fee090',
            '#fdae61',
            '#f46d43',
            '#d73027',
            '#a50026'
          ]
        }
      },
      xAxis3D: {
        type: 'category',
        data: DBarChartX
      },
      yAxis3D: {
        type: 'category',
        data:  ['PREPOWER', 'ROUND0', 'YD15']
      },
      zAxis3D: {
        type: 'value'
      },
      grid3D: {
        boxWidth: 200,
        boxDepth: 80,
        viewControl: {
          // projection: 'orthographic'
        },
        light: {
          main: {
            intensity: 1.2,
            shadow: true
          },
          ambient: {
            intensity: 0.3
          }
        }
      },
      series: [
        {
          type: 'bar3D',
          data: data.map(function (item) {
            return {
              value: [item[1], item[0], item[2]]
            };
          }),
          shading: 'lambert',
          label: {
            fontSize: 16,
            borderWidth: 1
          },
          emphasis: {
            label: {
              fontSize: 20,
              color: '#900'
            },
            itemStyle: {
              color: '#900'
            }
          }
        }
      ]
    };
    option && DBarChart.setOption(option);
  }
  // DBar end
};
// DBar start
const DBar = ref();
// 获取
const UpdateDBar = () => {
  function show(cfg){
    swal({
      closeOnClickOutside: false,
      closeOnEsc: false,
      // 解构cfg对象，展开cfg对象所有属性
      ...cfg
    })
  }
  const Dbarvalue = DBar.value;

  if (Dbarvalue){
    // 将Dbarvalue字典转换为列表
    var DBarChartY = Object.values(Dbarvalue);
    console.log(DBarChartY)
    //  三维柱状图
    {
      var DBarChart = echarts.init(chart7.value);
// prettier-ignore
      var DBarChartX = read('HomepageDATATIME');
      var data = [];
      var i,j,DBarChartYMax,DBarChartYMin;
      for (i of DBarChartY){
        // console.log(i)
        var temp = read('Homepage'+i)
        DBarChartYMax = Math.max.apply(DBarChartYMax, temp);
        DBarChartYMin = Math.min.apply(DBarChartYMin, temp);
        // console.log(temp)
        for(j=0; j<temp.length; j++){
          // console.log(read('Homepage'+i)[j])
          data.push([DBarChartY.indexOf(i),j,temp[j]])
        }
      }
      console.log(data)
      var option = {
        tooltip: {},
        visualMap: {
          max: DBarChartYMax,
          min: DBarChartYMin,
          inRange: {
            color: [
              '#313695',
              '#4575b4',
              '#74add1',
              '#abd9e9',
              '#e0f3f8',
              '#ffffbf',
              '#fee090',
              '#fdae61',
              '#f46d43',
              '#d73027',
              '#a50026'
            ]
          }
        },
        xAxis3D: {
          type: 'category',
          data: DBarChartX
        },
        yAxis3D: {
          type: 'category',
          data:  DBarChartY
        },
        zAxis3D: {
          type: 'value'
        },
        grid3D: {
          boxWidth: 200,
          boxDepth: 80,
          viewControl: {
            // projection: 'orthographic'
          },
          light: {
            main: {
              intensity: 1.2,
              shadow: true
            },
            ambient: {
              intensity: 0.3
            }
          }
        },
        series: [
          {
            type: 'bar3D',
            data: data.map(function (item) {
              return {
                value: [item[1], item[0], item[2]]
              };
            }),
            shading: 'lambert',
            label: {
              fontSize: 16,
              borderWidth: 1
            },
            emphasis: {
              label: {
                fontSize: 20,
                color: '#900'
              },
              itemStyle: {
                color: '#900'
              }
            }
          }
        ]
      };
      option && DBarChart.setOption(option);
    }

  }else {
    show({
      title: '错误',
      text: "请先选择三维柱状图坐标参数",
      icon: 'error',
      button: {
        text: '好的'
      }
    })
  }
};
// DBar end

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

</script>

<template>
<!--   添加div选择风机的选项-->
  <div class="fj-grid" id="Fj">
    <div class="card" id="FjSelect">
      <h5>风机选择</h5>
<!--      使用main.js中的Dropdown来选择1~20号风机-->
<!--令选择框和按钮居中-->
      <div class="p-d-flex p-jc-center">
        <Dropdown v-model="selectedfj"
                  :options="selectedfjs"
                  optionLabel="name"
                  placeholder="请选择一个风机"

        ></Dropdown>
        <!--          令Dropdown与Button在同一行间存在少许间隙-->
        <br>
        <br>
        <Button label="确定" @click="onSelect"></Button>
      </div>
    </div>
</div>

  <div class="grid p-fluid">
    <div class="col-12">
        <div class="card">
          <div ref="chart1" style="width: 1000px; height: 600px;"></div>
        </div>
  </div>

    <div class="col-12">
      <div class="card">
        <div ref="chart6" style="width: 1000px; height: 600px;"></div>
      </div>
    </div>

    <div class="col-12">
        <div class="card">
                <div ref="chart2" style="width: 1000px; height: 600px;"></div>
        </div>
    </div>

    <div class="col-12">
        <div class="card">
            <h5>   热力图   </h5>
                <div ref="chart3" style="width: 1000px; height: 600px;"></div>
        </div>
    </div>


    <!--DBar start-->
    <div class="col-12">
      <div class="card">
        <h5>三维柱状图</h5>
<!--            添加一行checkbox用于选择参数-->
        <div class="card flex flex-wrap justify-content-center gap-3">
          <div class="flex align-items-center">
            <Checkbox v-model="DBar" inputId="ingredient1" name="3DBar" value="PREPOWER" />
            <label for="ingredient1" class="ml-2"> PREPOWER </label>
          </div>
          <div class="flex align-items-center">
            <Checkbox v-model="DBar" inputId="ingredient2" name="3DBar" value="PRESSURE" />
            <label for="ingredient2" class="ml-2"> PRESSURE </label>
          </div>
          <div class="flex align-items-center">
            <Checkbox v-model="DBar" inputId="ingredient3" name="3DBar" value="TEMPERATURE" />
            <label for="ingredient3" class="ml-2"> TEMPERATURE </label>
          </div>
          <div class="flex align-items-center">
            <Checkbox v-model="DBar" inputId="ingredient4" name="3DBar" value="HUMIDITY" />
            <label for="ingredient4" class="ml-2"> HUMIDITY </label>
          </div>
          <div class="flex align-items-center">
            <Checkbox v-model="DBar" inputId="ingredient5" name="3DBar" value="ROUND0" />
            <label for="ingredient5" class="ml-2"> ROUND(A.POWER,0) </label>
          </div>
          <div class="flex align-items-center">
            <Checkbox v-model="DBar" inputId="ingredient6" name="3DBar" value="ROUND1" />
            <label for="ingredient6" class="ml-2"> ROUND(A.WS,1) </label>
          </div>
          <div class="flex align-items-center">
            <Checkbox v-model="DBar" inputId="ingredient7" name="3DBar" value="WINDSPEED" />
            <label for="ingredient7" class="ml-2"> WINDSPEED </label>
          </div>
          <div class="flex align-items-center">
            <Checkbox v-model="DBar" inputId="ingredient8" name="3DBar" value="WINDDIRECTION" />
            <label for="ingredient8" class="ml-2"> WINDDIRECTION </label>
          </div>
          <div class="flex align-items-center">
            <Checkbox v-model="DBar" inputId="ingredient9" name="3DBar" value="YD15" />
            <label for="ingredient9" class="ml-2"> YD15 </label>
          </div>
<!--          添加更新的Button-->
        </div>
        <div class="flex align-items-center">
          <Button label="更新" @click="UpdateDBar"></Button>
        </div>

        <div ref="chart7" style="width: 1000px; height: 600px;"></div>
      </div>
    </div>
    <!--DBar end-->

        <!-- <div class="col-12">
            <div class="card">
                <h5>Carousel</h5>
                <Carousel :value="products" :numVisible="1" :numScroll="1" :circular="false" :responsiveOptions="carouselResponsiveOptions">
                    <template #item="product">
                        <div class="product-item">
                                <div class="mb-3">
                                    <img :src="'demo/images/product/' + product.data.image" :alt="product.data.name" class="product-image" />
                                </div>
                                <h6 class="mt-0 mb-3"> Comments Here </h6>
                                <div class="car-buttons mt-5">
                                        <Button type="button" class="p-button p-button-rounded mr-2" icon="pi pi-search"></Button>
                                        <Button type="button" class="p-button-success p-button-rounded mr-2" icon="pi pi-star-fill"></Button>
                                        <Button type="button" class="p-button-help p-button-rounded" icon="pi pi-cog"></Button>
                                </div>
                        </div>
                    </template>
                </Carousel>
            </div>
        </div> -->

        <!-- <div class="col-12">
            <div class="card">
                <h5>Image</h5>
                <div class="flex justify-content-center">
                    <Image :src="'demo/images/galleria/galleria11.jpg'" alt="Image" width="250" preview />
                </div>
            </div>
        </div> -->
    </div>
</template>


<style lang="scss" scoped>
@import '@/assets/demo/styles/badges.scss';
@import '@/assets/demo/styles/items.scss';
</style>
