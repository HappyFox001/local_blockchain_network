<template>
    <header class="header">
      <div class="title-section">
        <img src="../assets/header_image/icon.webp" alt="Logo">
        <span class="divide">|</span>
        <span class="title">Local Block Chain Platform</span>
      </div>
      <div class="support-icons">
        <div class="github">
          <span class="support">Support us:</span>
          <a href="https://github.com/akveo" @mouseenter="onIconMouseEnter" @mouseleave="onIconMouseLeave"> 
            <img
            :src="githubIconSrc"
            alt="GitHub Star Icon"
            />
            <span>Star Here</span>
          </a>
        </div>
        <div class="email">
          <a href="https://mail.google.com/">
            <img src="../assets/header_image/email.svg" alt="Email Icon">
          </a>
          <span class="contact">3591713733@qq.com</span>
        </div>

        <div class="icon-group">
          <!-- <img src="search-icon.png" alt="Search Icon" class="icon">
          <img src="email-icon.png" alt="Email Icon" class="icon">
          <img src="notification-icon.png" alt="Notification Icon" class="icon"> -->
          <img src="../assets/header_image/my_icon.jpeg" alt="MyIcon" class="myicon">
          <span class="username">Qian Zhang</span>
          <!-- <span class="university">Wuhan University</span> -->
        </div>
      </div>
    </header>
  </template>
  
  <script>
    import githubStarWhite from '../assets/header_image/github_star_white.svg';
    import githubStarHover from '../assets/header_image/github_star_hover.svg';
    export default {
    name: "Header",
    data() {
        return {
        githubIconSrc: githubStarWhite, // 默认图像路径
        };
    },
    methods: {

        onIconMouseEnter() {
        // 鼠标移入时切换为 hover 图像
        this.mouseEnterTimeout = setTimeout(() => {
        this.githubIconSrc = githubStarHover;
    }, 100);
        },
        onIconMouseLeave() {
        // 鼠标移出时恢复默认图像
        this.githubIconSrc = githubStarWhite;
        },
    },
    };
  </script>
  
  <style scoped>
  @font-face {
    font-family: 'MonaSans-Italic-VariableFont';
    src: url('../assets/fonts/Mona_Sans,Montserrat,Noto_Serif/Mona_Sans/MonaSans-VariableFont_wdth,wght.ttf') format('truetype');
    font-weight: normal;
    font-style: normal;
  }
  @font-face {
    font-family: 'NotoSerif-Italic-VariableFont';
    src: url('../assets/fonts/Montserrat,Noto_Serif/Noto_Serif/NotoSerif-VariableFont_wdth,wght.ttf') format('truetype');
    font-weight: normal;
    font-style: normal;
  }
  .header {
    width: 100vw;
    height: 10vh;
    /* background: radial-gradient(at 99.16% 98.66%, hsla(258, 96%, 65%, 1) 0%, hsla(258, 96%, 65%, 0) 100%),
                radial-gradient(at 55.36% 82.86%, hsla(248, 100%, 60%, 1) 0%, hsla(248, 100%, 60%, 0) 100%),
                radial-gradient(at 62.79% 9.70%, hsla(0, 0%, 0%, 1) 0%, hsla(0, 0%, 0%, 0) 100%); */
    background-color: #38345c;
    position: absolute;
    display: flex;
    font-family: 'NotoSerif-Italic-VariableFont';
    /* justify-content: space-between; */
    align-items: center;
    color: #fff;
    box-shadow: 0px 2vh 10vh rgba(0, 0, 0, 0.5);
    border-bottom: 3vh solid balck;
    z-index: 1000;
  }
  
  .title-section {
    width:35%;
    position: relative;
    font-size: 2.0vw;
    display: flex;
    align-items: center;

  }

  .divide{
    margin-right: 2vw;
    font-size: 3.0vw;
    color: #000;
  }

  .title-section img {
    margin-left: 1.8vw;
    margin-right: 2vw;
    width: auto;
    height: 8vh;
    border-radius: 50%;
  }

  .title {
    font-size: 1.5vw;
  }
  .support-icons {
    width:65%;
    margin-left: 0;
    display: flex;
    align-items: center;
  }
  
  
  .github{
    display: flex;
    margin-left: 5vw;
    width:20vw;
  }

  .support {
    margin-left: 0;
    width:10vw;
    font-size: 1.8vw;
  }

  .github img{
    margin-left: 0;
    width:auto;
    height:2vw;
  }

  .github a {
    margin-left:1vw ;
    display: flex;
    justify-content: center;
    align-items: center;
    text-decoration: none;
    font-size: 1.2vw;
    color:#fff
  }

  .github a:hover {
      transform: matrix3d(1.1, 0, 0, 0, 0, 1.1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1);
      transition: all 0.5s ease-in-out;
      color:#a29bfe
  }

  .email {
    margin-left: 5vw;
    width:15vw;
    display: flex;
    align-items: center;
  }
  .email img {
    width:auto;
    height:5vh;
    margin-right: 1vw;
  }
  .contact {
    margin-right: 5vw;
    font-size: 1.0vw;
  }
  
  .icon-group {
    margin-right: 0;
    width:auto;
    margin-left: 5vw;
    display: flex;
    align-items: center;
  }
  
  
  .username {
    font-weight: bold;
    margin-right:2vw;
    
  }

  /* .university {
    font-weight: bold;
    margin-right: 0;
  } */

  .myicon{
    width:2.5vw;
    height: auto;
    margin-right: 1vw;
    border-radius: 50%;
  }
  </style>
  