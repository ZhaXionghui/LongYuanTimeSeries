<script setup>
import ProductService from '@/service/ProductService';
import PhotoService from '@/service/PhotoService';
import { useLayout } from '@/layout/composables/layout';
import NodeService from '@/service/NodeService';
import {onMounted, ref, watch} from 'vue';
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
  console.log(productService.getProductsSmall());
  photoService.getImages().then((data) => (images.value = data));
  nodeService.getTreeTableNodes().then((data) => (treeTableValue.value = data));
  nodeService.getModel1Nodes().then((data) => (model1Value.value = data));
});



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

const ADFTest = () => {
  const method = 'ADF';
  const usn = localStorage.getItem("usn");
  const ust = localStorage.getItem("ust");
  const uet = localStorage.getItem("uet");
  function show(cfg){
    swal({
      closeOnClickOutside: false,
      closeOnEsc: false,
      // 解构cfg对象，展开cfg对象所有属性
      ...cfg
    })
  }
  if (ust){
    axios.post('http://81.70.183.201:5000/AdfAcfPacfTest', {
      method,
      usn,
      ust,
      uet
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
        swal({
          title: ret.msg,
          // text: ret.msg,
          icon: 'success',
          button: {
            text: '好的'
          }
        })
      }
    //  将ret.data转为字符串后存储到localStorage中
      console.log(ret.data['timeseries_adf']);
      // ret.data = JSON.stringify(ret.data);
      // 读取RE
      // console.log(ret.data['timeseries_adf']);
      localStorage.setItem("diff0_adf", JSON.stringify(ret.data['timeseries_adf']));
      localStorage.setItem("diff1_adf", JSON.stringify(ret.data['timeseries_diff1_adf']));
      localStorage.setItem("diff2_adf", JSON.stringify(ret.data['timeseries_diff2_adf']));
      const diff0_adf = localStorage.getItem("diff0_adf");
      const diff1_adf = localStorage.getItem("diff1_adf");
      const diff2_adf = localStorage.getItem("diff2_adf");
      document.getElementById("diff0_adf").innerHTML = 'ADF检验结果为：' + diff0_adf;
      document.getElementById("diff1_adf").innerHTML = '一阶差分后的ADF检验结果为：' + diff1_adf;
      document.getElementById("diff2_adf").innerHTML = '二阶差分后的ADF检验结果为：' + diff2_adf;
    }).catch(err => {
      console.log(err);
    });
  }

};

const ACFPACF = () => {
  const method = 'ACFPACF';
  const usn = localStorage.getItem("usn");
  const ust = localStorage.getItem("ust");
  const uet = localStorage.getItem("uet");
  //  获取填写的p值
  const acfpacf_d = document.getElementById("acfpacf_d").value;
  localStorage.setItem("acfpacf_d", acfpacf_d);
  function show(cfg){
    swal({
      closeOnClickOutside: false,
      closeOnEsc: false,
      // 解构cfg对象，展开cfg对象所有属性
      ...cfg
    })
  }
  if (ust){
    axios.post('http://81.70.183.201:5000/AdfAcfPacfTest', {
      method,
      usn,
      ust,
      uet,
      acfpacf_d
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
        swal({
          title: ret.data,
          // text: ret.data.data,
          icon: 'success',
          button: {
            text: '好的'
          }
        })
      }
    }).catch(err => {
      console.log(err);
    });

  }

};


onMounted(() => {
  const acfpacf_d = localStorage.getItem("acfpacf_d");
  if (acfpacf_d){
    document.getElementById("acfpacf_d").value = acfpacf_d;
  }

  const diff0_adf = localStorage.getItem("diff0_adf");
  if (diff0_adf){
    const diff1_adf = localStorage.getItem("diff1_adf");
    const diff2_adf = localStorage.getItem("diff2_adf");
    document.getElementById("diff0_adf").innerHTML = 'ADF检验结果为：' + diff0_adf;
    document.getElementById("diff1_adf").innerHTML = '一阶差分后的ADF检验结果为：' + diff1_adf;
    document.getElementById("diff2_adf").innerHTML = '二阶差分后的ADF检验结果为：' + diff2_adf;
  }
});


</script>


<template>
  <div class="grid p-fluid">

    <div class="col-12">
      <div class="card">
        <h5>ADF</h5>
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
                    <Button label="ADF 检验" class="mr-2 mb-2" @click="ADFTest" />
        </Panel>
      </div>
    </div>

    <div class="col-12">
      <div class="card">
        <h5>Carousel</h5>
        <Carousel :value="products" :numVisible="1" :numScroll="1" :circular="false" :responsiveOptions="carouselResponsiveOptions">
          <template #item="product">
            <div class="product-item">
              <div class="product-item-content">
                <div class="mb-3">
