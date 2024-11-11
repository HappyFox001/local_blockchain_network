<template>
  <div class="main-content">
    <div class="place">
      <div class="dashboard-header">
        <div class="header-btn">
          <img src="/src/assets/about_image/contact.svg" />
          <p>Contact Us And Support</p>
          <a href="">Contact</a>
        </div>
        <div class="header-btn">
          <img src="/src/assets/about_image/build.svg" />
          <p>Learn How to Build</p>
          <a href="">Learn</a>
        </div>
      </div>
      
      <div class="dashboard-sections">
        <!-- Bitcoin Section -->
        <div class="crypto-section">
          <div class="description">
            <h3>Bitcoin (BTC)</h3>
            <p>
              Bitcoin is a decentralized digital currency, without a central
              bank or single administrator. It can be sent from user to user on
              the peer-to-peer bitcoin network without intermediaries.
            </p>
          </div>
          <div class="chart-container">
            <Line :data="bitcoinData" :options="chartOptions" />
          </div>
        </div>
        
        <!-- Ethereum Section -->
        <div class="crypto-section">
          <div class="description">
            <h3>Ethereum (ETH)</h3>
            <p>
              Ethereum is a decentralized, open-source blockchain with smart contract functionality.
              Ether (ETH) is the native cryptocurrency of the platform.
            </p>
          </div>
          <div class="chart-container">
            <Line :data="ethereumData" :options="chartOptions" />
          </div>
        </div>
        
        <!-- Solana Section -->
        <div class="crypto-section">
          <div class="description">
            <h3>Solana (SOL)</h3>
            <p>
              Solana is a high-performance blockchain supporting builders around the world creating crypto apps.
              It aims to improve scalability with a unique combination of proof-of-stake and proof-of-history consensus.
            </p>
          </div>
          <div class="chart-container">
            <Line :data="solanaData" :options="chartOptions" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { Line } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
} from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement);

// Sample six-month data for Bitcoin
const bitcoinData = ref({
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
  datasets: [
    {
      label: 'Price (USD)',
      backgroundColor: 'rgba(241, 196, 15, 0.2)',
      borderColor: '#f1c40f',
      data: [45000, 47000, 44000, 49000, 51000, 48000],
      fill: true,
      tension: 0.4, // Creates a wavy effect
      borderWidth: 2,
    },
  ],
});

// Sample six-month data for Ethereum
const ethereumData = ref({
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
  datasets: [
    {
      label: 'Price (USD)',
      backgroundColor: 'rgba(52, 152, 219, 0.2)',
      borderColor: '#3498db',
      data: [3000, 3200, 3100, 3300, 3400, 3200],
      fill: true,
      tension: 0.4, // Creates a wavy effect
      borderWidth: 2,
    },
  ],
});

// Sample six-month data for Solana
const solanaData = ref({
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
  datasets: [
    {
      label: 'Price (USD)',
      backgroundColor: 'rgba(155, 89, 182, 0.2)',
      borderColor: '#9b59b6',
      data: [150, 170, 160, 180, 175, 165],
      fill: true,
      tension: 0.4, // Creates a wavy effect
      borderWidth: 2,
    },
  ],
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    x: {
      grid: {
        color: '#333',
      },
    },
    y: {
      grid: {
        color: '#333',
      },
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

.main-content {
  display: flex;
  flex-direction: column;
  padding-left: 1.5vw;
  background-color: #232338;
  color: #ffffff;
  min-height: 100vh;
  height: auto;
  width: calc(100% - 12%);
  margin-left: 12%;
  position: relative;
}

.place {
  margin-top: 3vh;
  margin-left: 3vh;
  width: 93%;
  min-height: 100vh;
  height: auto;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  margin-top: 12vh;
  margin-bottom: 3vh;
  width: 100%;
  height: 12vh;
}

.header-btn {
  background-color: #38345c;
  width: 49%;
  height: 100%;
  border-radius: 8px;
  align-items: center;
  display: flex;
  justify-content: space-between;
}

.header-btn img {
  margin-left: 2vw;
  width: 3vw;
}

.header-btn p {
  margin-left: 1.5vw;
  font-size: 1.2vw;
  text-align: left;
  color: #fff;
  font-family: 'NotoSerif-Italic-VariableFont';
  font-weight: bold;
}

.header-btn a {
  text-decoration: none;
  display: flex;
  height: 50%;
  width: 30%;
  background-color: #c69bfe;
  align-items: center;
  text-align: center;
  justify-content: center;
  font-size: 1.8vw;
  font-weight: bold;
  margin-right: 1vw;
  border-radius: 8px;
}

.header-btn a:hover {
  background-color: #a472e7;
  box-shadow: 0px 4px 10px rgba(166, 114, 231, 0.4);
  transform: translateY(-2px);
}

.dashboard-sections {
  display: flex;
  flex-direction: column;
}

.crypto-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 8px;
  margin-bottom: 3vh;
}

.description {
  height: 35vh;
  flex: 1;
  padding-right: 20px;
  margin-right: 2vw;
  background-color: #38345c;
  border-radius: 8px;
  text-align: left;
}

.description h3 {
  margin-top: 5vh;
  margin-left: 1.5vw;
  font-size: 1.5vw;
  font-weight: bold;
}

.description p {
  margin-top: 6vh;
  margin-left: 1.5vw;
  font-size: 1.2vw;
  font-weight: bold;
}

.chart-container {
  flex: 2;
  width: 100%;
  height: 35vh; /* Reduced height */
  background-color: #38345c;
  border-radius: 3vh;
}

.additional-charts {
  display: flex;
  justify-content: space-around;
  margin-top: 4vh;
}

.pie-chart-container,
.bar-chart-container {
  background-color: #38345c;
  border-radius: 8px;
  padding: 20px;
  width: 40%; /* Adjusted width to make charts smaller */
  height: 30vh; /* Reduced height */
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #fff;
}

.pie-chart-container h3,
.bar-chart-container h3 {
  margin-bottom: 1.5vh;
  font-size: 1.5vw;
}

</style>
