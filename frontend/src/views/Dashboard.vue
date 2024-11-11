<template>
  <div class="main-content">
    <div
      class="blockchain-container"
      @mousedown="startPan"
      @mousemove="onPan"
      @mouseup="endPan"
      @mouseleave="endPan"
      @wheel.prevent="onZoom"
    >
      <svg :width="svgWidth" :height="svgHeight">
        <g :transform="`translate(${panX}, ${panY}) scale(${zoomLevel})`">
          <!-- 绘制连接线 -->
          <line
            v-for="(line, index) in lines"
            :key="index"
            :x1="line.x1"
            :y1="line.y1"
            :x2="line.x2"
            :y2="line.y2"
            :stroke="line.color"
            stroke-width="1"
          />
          <!-- 绘制区块 -->
          <g v-for="(block, index) in blocks" :key="index">
            <polygon
              :points="calculateHexagonPoints(index)"
              :fill="block.color"
              class="hexagon"
            />
            <text
              :x="getTextPosition(index).x"
              :y="getTextPosition(index).y"
              text-anchor="middle"
              fill="#fff"
              font-size="10"
            >
              {{ block.label }}
            </text>
          </g>
        </g>
      </svg>
      
      <!-- 操作按钮区域 -->
      <div class="button-container">
        <div class="action-button" @click="restart">Restart</div>
        <div class="action-button" @click="centerLatestGreenBlock">Center</div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import axios from 'axios';

const hexRadius = 20; // 每个六边形的半径
const svgWidth = 1600; // SVG 画布宽度
const svgHeight = 750; // SVG 画布高度
const minDistance = 50; // 区块之间的最小距离
const maxDistance = 80; // 区块之间的最大距离

// 缩放和平移状态
const zoomLevel = ref(1);
const panX = ref(svgWidth / 2);
const panY = ref(svgHeight / 2);
let isPanning = false;
let startX = 0;
let startY = 0;

const intervalTime = 1000; // 定时调用的时间间隔（毫秒）
let apiInterval = null;
const lastFetchedHeight = ref(1); // 记录上次获取的区块高度

// 区块颜色定义
const CONFIRMED_COLOR = '#2ecc71'; // 绿色 - 已确认的区块
const ORPHAN_COLOR = '#3498db';    // 蓝色 - 废弃链区块
const COMPETING_COLOR = '#e74c3c'; // 红色 - 竞争中的区块
const GREEN_LINE_COLOR = '#2ecc71'; // 绿色线段
const RED_LINE_COLOR = '#e74c3c'; // 红色线段

// 区块链的起始状态，包含一个已确认的起始区块
let blockHeight = 0; // 当前区块高度
let blocks = ref([
  { 
    hash: '0'.repeat(64), // 用于表示创世区块的哈希
    previousHash: null,
    label: `高度 ${blockHeight}`,
    color: CONFIRMED_COLOR,
    position: { x: 0, y: 0 }
  }]);

let lines = ref([]); // 用于存储连接线的数组
let if_data = true
// 定时获取区块信息的函数
const fetchBlockData = async () => {
  try {
    if (if_data)
    {
      const response = await axios.get('http://127.0.0.1:5000/blocks');

    if (response.data.success) {
      const newBlocks = response.data.blocks;

      newBlocks.forEach((block) => {
        // 查找是否已经存在该区块
        const existingBlock = blocks.value.find(b => b.hash === block.block_hash);
        
        // 根据区块类型设置颜色
        const color = block.type === "确认区块" ? CONFIRMED_COLOR
                      : block.type === "竞争区块" ? COMPETING_COLOR
                      : ORPHAN_COLOR;

        if (existingBlock) {
          // 如果区块已存在但颜色（类型）发生了变化，更新颜色
          if (existingBlock.color !== color) {
            existingBlock.color = color;
          }
        } else {
          // 如果区块不存在，则按哈希顺序插入新的区块
          const previousBlock = blocks.value.find(b => b.hash === block.previous_hash);
          const position = previousBlock ? getRandomPosition(previousBlock.position) : { x: 0, y: 0 };

          // 添加新区块到 `blocks` 数组
          blocks.value.push({
            hash: block.block_hash,
            previousHash: block.previous_hash,
            label: `高度 ${block.height}`,
            color: color,
            position: position
          });

          // 如果存在父区块，绘制连接线
          if (previousBlock) {
            const lineColor = color === CONFIRMED_COLOR ? GREEN_LINE_COLOR : RED_LINE_COLOR;
            lines.value.push({
              x1: previousBlock.position.x,
              y1: previousBlock.position.y,
              x2: position.x,
              y2: position.y,
              color: lineColor
            });
          }
        }

        // 更新 `lastFetchedHeight` 为最新的区块高度
        lastFetchedHeight.value = Math.max(lastFetchedHeight.value, block.height);
      });
    } else {
      console.error("获取区块数据失败:", response.data.error);
    }
  }
 } catch (error) {
    console.error("API 调用失败:", error);
  }
};


