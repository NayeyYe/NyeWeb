<template>
  <el-card class="filter-card" shadow="never">
    <template #header>
      <div class="filter-header">
        <span>筛选条件</span>
        <div class="header-actions">
          <el-button :loading="loading" class="refresh-btn" link @click="fetchTags">
            <el-icon>
              <Refresh/>
            </el-icon>
            刷新
          </el-button>
          <el-button class="reset-link-btn" link @click="resetAllFilters">重置</el-button>
        </div>
      </div>
    </template>
    <div class="filter-controls">
      <!-- 标签筛选独立一行 -->
      <div class="filter-row tag-row">
        <div class="filter-item">
          <label>标签筛选：</label>
          <el-select
              :model-value="filters.tags"
              :multiple-limit="3"
              allow-create
              filterable
              multiple
              placeholder="选择标签（最多3个）"
              size="default"
              style="width: 350px"
              @update:model-value="$emit('update:tags', $event)"
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
              clearable
              placeholder="输入标题关键字"
              style="width: 250px"
              @update:model-value="$emit('update:title', $event)"
          />
        </div>
      </div>
      <div class="filter-row">
        <div class="filter-item">
          <label>状态筛选：</label>
          <el-select
              :model-value="filters.status"
              placeholder="选择状态"
              style="width: 140px"
              @update:model-value="$emit('update:status', $event)"
          >
            <el-option label="全部" value=""/>
            <el-option label="已发布" value="published"/>
            <el-option label="草稿" value="draft"/>
            <el-option label="已回收" value="recycled"/>
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
import {onMounted, ref} from 'vue'
import axios from 'axios'
import {Refresh} from '@element-plus/icons-vue'

const props = defineProps({
  filters: Object,
  sortOrder: String
})

const emit = defineEmits(['update:tags', 'update:title', 'update:status', 'update:sortOrder', 'reset'])

const allTags = ref([])
const loading = ref(false)

// 获取标签(获取所有文章的标签，不限制状态)
const fetchTags = async () => {
  try {
    loading.value = true
    const res = await axios.get('/api/tags')
    allTags.value = res.data.tags || []
    console.log('获取到的所有标签:', allTags.value)
  } catch (error) {
    console.error('获取标签失败:', error)
    allTags.value = []
  } finally {
    loading.value = false
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

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.refresh-btn {
  color: #666 !important;
  font-weight: normal !important;
  display: flex;
  align-items: center;
  gap: 4px;
}

.refresh-btn:hover {
  color: #409eff !important;
  background: transparent !important;
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

/* 响应式布局优化 */
@media (max-width: 768px) {
  .filter-card {
    height: 250px;
  }
  
  .filter-controls {
    height: 170px;
    padding: 8px 0;
  }
  
  .tag-row {
    margin-bottom: 15px;
  }
  
  .filter-row {
    margin-bottom: 12px;
  }
  
  .filter-item label {
    min-width: 70px;
    font-size: 13px;
  }
  
  .filter-item :deep(.el-select) {
    width: 280px !important;
  }
  
  .filter-item :deep(.el-input) {
    width: 200px !important;
  }
  
  .header-actions {
    gap: 5px;
  }
}

@media (max-width: 480px) {
  .filter-card {
    height: 220px;
  }
  
  .filter-controls {
    height: 140px;
    padding: 5px 0;
  }
  
  .tag-row {
    margin-bottom: 10px;
  }
  
  .filter-row {
    margin-bottom: 8px;
    gap: 10px;
  }
  
  .filter-item {
    gap: 5px;
  }
  
  .filter-item label {
    min-width: 60px;
    font-size: 12px;
  }
  
  .filter-item :deep(.el-select) {
    width: 180px !important;
  }
  
  .filter-item :deep(.el-input) {
    width: 150px !important;
  }
  
  .filter-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .header-actions {
    align-self: flex-end;
    gap: 3px;
  }
  
  :deep(.el-card__header) {
    padding: 10px 12px;
  }
  
  :deep(.el-card__body) {
    padding: 12px;
  }
  
  :deep(.el-button) {
    font-size: 12px;
    padding: 6px 10px;
  }
}
</style>
