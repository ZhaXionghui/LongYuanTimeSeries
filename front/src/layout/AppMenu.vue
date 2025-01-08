<script setup>
import { ref } from 'vue';

import AppMenuItem from './AppMenuItem.vue';

const model = ref([
    {
        label: 'Home',
        items: [
            {
                label: 'Bilibili',
                icon: 'pi pi-fw pi-star',
                items: [
                    {
                        label: '风电数据可视化',
                        icon: 'pi pi-fw pi-search',
                        url: 'https://www.bilibili.com/video/BV1Dd4y1f726',
                        target: '_blank'
                    },
                    {
                        label: '风电数据时间序列预测',
                        icon: 'pi pi-fw pi-search',
                        url: 'https://www.bilibili.com/video/BV1Nu411j7Kr',
                        target: '_blank'
                    },
                    {
                        label: '风电数据集成方法预测',
                        icon: 'pi pi-fw pi-search',
                        url: 'https://www.bilibili.com/video/BV1Vu4y1974R',
                        target: '_blank'
                    },
                ]
            },
            {
                label: 'AiStudio',
                icon: 'pi pi-fw pi-share-alt',
                items: [
                    {
                        label: '风电数据可视化',
                        icon: 'pi pi-fw pi-search',
                        url: 'https://aistudio.baidu.com/aistudio/projectdetail/6173709',
                        target: '_blank'
                    },
                    {
                        label: '风电数据时间序列预测',
                        icon: 'pi pi-fw pi-search',
                        url: 'https://aistudio.baidu.com/aistudio/projectdetail/6159803',
                        target: '_blank'
                    },
                    {
                        label: '风电数据集成方法预测',
                        icon: 'pi pi-fw pi-search',
                        url: 'https://aistudio.baidu.com/projectdetail/6641974 ',
                        target: '_blank'
                    },
                    
                ]
            },
            {label: 'Github', icon: 'pi pi-fw pi-clone', 
            url: 'https://github.com/ZhaXionghui/LongYuanTimeSerise'},
        ]
    },
    {
        label: 'Model',
        items: [
            {label: 'DataShow', icon: 'pi pi-fw pi-home', to: '/' }, 
            {label: 'Upload', icon: 'pi pi-fw pi-file', to: '/uikit/file' },
            {
                label: 'Machine Learning',
                icon: 'pi pi-fw pi-bookmark',
                items: [
                    {
                        label: 'LSTM',
                        icon: 'pi pi-fw pi-bookmark',
                        to: '/model/model1'
                        // items: [
                        //     { label: 'Submenu 1.1.1', icon: 'pi pi-fw pi-bookmark' },
                        //     { label: 'Submenu 1.1.2', icon: 'pi pi-fw pi-bookmark' },
                        //     { label: 'Submenu 1.1.3', icon: 'pi pi-fw pi-bookmark' }
                        // ]
                    },
                    // {
                    //     label: 'Model2',
                    //     icon: 'pi pi-fw pi-bookmark',
                    //     // to: '/uikit/media'
                    // },
                    // {
                    //     label: 'Model3',
                    //     icon: 'pi pi-fw pi-bookmark',
                    // },
                    // {
                    //     label: 'Model4',
                    //     icon: 'pi pi-fw pi-bookmark',
                    // },
                    // {
                    //     label: 'Submenu 1.2',
                    //     icon: 'pi pi-fw pi-bookmark',
                    //     items: [{ label: 'Submenu 1.2.1', icon: 'pi pi-fw pi-bookmark' }]
                    // }
                ]
            },
            {
                label: 'Traditional ML Models',
                icon: 'pi pi-fw pi-bookmark',
                items: [
                  {
                    label: 'ACF、PACF test',
                    icon: 'pi pi-fw pi-bookmark',
                    to: '/model/test'
                    // items: [
                    //     { label: 'Submenu 2.1.1', icon: 'pi pi-fw pi-bookmark' },
                    //     { label: 'Submenu 2.1.2', icon: 'pi pi-fw pi-bookmark' }
                    // ]
                  },
                    {
                        label: 'AR',
                        icon: 'pi pi-fw pi-bookmark',
                        to: '/model/ar'
                        // items: [
                        //     { label: 'Submenu 2.1.1', icon: 'pi pi-fw pi-bookmark' },
                        //     { label: 'Submenu 2.1.2', icon: 'pi pi-fw pi-bookmark' }
                        // ]
                    },
                    {
                        label: 'MA',
                        icon: 'pi pi-fw pi-bookmark',
                        to: '/model/ma'
                        // items: [{ label: 'Submenu 2.2.1', icon: 'pi pi-fw pi-bookmark' }]
                    },
                    {
                      label: 'ARMA',
                      icon: 'pi pi-fw pi-bookmark',
                      to: '/model/arma'
                      // items: [{ label: 'Submenu 2.2.1', icon: 'pi pi-fw pi-bookmark' }]
                    },
                    {
                      label: 'ARIMA',
                      icon: 'pi pi-fw pi-bookmark',
                      to: '/model/arima'
                      // items: [{ label: 'Submenu 2.2.1', icon: 'pi pi-fw pi-bookmark' }]
                    },
                    {
                      label: 'SES',
                      icon: 'pi pi-fw pi-bookmark',
                      to: '/model/ses'
                      // items: [{ label: 'Submenu 2.2.1', icon: 'pi pi-fw pi-bookmark' }]
                    },
                    {
                      label: 'DES',
                      icon: 'pi pi-fw pi-bookmark',
                      to: '/model/des'
                      // items: [{ label: 'Submenu 2.2.1', icon: 'pi pi-fw pi-bookmark' }]
                    },
                    {
                      label: 'TES',
                      icon: 'pi pi-fw pi-bookmark',
                      to: '/model/tes'
                      // items: [{ label: 'Submenu 2.2.1', icon: 'pi pi-fw pi-bookmark' }]
                    },
                    {
                      label: 'SARIMA',
                      icon: 'pi pi-fw pi-bookmark',
                      to: '/model/sarima'
                      // items: [{ label: 'Submenu 2.2.1', icon: 'pi pi-fw pi-bookmark' }]
                    },
                    {
                      label: 'VAR',
                      icon: 'pi pi-fw pi-bookmark',
                      to: '/model/var'
                      // items: [{ label: 'Submenu 2.2.1', icon: 'pi pi-fw pi-bookmark' }]
                    },
                    {
                      label: 'GARCH',
                      icon: 'pi pi-fw pi-bookmark',
                      to: '/model/garch'
                      // items: [{ label: 'Submenu 2.2.1', icon: 'pi pi-fw pi-bookmark' }]
                    }
                ]
            },
          {
            label: 'Esemble Learning Model',
            icon: 'pi pi-fw pi-bookmark',
            to: '/model/mixing'
            // items: [{ label: 'Submenu 2.2.1', icon: 'pi pi-fw pi-bookmark' }]
          },
          {
            label: 'User Model',
            icon: 'pi pi-fw pi-bookmark',
            to: '/model/usermodel'
            // items: [{ label: 'Submenu 2.2.1', icon: 'pi pi-fw pi-bookmark' }]
          }
        ]
    },    
    // {
    //     label: 'Test',
    //     items: [
    //         { label: 'Form Layout', icon: 'pi pi-fw pi-id-card', to: '/uikit/formlayout' },
    //         { label: 'Input', icon: 'pi pi-fw pi-check-square', to: '/uikit/input' },
    //         { label: 'Float Label', icon: 'pi pi-fw pi-bookmark', to: '/uikit/floatlabel' },
    //         { label: 'Invalid State', icon: 'pi pi-fw pi-exclamation-circle', to: '/uikit/invalidstate' },
    //         { label: 'Button', icon: 'pi pi-fw pi-mobile', to: '/uikit/button', class: 'rotated-icon' },
    //         { label: 'Table', icon: 'pi pi-fw pi-table', to: '/uikit/table' },
    //         { label: 'List', icon: 'pi pi-fw pi-list', to: '/uikit/list' },
    //         { label: 'Tree', icon: 'pi pi-fw pi-share-alt', to: '/uikit/tree' },
    //         { label: 'Panel', icon: 'pi pi-fw pi-tablet', to: '/uikit/panel' },
    //         { label: 'Overlay', icon: 'pi pi-fw pi-clone', to: '/uikit/overlay' },
    //         { label: 'Media', icon: 'pi pi-fw pi-image', to: '/uikit/media' },
    //         { label: 'Menu', icon: 'pi pi-fw pi-bars', to: '/uikit/menu', preventExact: true },
    //         { label: 'Message', icon: 'pi pi-fw pi-comment', to: '/uikit/message' },
    //         { label: 'File', icon: 'pi pi-fw pi-file', to: '/uikit/file' },
    //         { label: 'Chart', icon: 'pi pi-fw pi-chart-bar', to: '/uikit/charts' },
    //         { label: 'Misc', icon: 'pi pi-fw pi-circle', to: '/uikit/misc' }
    //     ]
    // },
    // {
    //     label: 'Prime Blocks',
    //     items: [
    //         { label: 'Free Blocks', icon: 'pi pi-fw pi-eye', to: '/blocks', badge: 'NEW' },
    //         { label: 'All Blocks', icon: 'pi pi-fw pi-globe', url: 'https://www.primefaces.org/primeblocks-vue', target: '_blank' }
    //     ]
    // },
    // {
    //     label: 'Utilities',
    //     items: [
    //         { label: 'PrimeIcons', icon: 'pi pi-fw pi-prime', to: '/utilities/icons' },
    //         { label: 'PrimeFlex', icon: 'pi pi-fw pi-desktop', url: 'https://www.primefaces.org/primeflex/', target: '_blank' }
    //     ]
    // },
    // {
    //     label: 'Pages',
    //     icon: 'pi pi-fw pi-briefcase',
    //     to: '/pages',
    //     items: [
    //         {
    //             label: 'Landing',
    //             icon: 'pi pi-fw pi-globe',
    //             to: '/landing'
    //         },
    //         {
    //             label: 'Auth',
    //             icon: 'pi pi-fw pi-user',
    //             items: [
    //                 {
    //                     label: 'Login',
    //                     icon: 'pi pi-fw pi-sign-in',
    //                     to: '/auth/login'
    //                 },
    //                 {
    //                     label: 'Error',
    //                     icon: 'pi pi-fw pi-times-circle',
    //                     to: '/auth/error'
    //                 },
    //                 {
    //                     label: 'Access Denied',
    //                     icon: 'pi pi-fw pi-lock',
    //                     to: '/auth/access'
    //                 }
    //             ]
    //         },
    //         {
    //             label: 'Crud',
    //             icon: 'pi pi-fw pi-pencil',
    //             to: '/pages/crud'
    //         },
    //         {
    //             label: 'Timeline',
    //             icon: 'pi pi-fw pi-calendar',
    //             to: '/pages/timeline'
    //         },
    //         {
    //             label: 'Not Found',
    //             icon: 'pi pi-fw pi-exclamation-circle',
    //             to: '/pages/notfound'
    //         },
    //         {
    //             label: 'Empty',
    //             icon: 'pi pi-fw pi-circle-off',
    //             to: '/pages/empty'
    //         }
    //     ]
    // },
    // {
    //     label: 'Get Started',
    //     items: [
    //         {
    //             label: 'Documentation',
    //             icon: 'pi pi-fw pi-question',
    //             to: '/documentation'
    //         },
    //         {
    //             label: 'View Source',
    //             icon: 'pi pi-fw pi-search',
    //             url: 'https://github.com/primefaces/sakai-vue',
    //             target: '_blank'
    //         },
    //         {
    //             label: 'Nuxt Version',
    //             url: 'https://github.com/primefaces/sakai-nuxt',
    //             icon: 'pi pi-fw pi-star'
    //         }
    //     ]
    // }
]);
</script>

<template>
    <ul class="layout-menu">
        <template v-for="(item, i) in model" :key="item">
            <app-menu-item v-if="!item.separator" :item="item" :index="i"></app-menu-item>
            <li v-if="item.separator" class="menu-separator"></li>
        </template>
        <li>
            <a href="https://www.primefaces.org/primeblocks-vue/#/" target="_blank">
                <!-- <img src="/layout/images/banner-primeblocks.png" alt="Prime Blocks" class="w-full mt-3" /> -->
            </a>
        </li>
    </ul>
</template>

<style lang="scss" scoped></style>
