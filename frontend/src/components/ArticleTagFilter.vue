<template>
  <el-card class="tag-filter-card" shadow="never">
    <template #header>
      <div class="card-header">
        <span>标签分类</span>
        <el-button link type="primary" @click="clearFilter" v-if="activeTag">清空</el-button>
      </div>
    </template>
    <div v-loading="loading">
      <div v-if="!loading && tagsFromDB.length > 0" class="tag-list">
        <el-tag
          v-for="tag in tagsFromDB"
          :key="tag"
          :class="{ 'is-active': activeTag === tag }"
          class="tag-item"
          effect="light"
          @click="selectTag(tag)"
          :style="getTagStyle(tagCountsFromDB[tag] || 0)"
        >
          {{ tag }} ({{ tagCountsFromDB[tag] || 0 }})
        </el-tag>
      </div>
      <el-empty v-else-if="!loading && tagsFromDB.length === 0" description="暂无标签数据" :image-size="60">
      </el-empty>
    </div>
  </el-card>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'

const props = defineProps({
  tags: {
    type: Array,
    required: true,
  },
  counts: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['tag-selected'])

const loading = ref(false)
const tagsFromDB = ref([])
const tagCountsFromDB = ref({})
const activeTag = ref(null)

const API_BASE_URL = 'http://localhost:8080/api'

// 获取数据库中的标签数据
const fetchTags = async () => {
  loading.value = true
  try {
    const response = await axios.get(`${API_BASE_URL}/tags`, {
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    })

    if (response.data) {
      tagsFromDB.value = response.data.tags || []
      tagCountsFromDB.value = response.data.counts || {}
      console.log(`成功获取 ${tagsFromDB.value.length} 个标签`)
    }
  } catch (error) {
    console.error('获取标签数据失败:', error)
    tagsFromDB.value = []
    tagCountsFromDB.value = {}
  } finally {
    loading.value = false
  }
}

const selectTag = (tag) => {
  // 如果点击的是当前已激活的标签，则取消选择
  if (activeTag.value === tag) {
    clearFilter()
  } else {
    activeTag.value = tag
    emit('tag-selected', tag)
  }
}

const clearFilter = () => {
  activeTag.value = null
  emit('tag-selected', null)
}

// 计算数值范围，用于动态调整样式
const fontMetrics = computed(() => {
  // 优先使用数据库数据，如果没有则使用传入的props数据作为备用
  const countsToUse = Object.keys(tagCountsFromDB.value).length > 0 ? tagCountsFromDB.value : props.counts
  const countsArray = Object.values(countsToUse)
  if (countsArray.length === 0) {
    return { min: 1, max: 1 }
  }
  return {
    min: Math.min(...countsArray),
    max: Math.max(...countsArray),
  }
})

// 根据文章数量获取标签样式
const getTagStyle = (count) => {
  const { min, max } = fontMetrics.value
  const basePadding = 1 // em
  const maxPadding = 2.5 // em

  let horizontalPadding
  if (max === min || count === undefined) {
    horizontalPadding = basePadding
  } else {
    const normalized = (count - min) / (max - min)
    horizontalPadding = basePadding + normalized * (maxPadding - basePadding)
  }

  return {
    padding: `0 ${horizontalPadding.toFixed(2)}em`,
  }
}

// 监听props变化，当props数据更新时重新获取标签
watch(() => [props.tags, props.counts], ([newTags, newCounts]) => {
  if (newTags && newTags.length > 0 && tagsFromDB.value.length === 0) {
    // 如果还没有从数据库获取到数据，且有新的标签数据，则尝试重新获取
    fetchTags()
  }
}, { immediate: true })

onMounted(() => {
  fetchTags()
})
</script>

<style scoped>
.tag-filter-card {
  border-radius: 15px;
  border: 1px solid var(--el-border-color-lighter);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag-item {
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  border: 1px solid var(--el-border-color-light);
  /* 动态调整大小 */
  height: auto;
  line-height: 2;
  /* 默认样式：白色背景，深色文字 */
  background-color: #ffffff;
  color: var(--el-text-color-primary);
}

.tag-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--el-box-shadow-light);
}

.tag-item.is-active {
  background-color: var(--el-color-primary);
  color: white;
  border-color: var(--el-color-primary);
}
</style>
