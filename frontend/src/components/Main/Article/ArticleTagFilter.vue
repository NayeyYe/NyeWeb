<template>
  <el-card class="tag-filter-card" shadow="never">
    <template #header>
      <div class="card-header">
        <span>标签分类</span>
        <el-button link type="primary" @click="clearFilter" v-if="activeTag">清空</el-button>
      </div>
    </template>
    <div v-loading="loading">
      <div v-if="!loading && displayTags.length > 0" class="tag-list">
        <el-tag
          v-for="tag in displayTags"
          :key="tag"
          :class="{ 'is-active': activeTag === tag }"
          class="tag-item"
          effect="light"
          @click="selectTag(tag)"
          :style="getTagStyle(displayTagCounts[tag] || 0)"
        >
          {{ tag }} ({{ displayTagCounts[tag] || 0 }})
        </el-tag>
      </div>
      <el-empty v-else-if="!loading && displayTags.length === 0" description="暂无标签数据" :image-size="60">
      </el-empty>
    </div>
  </el-card>
</template>

<script setup>
import {computed, onMounted, ref, watch} from 'vue'
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

const API_BASE_URL = '/api'

// 优先显示数据库数据，���果没有则使用props数据
const displayTags = computed(() => {
  return tagsFromDB.value.length > 0 ? tagsFromDB.value : props.tags
})

const displayTagCounts = computed(() => {
  return Object.keys(tagCountsFromDB.value).length > 0 ? tagCountsFromDB.value : props.counts
})

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
      console.log(`ArticleTagFilter: 成功获取 ${tagsFromDB.value.length} 个标签`)
    }
  } catch (error) {
    console.error('ArticleTagFilter: 获取标签数据失败:', error)
    tagsFromDB.value = []
    tagCountsFromDB.value = {}
  } finally {
    loading.value = false
  }
}

const selectTag = (tag) => {
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
  const countsToUse = displayTagCounts.value
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
  const basePadding = 1
  const maxPadding = 2.5

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
