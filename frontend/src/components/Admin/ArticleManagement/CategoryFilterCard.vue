<template>
  <el-card class="filter-card category-card" shadow="never">
    <template #header>
      <div class="filter-header">
        <span>文章分类</span>
        <div class="header-actions">
          <el-button link @click="clearCategoryFilter" v-if="modelValue" class="reset-link-btn">清空</el-button>
          <el-button link @click="handleRefresh" :loading="categoryLoading" class="refresh-btn">
            <el-icon><Refresh /></el-icon>
          </el-button>
        </div>
      </div>
    </template>
    <div v-loading="categoryLoading" class="category-content">
      <el-tree
        v-if="!categoryLoading && categoryTree.length > 0"
        :data="categoryTree"
        :props="treeProps"
        @node-click="handleCategoryClick"
        :highlight-current="true"
        :expand-on-click-node="false"
        node-key="path"
        ref="categoryTreeRef"
        class="category-tree"
        :current-node-key="modelValue"
      />
      <el-empty v-else-if="!categoryLoading && categoryTree.length === 0" description="暂无分类" :image-size="40" />
    </div>
  </el-card>
</template>

<script setup>
import {onMounted, ref} from 'vue'
import {Refresh} from '@element-plus/icons-vue'
import axios from 'axios'

const props = defineProps({
  modelValue: String
})

const emit = defineEmits(['update:modelValue'])

const categoryTree = ref([])
const categoryLoading = ref(false)
const categoryTreeRef = ref(null)

const treeProps = {
  children: 'children',
  label: 'label'
}

// 获取分类数据
const fetchCategories = async () => {
  categoryLoading.value = true
  try {
    const response = await axios.get('/api/articles/categories', {
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    })

    if (response.data && response.data.categories) {
      // 构建分类树
      buildCategoryTreeFromData(response.data.categories)
    }
  } catch (error) {
    console.error('获取分类数据失败:', error)
    categoryTree.value = []
  } finally {
    categoryLoading.value = false
  }
}

// 从数据库数据构建分类树
const buildCategoryTreeFromData = (categories) => {
  const root = []
  const map = new Map()

  categories.forEach(cat => {
    const pathParts = cat.path.split('/')
    let currentLevel = root
    let currentPath = ''

    pathParts.forEach((part, index) => {
      currentPath += (index > 0 ? '/' : '') + part
      let node = map.get(currentPath)

      if (!node) {
        node = {
          label: part,
          path: currentPath,
          children: [],
        }
        map.set(currentPath, node)
        currentLevel.push(node)
      }
      currentLevel = node.children
    })
  })

  categoryTree.value = root
}

// 分类点击处理
const handleCategoryClick = (data) => {
  if (props.modelValue === data.path) {
    clearCategoryFilter()
  } else {
    emit('update:modelValue', data.path)
  }
}

const clearCategoryFilter = () => {
  emit('update:modelValue', '')
  if (categoryTreeRef.value) {
    categoryTreeRef.value.setCurrentKey(null)
  }
}

// 刷新分类数据
const handleRefresh = async () => {
  await fetchCategories()
}

onMounted(() => {
  fetchCategories()
})
</script>

<style scoped>
.filter-card {
  border-radius: 12px;
  border: 1px solid #e1e8ed;
  height: 300px;
}

.category-content {
  height: 220px;
  overflow-y: auto;
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

.reset-link-btn {
  color: #666 !important;
  font-weight: normal !important;
}

.reset-link-btn:hover {
  color: #409eff !important;
  background: transparent !important;
}

.refresh-btn {
  color: #666 !important;
  font-weight: normal !important;
}

.refresh-btn:hover {
  color: #409eff !important;
  background: transparent !important;
}

.category-tree {
  background: transparent;
}

/* 自定义滚动条样式 */
.category-content::-webkit-scrollbar {
  width: 6px;
}

.category-content::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.category-content::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.category-content::-webkit-scrollbar-thumb:hover {
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

:deep(.el-tree-node__content) {
  padding: 6px 0;
}

:deep(.el-tree-node__content:hover) {
  background-color: #f5f7fa;
}
</style>