<!--                  <img :src="'demo/images/product/' + product.data.image" :alt="product.data.name" class="product-image" />-->
<!--                  <img :src="'81.70.183.201:5000/static/img/' + product.data.image" :alt="product.data.name" class="product-image" />-->
                  <Image :src="'http://81.70.183.201:5000/static/img/ADF.png'" :alt="ADF" class="product-image" width="600" preview />
                </div>
                <div>
                  <h4 class="mb-1">
                    {{ product.data.name }}
                  </h4>
<!--                  <h6 class="mt-0 mb-3">${{ product.data.price }}</h6>-->
<!--                  <span :class="'product-badge status-' + product.data.inventoryStatus.toLowerCase()">{{ product.data.inventoryStatus }}</span>-->
<!--                  <div class="car-buttons mt-5">-->
<!--                    <Button type="button" class="p-button p-button-rounded mr-2" icon="pi pi-search"></Button>-->
<!--                    <Button type="button" class="p-button-success p-button-rounded mr-2" icon="pi pi-star-fill"></Button>-->
<!--                    <Button type="button" class="p-button-help p-button-rounded" icon="pi pi-cog"></Button>-->
<!--                  </div>-->
                </div>
              </div>
            </div>
          </template>
        </Carousel>
      </div>
    </div>

    <!-- 文本 -->
    <div class="col-12">
      <div class="card">
        <h5>ADF 检验</h5>
        <Accordion :activeIndex="0">
          <AccordionTab header="结果">
            <p class="line-height-3 m-0" id="diff0_adf">
              ADF检验结果为
            </p>
            <p class="line-height-3 m-0" id="diff1_adf">
              一阶差分后的ADF检验结果为
            </p>
            <p class="line-height-3 m-0" id="diff2_adf">
              二阶差分后的ADF检验结果为
            </p>
          </AccordionTab>
<!--          <AccordionTab header="Reference">-->
<!--            <p class="line-height-3 m-0">-->
<!--              参考文献-->
<!--            </p>-->
<!--          </AccordionTab>-->
        </Accordion>
      </div>
    </div>



    <!-- 模型参数选择 -->
    <div class="col-12 md:col-6">
      <div class="card">
        <h5>ACF、PACF</h5>

                <div class="field">
                  <label for="acfpacf_d" >d</label>
                  <InputText  id="acfpacf_d" type="text" />
                </div>
                <Button label="确认" @click="ACFPACF" />
      </div>
    </div>

    <!-- 模型参数选择示例 -->
    <div class="col-12 md:col-6">
      <div class="card">
        <Panel header="示例" :toggleable="true">
          <p class="line-height-3 m-0" id="Fan">
            d = 1
          </p>
          <p>
          </p>
        </Panel>
      </div>
    </div>

    <div class="col-12">
      <div class="card">
        <h5>Carousel</h5>
        <Carousel :value="products" :numVisible="1" :numScroll="1" :circular="false" :responsiveOptions="carouselResponsiveOptions">
          <template #item="product">
            <div class="product-item">
              <div class="product-item-content">
                <div class="mb-3">
<!--                  <img src="'http://81.70.183.201:5000/static/img/' + product.data.image" :alt="product.data.name" class="product-image" />-->
                  <Image :src="product.data.url" :alt="product.data.name" class="product-image" width="600" preview />

                </div>
                <div>
                  <h4 class="mb-1">
                    {{ product.data.name }}
                  </h4>
                  <!--                  <h6 class="mt-0 mb-3">${{ product.data.price }}</h6>-->
                  <!--                  <span :class="'product-badge status-' + product.data.inventoryStatus.toLowerCase()">{{ product.data.inventoryStatus }}</span>-->
                  <!--                  <div class="car-buttons mt-5">-->
                  <!--                    <Button type="button" class="p-button p-button-rounded mr-2" icon="pi pi-search"></Button>-->
                  <!--                    <Button type="button" class="p-button-success p-button-rounded mr-2" icon="pi pi-star-fill"></Button>-->
                  <!--                    <Button type="button" class="p-button-help p-button-rounded" icon="pi pi-cog"></Button>-->
                  <!--                  </div>-->
                </div>
              </div>
            </div>
          </template>
        </Carousel>
      </div>
    </div>


  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/demo/styles/badges.scss';
@import '@/assets/demo/styles/items.scss';
</style>
