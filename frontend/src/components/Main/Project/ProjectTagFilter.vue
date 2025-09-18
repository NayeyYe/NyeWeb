<script lang="ts" setup>
import {computed, onMounted, ref, watch} from 'vue'
import axios from 'axios'

interface Props {
  tags: string[]
  counts: Record<string, number>
}

const props = defineProps<Props>()

const emit = defineEmits(['tag-selected'])

const loading = ref(false)
const tagsFromDB = ref<string[]>([])
const tagCountsFromDB = ref<Record<string, number>>({})
const activeTag = ref<string | null>(null)

const API_BASE_URL = '/api'

// 获取数据库中的项目标签数据
const fetchProjectTags = async () => {
  loading.value = true
  try {
    const response = await axios.get(`${API_BASE_URL}/project-tags`, {
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    })

    if (response.data) {
      tagsFromDB.value = response.data.tags || []
      tagCountsFromDB.value = response.data.counts || {}
      console.log(`ProjectTagFilter: 成功获取 ${tagsFromDB.value.length} 个项目标签`)
    }
  } catch (error) {
    console.error('ProjectTagFilter: 获取项目标签数据失败:', error)
    tagsFromDB.value = []
    tagCountsFromDB.value = {}
  } finally {
    loading.value = false
  }
}

const selectTag = (tag: string | null) => {
  if (activeTag.value === tag) {
    activeTag.value = null
  } else {
    activeTag.value = tag
  }
  emit('tag-selected', activeTag.value)
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
    return {min: 1, max: 1}
  }
  return {
    min: Math.min(...countsArray),
    max: Math.max(...countsArray),
  }
})

// 根据项目数量获取标签样式
const getTagStyle = (count) => {
  const {min, max} = fontMetrics.value
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

// 监听props变化，当props��据更新时重新获取标签
watch(() => [props.tags, props.counts], ([newTags, newCounts]) => {
  if (newTags && newTags.length > 0 && tagsFromDB.value.length === 0) {
    // 如果还没有从数据库获取到数据，且有新的标签数据，则尝试重新获取
    fetchProjectTags()
  }
}, {immediate: true})

onMounted(() => {
  fetchProjectTags()
})
</script>

<template>
  <el-card class="tag-filter-card" shadow="never">
    <template #header>
      <div class="card-header">
        <span>技术标签</span>
        <el-button v-if="activeTag" link type="primary" @click="clearFilter">清空</el-button>
      </div>
    </template>
    <div v-loading="loading">
      <div v-if="!loading && (tagsFromDB.length > 0 || props.tags.length > 0)" class="tag-list">
        <el-tag
            v-for="tag in (tagsFromDB.length > 0 ? tagsFromDB : props.tags)"
            :key="tag"
            :class="{ 'is-active': activeTag === tag }"
            :style="getTagStyle((Object.keys(tagCountsFromDB).length > 0 ? tagCountsFromDB : props.counts)[tag] || 0)"
            class="tag-item"
            effect="light"
            @click="selectTag(tag)"
        >
          {{ tag }} ({{ (Object.keys(tagCountsFromDB).length > 0 ? tagCountsFromDB : props.counts)[tag] || 0 }})
        </el-tag>
      </div>
      <el-empty v-else-if="!loading && tagsFromDB.length === 0 && props.tags.length === 0" :image-size="60"
                description="暂无标签数据">
      </el-empty>
    </div>
  </el-card>
</template>

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
  height: auto;
  line-height: 2;
  background-color: #ffffff;
  color: var(--el-text-color-primary);
}

.tag-item:hover {
  background-color: #f5f7fa;
  color: var(--el-color-primary);
}

.tag-item.is-active {
  background-color: var(--el-color-primary);
  color: #fff;
  border-color: var(--el-color-primary);
}
</style>