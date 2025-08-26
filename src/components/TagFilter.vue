<template>
  <el-card class="tag-filter-card" shadow="never">
    <template #header>
      <div class="card-header">
        <span>标签分类</span>
      </div>
    </template>
    <div class="tag-list">
      <el-tag
        v-for="tag in tags"
        :key="tag"
        :class="{ 'is-active': activeTag === tag }"
        class="tag-item"
        effect="light"
        @click="selectTag(tag)"
        :style="getTagStyle(counts[tag] || 0)"
      >
        {{ tag }} ({{ counts[tag] || 0 }})
      </el-tag>
    </div>
  </el-card>
</template>

<script setup>
import { ref, computed } from 'vue'

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

const activeTag = ref(null)

const selectTag = (tag) => {
  // 如果点击的是当前已激活的标签，则取消选择
  if (activeTag.value === tag) {
    activeTag.value = null
  } else {
    activeTag.value = tag
  }
  emit('tag-selected', activeTag.value)
}

// 计算数值范围，用于动态调整样式
const fontMetrics = computed(() => {
  const countsArray = Object.values(props.counts)
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
</script>

<style scoped>
.tag-filter-card {
  border-radius: 15px;
  border: 1px solid var(--el-border-color-lighter);
}

.card-header {
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
