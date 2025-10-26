<template>
  <el-card class="timeline-card" shadow="never">
    <template #header>
      <div class="card-header">
        <span>文章归档</span>
        <el-button v-if="selectedDate" link type="primary" @click="clearFilter">清空</el-button>
        <el-icon :title="isCollapsed ? '展开' : '收起'" class="collapse-icon" @click="isCollapsed = !isCollapsed">
          <arrow-up-bold v-if="!isCollapsed"/>
          <arrow-down-bold v-else/>
        </el-icon>
      </div>
    </template>
    <div v-loading="loading" class="timeline-content">
      <el-collapse-transition>
        <el-timeline v-show="!isCollapsed && !loading && sortedArticles.length > 0">
          <el-timeline-item
              v-for="article in sortedArticles"
              :key="article.slug"
              :timestamp="article.date"
              placement="top"
          >
            <a class="timeline-link" @click.prevent="onArticleClick(article.slug)">
              {{ article.title }}
            </a>
          </el-timeline-item>
        </el-timeline>
      </el-collapse-transition>
      <el-empty v-if="!loading && sortedArticles.length === 0" :image-size="60" description="暂无文章数据">
      </el-empty>
    </div>
  </el-card>
</template>

<script setup>
import {computed, onMounted, ref, watch} from 'vue'
import {ArrowDownBold, ArrowUpBold} from '@element-plus/icons-vue'
import axios from 'axios'

const props = defineProps({
  articles: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['scrollToArticle'])

const loading = ref(false)
const articlesFromDB = ref([])
const isCollapsed = ref(false)
const selectedDate = ref(null)

const API_BASE_URL = '/api'

// 获取数据库中的文章数据
const fetchArticles = async () => {
  loading.value = true
  try {
    const response = await axios.get(`${API_BASE_URL}/articles`, {
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    })

    if (response.data && Array.isArray(response.data)) {
      articlesFromDB.value = response.data
      console.log(`ArticleTimeline: 成功获取 ${articlesFromDB.value.length} 篇文章`)
    }
  } catch (error) {
    console.error('ArticleTimeline: 获取文章数据失败:', error)
    articlesFromDB.value = []
  } finally {
    loading.value = false
  }
}

// 修改：直接使用传入的articles，这样可以响应筛选
const sortedArticles = computed(() => {
  return [...props.articles].sort((a, b) => new Date(b.date) - new Date(a.date))
})

const onArticleClick = (slug) => {
  emit('scrollToArticle', slug)
}

const clearFilter = () => {
  selectedDate.value = null
  // 可以在这里添加更多清空逻辑
}

// 监听props变化，当articles数据更新时重新获取数据库文章
watch(() => props.articles, (newArticles) => {
  if (newArticles && newArticles.length > 0 && articlesFromDB.value.length === 0) {
    // 如果还没有从数据库获取到数据，且有新的文章数据，则尝试重新获取
    fetchArticles()
  }
}, {immediate: true})

onMounted(() => {
  fetchArticles()
})
</script>

<style scoped>
.timeline-card {
  border-radius: 15px;
  position: sticky;
  top: 100px;
  border: 1px solid var(--el-border-color-lighter);
  margin-bottom: 20px;
  max-height: 600px;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.collapse-icon {
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
}

.collapse-icon:hover {
  color: var(--el-color-primary);
}

.timeline-link {
  cursor: pointer;
  color: #606266;
  transition: color 0.3s;
  text-decoration: none;
  display: block;
  padding: 2px 0;
}

.timeline-link:hover {
  color: var(--el-color-primary);
}

.el-timeline {
  padding-left: 0;
}

:deep(.el-timeline-item__timestamp) {
  color: var(--el-text-color-regular);
  font-size: 12px;
}

.timeline-content {
  max-height: 500px;
  overflow-y: auto;
  overflow-x: hidden;
}

.timeline-content::-webkit-scrollbar {
  width: 6px;
}

.timeline-content::-webkit-scrollbar-track {
  background: var(--el-fill-color-lighter);
  border-radius: 3px;
}

.timeline-content::-webkit-scrollbar-thumb {
  background: var(--el-border-color);
  border-radius: 3px;
}

.timeline-content::-webkit-scrollbar-thumb:hover {
  background: var(--el-border-color-dark);
}
</style>
