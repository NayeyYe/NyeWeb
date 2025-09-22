<template>
  <el-card class="filter-card category-card" shadow="never">
    <template #header>
      <div class="filter-header">
        <span>文章分类</span>
        <div class="header-actions">
          <el-button v-if="modelValue" class="reset-link-btn" link @click="clearCategoryFilter">清空</el-button>
          <el-button :loading="categoryLoading" class="refresh-btn" link @click="handleRefresh">
            <el-icon>
              <Refresh/>
            </el-icon>
          </el-button>
        </div>
      </div>
    </template>
    <div v-loading="categoryLoading" class="category-content">
      <el-tree
          v-if="!categoryLoading && categoryTree.length > 0"
          ref="categoryTreeRef"
          :current-node-key="modelValue"
          :data="categoryTree"
          :expand-on-click-node="false"
          :highlight-current="true"
          :props="treeProps"
          class="category-tree"
          node-key="path"
          @node-click="handleCategoryClick"
      />
      <el-empty v-else-if="!categoryLoading && categoryTree.length === 0" :image-size="40" description="暂无分类"/>
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
  if (!categories || categories.length === 0) {
    categoryTree.value = []
    return
  }

  // 过滤掉错误的分类数据
  const validCategories = categories.filter(cat =>
      cat.path &&
      cat.path !== "请先创建分类文件夹" &&
      cat.path !== "error" &&
      !cat.path.includes("请先创建")
  )

  if (validCategories.length === 0) {
    categoryTree.value = []
    return
  }

  const root = []
  const map = new Map()

  // 收集所有路径段
  const allPaths = new Set()

  validCategories.forEach(category => {
    if (!category.path) return

    const pathParts = category.path.split('/')
    let currentPath = ''

    // 为每个路径段创建完整路径
    pathParts.forEach((part, index) => {
      if (!part.trim()) return // 跳过空路径段

      const parentPath = currentPath
      currentPath = currentPath ? `${currentPath}/${part}` : part
      allPaths.add(currentPath)
    })
  })

  // 按路径长度排序，确保父节点先创建
  const sortedPaths = Array.from(allPaths).sort((a, b) => {
    const aDepth = a.split('/').length
    const bDepth = b.split('/').length
    if (aDepth !== bDepth) return aDepth - bDepth
    return a.localeCompare(b)
  })

  // 创建所有节点
  const nodeMap = new Map()

  sortedPaths.forEach(fullPath => {
    if (!nodeMap.has(fullPath)) {
      const pathParts = fullPath.split('/')
      const label = pathParts[pathParts.length - 1]
      const parentPath = pathParts.slice(0, -1).join('/')

      const node = {
        path: fullPath,
        label: label,
        children: []
      }

      nodeMap.set(fullPath, node)

      // 找到父节点并添加到其children中
      if (parentPath && nodeMap.has(parentPath)) {
        const parentNode = nodeMap.get(parentPath)
        if (!parentNode.children.find(child => child.path === fullPath)) {
          parentNode.children.push(node)
        }
      } else if (!parentPath) {
        // 根节点
        if (!root.find(child => child.path === fullPath)) {
          root.push(node)
        }
      }
    }
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

/* 响应式布局优化 */
@media (max-width: 768px) {
  .filter-card {
    height: 250px;
  }
  
  .category-content {
    height: 170px;
  }
  
  :deep(.el-card__header) {
    padding: 12px 15px;
  }
  
  :deep(.el-card__body) {
    padding: 15px;
  }
}

@media (max-width: 480px) {
  .filter-card {
    height: 220px;
  }
  
  .category-content {
    height: 140px;
  }
  
  .filter-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .header-actions {
    align-self: flex-end;
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
