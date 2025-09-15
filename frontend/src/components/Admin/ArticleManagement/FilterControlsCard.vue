<template>
  <el-card class="filter-card" shadow="never">
    <template #header>
      <div class="filter-header">
        <span>筛选条件</span>
        <el-button link @click="resetAllFilters" class="reset-link-btn">重置</el-button>
      </div>
    </template>
    <div class="filter-controls">
      <!-- 标签筛选独立一行 -->
      <div class="filter-row tag-row">
        <div class="filter-item">
          <label>标签筛选：</label>
          <el-select
            :model-value="filters.tags"
            @update:model-value="$emit('update:tags', $event)"
            multiple
            filterable
            allow-create
            placeholder="选择或输入标签（最多3个）"
            style="width: 350px"
            size="default"
            :multiple-limit="3"
          >
            <el-option
              v-for="tag in allTags"
              :key="tag"
              :label="tag"
              :value="tag"
            />
          </el-select>
        </div>
      </div>
      <!-- 其他筛选条件 -->
      <div class="filter-row">
        <div class="filter-item">
          <label>标题搜索：</label>
          <el-input
            :model-value="filters.title"
            @update:model-value="$emit('update:title', $event)"
            placeholder="输入标题关键字"
            style="width: 250px"
            clearable
          />
        </div>
      </div>
      <div class="filter-row">
        <div class="filter-item">
          <label>状态筛选：</label>
          <el-select
            :model-value="filters.status"
            @update:model-value="$emit('update:status', $event)"
            style="width: 140px"
            placeholder="选择状态"
          >
            <el-option label="全部" value="" />
            <el-option label="已发布" value="published" />
            <el-option label="草稿" value="draft" />
            <el-option label="已回收" value="recycled" />
          </el-select>
        </div>
      </div>
      <div class="filter-row">
        <div class="filter-item">
          <label>时间排序：</label>
          <el-button-group>
            <el-button
              :type="sortOrder === 'asc' ? 'primary' : ''"
              @click="$emit('update:sortOrder', 'asc')"
            >
              升序
            </el-button>
            <el-button
              :type="sortOrder === 'desc' ? 'primary' : ''"
              @click="$emit('update:sortOrder', 'desc')"
            >
              降序
            </el-button>
          </el-button-group>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'

const props = defineProps({
  filters: Object,
  sortOrder: String
})

const emit = defineEmits(['update:tags', 'update:title', 'update:status', 'update:sortOrder', 'reset'])

const allTags = ref([])

// 获取标签
const fetchTags = async () => {
  try {
    const res = await axios.get('/api/tags')
    allTags.value = res.data.tags || []
  } catch (error) {
    console.error('获取标签失败:', error)
    allTags.value = []
  }
}

const resetAllFilters = () => {
  emit('reset')
}

onMounted(() => {
  fetchTags()
})
</script>

<style scoped>
.filter-card {
  border-radius: 12px;
  border: 1px solid #e1e8ed;
  height: 300px;
}

.filter-controls {
  padding: 10px 0;
  height: 220px;
  overflow-y: auto;
}

.tag-row {
  margin-bottom: 20px;
}

.filter-row {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 16px;
}

.filter-row:last-child {
  margin-bottom: 0;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-item label {
  color: #666;
  font-size: 14px;
  white-space: nowrap;
  min-width: 80px;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.reset-link-btn {
  color: #666 !important;
  font-weight: normal !important;
}

.reset-link-btn:hover {
  color: #409eff !important;
  background: transparent !important;
}

/* 自定义滚动条样式 */
.filter-controls::-webkit-scrollbar {
  width: 6px;
}

.filter-controls::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.filter-controls::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.filter-controls::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

:deep(.el-card__header) {
  padding: 16px 20px;
  background: #fafafa;
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-card__body) {
  padding: 20px;
}
</style>

