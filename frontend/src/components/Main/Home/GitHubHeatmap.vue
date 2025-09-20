<template>
  <el-card class="github-heatmap-card">
    <template #header>
      <div class="card-header">
        <span>GitHub 贡献</span>
        <el-tooltip content="过去一年的代码提交活动" placement="top">
          <el-icon><InfoFilled /></el-icon>
        </el-tooltip>
      </div>
    </template>
    <div v-loading="loading" class="heatmap-container">
      <div v-if="!loading && contributions.length === 0" class="empty-state">
        <el-empty description="暂无贡献数据" :image-size="60" />
      </div>
      <div v-else-if="!loading" class="heatmap">
        <div class="heatmap-months">
          <span v-for="month in months" :key="month" class="month-label">{{ month }}</span>
        </div>
        <div class="heatmap-grid">
          <div 
            v-for="(week, weekIndex) in weeks" 
            :key="weekIndex" 
            class="heatmap-week"
          >
            <div
              v-for="day in week"
              :key="day.date"
              class="heatmap-day"
              :class="getDayColorClass(day.count)"
              :style="{ opacity: day.count > 0 ? 0.8 + (day.count / maxCount) * 0.2 : 1.0 }"
              :title="`${day.date}: ${day.count} 次提交`"
            />
          </div>
        </div>
        <div class="heatmap-legend">
          <span>较少</span>
          <div class="legend-items">
            <div class="legend-item" style="background-color: #ebedf0;"></div>
            <div class="legend-item" style="background-color: #9be9a8; opacity: 0.8"></div>
            <div class="legend-item" style="background-color: #40c463; opacity: 0.9"></div>
            <div class="legend-item" style="background-color: #30a14e; opacity: 1.0"></div>
            <div class="legend-item" style="background-color: #216e39; opacity: 1.0"></div>
          </div>
          <span>较多</span>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { InfoFilled } from '@element-plus/icons-vue'

const loading = ref(false)
const contributions = ref([])
const maxCount = ref(0)

// 获取环境变量中的GitHub token
const GITHUB_TOKEN = import.meta.env.VITE_GITHUB_TOKEN

// 格式化月份标签
const months = computed(() => {
  const monthNames = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
  const uniqueMonths = new Set()
  contributions.value.forEach(contribution => {
    const date = new Date(contribution.date)
    uniqueMonths.add(date.getMonth())
  })
  return Array.from(uniqueMonths).sort().map(month => monthNames[month])
})

// 将贡献数据按周分组
const weeks = computed(() => {
  const weeksArray = []
  let currentWeek = []
  
  contributions.value.forEach((day, index) => {
    if (index % 7 === 0 && currentWeek.length > 0) {
      weeksArray.push(currentWeek)
      currentWeek = []
    }
    currentWeek.push(day)
  })
  
  if (currentWeek.length > 0) {
    weeksArray.push(currentWeek)
  }
  
  return weeksArray
})

// 根据提交次数获取颜色类
const getDayColorClass = (count) => {
  if (count === 0) return 'color-0'
  if (count <= 1) return 'color-1'
  if (count <= 3) return 'color-2'
  if (count <= 5) return 'color-3'
  return 'color-4'
}

// 获取GitHub贡献数据
const fetchGitHubContributions = async () => {
  if (!GITHUB_TOKEN || GITHUB_TOKEN === 'your_github_token_here') {
    console.warn('GitHub token未配置，请设置VITE_GITHUB_TOKEN环境变量')
    return
  }

  loading.value = true
  try {
    // 使用GitHub GraphQL API获取贡献数据
    const query = `
      query {
        viewer {
          contributionsCollection(from: "${getOneYearAgo().toISOString()}", to: "${new Date().toISOString()}") {
            contributionCalendar {
              totalContributions
              weeks {
                contributionDays {
                  date
                  contributionCount
                  color
                }
              }
            }
          }
        }
      }
    `

    const response = await axios.post(
      'https://api.github.com/graphql',
      { query },
      {
        headers: {
          'Authorization': `Bearer ${GITHUB_TOKEN}`,
          'Content-Type': 'application/json',
        },
        timeout: 10000,
      }
    )

    const data = response.data.data.viewer.contributionsCollection.contributionCalendar
    const allContributions = []
    
    data.weeks.forEach(week => {
      week.contributionDays.forEach(day => {
        allContributions.push({
          date: day.date,
          count: day.contributionCount
        })
      })
    })

    contributions.value = allContributions
    maxCount.value = Math.max(...allContributions.map(d => d.count), 1)
    
  } catch (error) {
    console.error('获取GitHub贡献数据失败:', error)
    // 如果API调用失败，使用模拟数据
    contributions.value = generateMockData()
    maxCount.value = Math.max(...contributions.value.map(d => d.count), 1)
  } finally {
    loading.value = false
  }
}

// 生成一年前的日期
const getOneYearAgo = () => {
  const date = new Date()
  date.setFullYear(date.getFullYear() - 1)
  return date
}

// 生成模拟数据（用于测试或API失败时）
const generateMockData = () => {
  const data = []
  const today = new Date()
  const oneYearAgo = new Date(today)
  oneYearAgo.setFullYear(oneYearAgo.getFullYear() - 1)
  
  for (let d = new Date(oneYearAgo); d <= today; d.setDate(d.getDate() + 1)) {
    const dateStr = d.toISOString().split('T')[0]
    // 随机生成一些提交数据
    const count = Math.random() > 0.7 ? Math.floor(Math.random() * 10) : 0
    data.push({ date: dateStr, count })
  }
  
  return data
}

onMounted(() => {
  fetchGitHubContributions()
})
</script>

<style scoped>
.github-heatmap-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header span {
  font-size: 1.2em;
  font-weight: bold;
}

.heatmap-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 5px;
  width: 100%;
  box-sizing: border-box;
}

.heatmap {
  display: flex;
  flex-direction: column;
  gap: 3px;
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
}

.heatmap-months {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
  font-size: 10px;
  color: #666;
  height: 15px;
}

.month-label {
  flex: 1;
  text-align: center;
}

.heatmap-grid {
  display: flex;
  gap: 3px;
  justify-content: space-between;
  width: 100%;
  flex-wrap: nowrap;
}

.heatmap-week {
  display: flex;
  flex-direction: column;
  gap: 3px;
  flex: 1;
  min-width: 0;
}

.heatmap-day {
  width: 100%;
  aspect-ratio: 1 / 1;
  border-radius: 2px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-sizing: border-box;
  background-color: #ebedf0;
}

.heatmap-day:hover {
  opacity: 1 !important;
  transform: scale(1.1);
  z-index: 2;
  outline: 1px solid rgba(27, 31, 35, 0.3);
}

.color-0 { background-color: #ebedf0; }
.color-1 { background-color: #9be9a8; }
.color-2 { background-color: #40c463; }
.color-3 { background-color: #30a14e; }
.color-4 { background-color: #216e39; }

.heatmap-legend {
  display: flex;
  align-items: center;
  gap: 5px;
  margin-top: 8px;
  font-size: 10px;
  color: #666;
  justify-content: center;
  width: 100%;
  flex-shrink: 0;
}

.legend-items {
  display: flex;
  gap: 2px;
}

.legend-item {
  width: 10px;
  height: 10px;
  border-radius: 2px;
  flex-shrink: 0;
}

.empty-state {
  padding: 20px 0;
}
</style>