<template>
    <div class="sidebar">
      <div v-for="(item, index) in menu" :key="index" class="menu-section">
        <div class="menu-item" @click="toggleSubmenu(index)"  @mouseenter="item.hovered = true" 
        @mouseleave="item.hovered = false">
          <img :src="item.hovered ? item.icon2 : item.icon" class="icon"></img>
          <span>{{ item.title }}</span>
          <i class="arrow" :class="{ 'open': item.open }">›</i>
        </div>
        <ul v-if="item.submenu && item.open" class="submenu">
          <router-link 
            v-for="(subitem, subIndex) in item.submenu"
            :key="subIndex"
            class="submenu-item"
            :to="subitem.path"
          >
            {{ subitem.title }}
          </router-link>
        </ul>
      </div>
    </div>
  </template>

<script>
export default {
  name: 'Sidebar',
  data() {
    return {
      menu: [
        {
          title: 'Home',
          icon: "/src/assets/sider_image/home.svg",
          icon2: "/src/assets/sider_image/home_hover.svg",
          open: false,
          hovered: false,
          submenu: [
            { title: 'About', path: '/' },
            { title: 'Dashboard', path: '/dashboard' },
          ],
        },
        {
          title: 'Configuration',
          icon: '/src/assets/sider_image/config.svg',
          icon2: "/src/assets/sider_image/config_hover.svg",
          open: false,
          hovered: false,
          submenu: [
            { title: 'Set Nodes', path: '/set-nodes' },
            { title: 'Change Config', path: '/change-config' },
          ],
        },
        // 更多菜单项...
      ],
    };
  },
  methods: {
    toggleSubmenu(index) {
      this.menu[index].open = !this.menu[index].open;
    },
  },
};
</script>
  
  <style scoped>
  @font-face {
    font-family: 'NotoSerif-Italic-VariableFont';
    src: url('../assets/fonts/Montserrat,Noto_Serif/Noto_Serif/NotoSerif-VariableFont_wdth,wght.ttf') format('truetype');
    font-weight: normal;
    font-style: normal;
  }
  .sidebar {
    margin-top: 10vh;
    position: absolute;
    width: 12%;
    min-height: 90%;
    height: auto;
    background-color: #38345c;
    color: #fff;
    font-family: "NotoSerif-Italic-VariableFont";
  }
  
  .menu-header {
    font-size: 1.2em;
    color: #a29bfe;
    margin-bottom: 20px;
  }
  
  .menu-section {
    margin-bottom: 0vh;
  }

  .menu-section:first-child {
    margin-top: 2vh;
  }

  .menu-item {
    display: flex;
    align-items: center;
    cursor: pointer;
    padding: 10px;
    font-size: 1em;
    transition: background 0.3s;
    border-bottom: 1.5px solid black;
  }
  
  .menu-item:hover {
    color: #a29bfe;
  }
  
  .icon {
    margin-left: 0.2vw;
    margin-right: 1.1vw;
  }
  .arrow {
    margin-left: auto;
    transition: transform 0.3s;
  }
  
  .arrow.open {
    transform: rotate(90deg);
  }
  
  
  .submenu-item {
    width:100%;
    margin-left:-1.50vw;
    text-align: center;
    padding: 10px 0px;
    cursor: pointer;
    list-style: none;
    margin-bottom: 1vh;
    border-bottom: 1.5px solid black;
  }

  .submenu-item:hover{
    color:#a29bfe
  }

  .submenu a{
    text-decoration: none;
    color: #fff;
    display: block;
    padding-left: 0;
  }


  </style>
  