// 设置定时器
onMounted(() => {
  fetchBlockData(); // 初次加载时调用
  apiInterval = setInterval(fetchBlockData, intervalTime); // 设置定时调用
});

// 清除定时器
onBeforeUnmount(() => {
  if (apiInterval) {
    clearInterval(apiInterval);
  }
});

// 随机生成一个不重叠的位置
const getRandomPosition = (lastPosition) => {
  let newPosition;
  let isOverlapping;

  do {
    const angle = Math.random() * 2 * Math.PI;
    const distance = minDistance + Math.random() * (maxDistance - minDistance);
    newPosition = {
      x: lastPosition.x + distance * Math.cos(angle),
      y: lastPosition.y + distance * Math.sin(angle)
    };

    isOverlapping = blocks.value.some(
      block => Math.hypot(block.position.x - newPosition.x, block.position.y - newPosition.y) < minDistance
    );
  } while (isOverlapping);

  return newPosition;
};

// 鼠标拖拽平移
const startPan = (event) => {
  isPanning = true;
  startX = event.clientX - panX.value;
  startY = event.clientY - panY.value;
};

const onPan = (event) => {
  if (isPanning) {
    panX.value = event.clientX - startX;
    panY.value = event.clientY - startY;
  }
};

const endPan = () => {
  isPanning = false;
};

// 鼠标滚轮缩放
const onZoom = (event) => {
  const scaleAmount = 0.1;
  zoomLevel.value = Math.min(Math.max(zoomLevel.value + (event.deltaY > 0 ? -scaleAmount : scaleAmount), 0.5), 3);
};

// 将最新的绿色区块移动到视图中心
const centerLatestGreenBlock = () => {
  const latestGreenBlock = blocks.value.slice().reverse().find(block => block.color === CONFIRMED_COLOR);
  if (latestGreenBlock) {
    panX.value = svgWidth / 2 - latestGreenBlock.position.x * zoomLevel.value;
    panY.value = svgHeight / 2 - latestGreenBlock.position.y * zoomLevel.value;
  }
};
// const startMining = async () => {
//   try {
//     const response = await axios.post('http://127.0.0.1:5000/start_mining');
//     console.log(response.data.message);
//   } catch (error) {
//     console.error("Error starting mining:", error);
//   }
// };

// const stopMining = async () => {
//   try {
//     const response = await axios.post('http://127.0.0.1:5000/stop_mining');
//     console.log(response.data.message);
//   } catch (error) {
//     console.error("Error stopping mining:", error);
//   }
// };

const restart = async () => {
  try {
    if_data=false
    let blockHeight = 0;
    blocks = ref([
  { 
    hash: '0'.repeat(64), // 用于表示创世区块的哈希
    previousHash: null,
    label: `高度 ${blockHeight}`,
    color: CONFIRMED_COLOR,
    position: { x: 0, y: 0 }
  }]);
  lines = ref([]);
  await axios.post('http://127.0.0.1:5000/restart_nodes');
  if_data= true
  // startMining();
  } catch (error) {
    console.error("Error restarting nodes:", error);
  }
}


// 根据索引计算六边形的点
const calculateHexagonPoints = (index) => {
  const { x, y } = blocks.value[index].position;
  let points = '';
  for (let i = 0; i < 6; i++) {
    const angle = Math.PI / 3 * i;
    const px = x + hexRadius * Math.cos(angle);
    const py = y + hexRadius * Math.sin(angle);
    points += `${px},${py} `;
  }
  return points.trim();
};

// 获取文本位置
const getTextPosition = (index) => blocks.value[index].position;
</script>

<style scoped>
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
}

.blockchain-container {
  margin-left: 2vw;
  margin-top: 16vh;
  width:80vw;
  height:auto;
  position: relative;
  display: flex;
  align-items: center;
  overflow: hidden;
  cursor: grab;
}

.blockchain-container:active {
  cursor: grabbing;
}

svg {
  background-color: #38345c;
  border-radius: 8px;
}

.hexagon {
  stroke: #34495e;
  stroke-width: 2;
  transition: fill 0.3s ease;
}

.button-container {
  display: flex;
  flex-direction: column;
  position: absolute;
  top: 1vh;
  right: 0.8vw;
  gap: 0.5vh;
}

.action-button {
  font-family: "NotoSerif-Italic-VariableFont";
  font-size: 1.2vw;
  padding: 1vh 1.5vw;
  color: rgb(140, 19, 177);
  background-color: #c69bfe;
  font-weight: bold;
  border-radius: 8px;
  box-shadow: 0px 4px 10px rgba(198, 155, 254, 0.4);
  text-align: center;
  cursor: pointer;
  margin-bottom: 1.5vh;
}

.action-button:hover {
  background-color: #a472e7;
  box-shadow: 0px 4px 10px rgba(166, 114, 231, 0.4);
  transform: translateY(-2px);
}

</style>
