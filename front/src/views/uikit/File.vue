<script setup>
import { useToast } from 'primevue/usetoast';
import axios from "axios";
import swal from 'sweetalert';
import {onMounted} from "vue";
const toast = useToast();

const onUpload =(csvfile) => {
  toast.add({ severity: 'info', summary: 'Success', detail: 'File Uploaded', life: 3000 });
  // 获取上传的文件，并打印
  const file = csvfile.files[0];
  let formData = new FormData();
  formData.append('file', file);
  formData.append('filename', file.name);
  // console.log(csvfile.raw);
  // let reader = new FileReader();   //先new 一个读文件的对象 FileReader
  //
  // if (typeof FileReader === "undefined") {  //用来判断你的浏览器是否支持 FileReader
  //   console.log("您的浏览器不支持文件读取。");
  // }
  // console.log(csvfile.raw);
  // reader.readAsArrayBuffer(file.raw); //读任意文件
  //
  // reader.onload = function (e) {
  //   var ints = new Uint8Array(e.target.result); //要使用读取的内容，所以将读取内容转化成Uint8Array
  //   ints = ints.slice(0, 5000); //截取一段读取的内容
  //   let snippets = new TextDecoder('gb2312').decode(ints); //二进制缓存区内容转化成中文（即也就是读取到的内容）
  //   console.log("读取的内容如下：");
  //   console.log(snippets);
  // };
  // console.log(file);
  // console.log(file.value);

  // axios.post('http://
  //    将Upload标签上传的文件传给后端
  axios.post('http://81.70.183.201:5000/Upload', formData, {
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

// 当用户访问该页面的时候，先判断本地是否存储了风机代号，如果存储了，则显示风机代号和时间范围
// 在Vue3中，渲染完后执行函数
onMounted(() => {
  //调用需要执行的方法
  const usn = localStorage.getItem("usn");
  const ust = localStorage.getItem("ust");
  // console.log(ust);
  if (ust){
    let usn = localStorage.getItem("usn");
    let st = localStorage.getItem("st");
    let et = localStorage.getItem("et");
    let ust = localStorage.getItem("ust");
    let uet = localStorage.getItem("uet");
    document.getElementById("fj").value = usn;
    document.getElementById("Fan").innerHTML = '已选择的风机代号为：'+ usn;
    document.getElementById("TimeRange").innerHTML = '对应的时间范围为：' + st + '~' + et;
    document.getElementById("start").setAttribute("min", st.split(' ')[0]);
    document.getElementById("start").setAttribute("max", et.split(' ')[0]);
    document.getElementById("start").value = ust;
    document.getElementById("end").setAttribute("min", st.split(' ')[0]);
    document.getElementById("end").setAttribute("max", et.split(' ')[0]);
    document.getElementById("end").value = uet;
  }
  else {
    if (usn){
      let usn = localStorage.getItem("usn");
      let st = localStorage.getItem("st");
      let et = localStorage.getItem("et");
      document.getElementById("fj").value = usn;
      document.getElementById("Fan").innerHTML = '已选择的风机代号为：'+ usn;
      document.getElementById("TimeRange").innerHTML = '对应的时间范围为：' + st + '~' + et;
    }
  }
});

// 根据风机代号从后端获取时间范围
const Gettimerange = () => {
    const usn = document.getElementById('fj').value;
    function show(cfg){
      swal({
        closeOnClickOutside: false,
        closeOnEsc: false,
        // 解构cfg对象，展开cfg对象所有属性
        ...cfg
      })
    }
    axios.post('http://81.70.183.201:5000/Gettimerange', {
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
        // console.log('test')
        // console.log(ret.data.msg);
      }else { // 成功
        //如果本地存储了风机代号，先清空
        if (localStorage.getItem('usn') != null) {
          localStorage.removeItem('usn');
          localStorage.removeItem('st');
          localStorage.removeItem('et');
        }
        // 存储风机代号，开始时间，结束时间
        localStorage.setItem('usn', usn);
        localStorage.setItem('st', ret.data.st);
        localStorage.setItem('et', ret.data.et);
        // // 给id为fj的input标签添加内容，内容为风机代号
        // document.getElementById('fj').value = usn;
        // 给id为Fan的p标签添加内容，内容为风机代号
        document.getElementById('Fan').innerHTML = '已选择的风机代号为：' + localStorage.getItem('usn');
        // 给id为TimeRange的p标签添加内容，内容为开始时间~结束时间
        document.getElementById('TimeRange').innerHTML = '对应的时间范围为：' + localStorage.getItem('st') + '~' + localStorage.getItem('et');
        // 打印存储的风机代号，开始时间，结束时间
        // console.log(localStorage.getItem('usn'));
        // console.log(localStorage.getItem('st'));
        // console.log(localStorage.getItem('et'));
      // 限制可选时间范围并默认为开始时间~结束时间
        document.getElementById('start').setAttribute("min", localStorage.getItem('st').split(' ')[0]);
        document.getElementById('start').setAttribute("max", localStorage.getItem('et').split(' ')[0]);
        document.getElementById('start').setAttribute("value", localStorage.getItem('st').split(' ')[0]);
        document.getElementById('end').setAttribute("min", localStorage.getItem('st').split(' ')[0]);
        document.getElementById('end').setAttribute("max", localStorage.getItem('et').split(' ')[0]);
        document.getElementById('end').setAttribute("value", localStorage.getItem('et').split(' ')[0]);
      }
    }).catch(err => {
        console.log(err);
    });
};

// 输入开始时间和结束时间，将时间范围传给后端
const modelpredict = () => {
  // 若是本地有存储ust和uet，则先清空
  if (localStorage.getItem('ust') != null) {
    localStorage.removeItem('ust');
    localStorage.removeItem('uet');
  }
  // 获取开始时间和结束时间
  const ust = document.getElementById('start').value;
  const uet = document.getElementById('end').value;
  localStorage.setItem('ust', ust);
  localStorage.setItem('uet', uet);
  // console.log(ust);
  // console.log(uet);
  function show(cfg) {
    // eslint-disable-next-line no-undef
    swal({
      closeOnClickOutside: false,
      closeOnEsc: false,
      // 解构cfg对象，展开cfg对象所有属性
      ...cfg
    })
  }
  // //判断本地是否存储了风机代号
  // if (localStorage.getItem('usn') == null) {
  //   show({
  //     title: '错误',
  //     text: '请先选择风机代号，获取时间范围',
  //     icon: 'error',
  //     button: {
  //       text: '好的'
  //     }
  //   })
  //   return;
  // }
  // else {
  //   //判断输入的时间是否合法
  //   if (ust > ent) {
  //     show({
  //       title: '错误',
  //       text: '开始时间不能大于结束时间',
  //       icon: 'error',
  //       button: {
  //         text: '好的'
  //       }
  //     })
  //     return;
  //   }
  //   else {
  //     //判断输入的时间是否为空
  //     if (ust == '' || ent == '') {
  //       show({
  //         title: '错误',
  //         text: '开始时间和结束时间不能为空',
  //         icon: 'error',
  //         button: {
  //           text: '好的'
  //         }
  //       })
  //       return;
  //     }
  //     else {
  //       //  判断输入的时间是否在时间范围内
  //       if (ust < localStorage.getItem('st') || ent > localStorage.getItem('et')) {
  //         show({
  //           title: '错误',
  //           text: '输入的时间不在时间范围内',
  //           icon: 'error',
  //           button: {
  //             text: '好的'
  //           }
  //         })
  //         return;
  //       }
  //     }
  //   }
  // }
  // 判断本地是否存储了风机代号
  if (localStorage.getItem('usn') == null) {
    show({
      title: '错误',
      text: '请先选择风机代号，获取时间范围',
      icon: 'error',
      button: {
        text: '好的'
      }
    })
    return;
  }
  else {
    show({
      title: '提示',
      text: '正在进行模型预测...',
      icon: 'info',
      button: false
    })
    const st = localStorage.getItem('st');
    const et = localStorage.getItem('et');
    axios.post('http://81.70.183.201:5000/modelpredict', {
      st,
      et,
      ust,
      uet
    }).then(res => {
      const ret = res.data
      if (ret.code) { // 错误
        show({
          title: '错误',
          text: ret.data.msg,
          icon: 'error',
          button: {
            text: '好的'
          }
        })
      } else { // 成功
        console.log(ret.data);
        show({
          title: '提示',
          text: ret.data.msg,
          icon: 'success',
          button: {
            text: '好的'
          }
        })
        // const t_id = ret.msg[2].toString()
        // localStorage.setItem('t_id', t_id);
        // // 跳转聊天页面
        // window.location.href='chat.html';
        // console.log(ret.st.toString());

        // const st = ret.st.toString();
        // console.log(st);
        // const st = ret.st.toString();
        // console.log(ret.data.code);
        // console.log(ret.data);
        // console.log(ret.et.toString());
        //  const t_id = ret.msg[2].toString()
        //  localStorage.setItem('t_id', t_id);
      }
    }).catch(err => {
      console.log(err);
    });
  }

};

// // 进入File页面时，先判断本地是否存储了风机代号，如果存储了，则显示风机代号和时间范围
// const usn = localStorage.getItem('usn');
// if (usn) {
//   document.getElementById('fj').value = usn;
//   Gettimerange();
// }


</script>

<template>
    <div class="grid">
        <div class="col-12">
            <div class="card">
                <h5>Upload</h5>
                <FileUpload name="demo[]" @uploader="onUpload" :multiple="true" customUpload />

                <!-- <h5>Basic</h5>
                <FileUpload mode="basic" name="demo[]" accept="image/*" :maxFileSize="1000000" @uploader="onUpload" customUpload /> -->
            </div>
        </div>
        <Toast />
    </div>

    <div class="grid">
        <div class="col-12 md:col-6">
            <div class="card p-fluid">
                <h5>参数输入</h5>
                <div class="field">
                    <label for="fj">风机代号</label>
                    <InputText id="fj" type="text" />
                </div>
              <Button label="获取" @click="Gettimerange" />
                <div class="field">
                    <label for="start">开始时间</label>
<!--                    <InputText id="start" type="text" />-->
<!--                  在有时间范围后提供可以选择开始日期和截止日期-->
                  <input type="date" id="start" name="start"
                         value="2021-01-01"
                         min="2021-01-01" max="2021-12-31">
                </div>
                <div class="field">
                    <label for="end">结束时间</label>
<!--                    <InputText id="end" type="text" />-->
                      <input type="date" id="end" name="end"
                         value="2021-01-01"
                         min="2021-01-01" max="2021-12-31">
                </div>
                <Button label="预测" @click="modelpredict" />
<!--              提供能够让用户下拉选择的从后端传来的时间范围内的开始时间和结束时间-->

            </div>
        </div>

        <div class="col-12 md:col-6">
            <div class="card">
                <h5>参数确认</h5>
                <Panel header="">
                    <p class="line-height-3 m-0" id="Fan">
                        已选择的风机代号为：
                    </p>
                    <p class="line-height-3 m-0" id="TimeRange">
                        对应的时间范围为：
                    </p>
                </Panel>
            </div>
        </div>
    </div>
</template>


