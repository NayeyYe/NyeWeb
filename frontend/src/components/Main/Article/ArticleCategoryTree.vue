<template>
  <el-card class="category-tree-card" shadow="never">
    <template #header>
      <div class="card-header">
        <span>文章归档</span>
        <div class="header-actions">
          <el-button v-if="currentKey" link type="primary" @click="clearFilter">清空</el-button>
          <el-button v-if="showCollapseButton" class="collapse-button" link @click="handleCollapse">
            <el-icon>
              <Fold />
            </el-icon>
          </el-button>
        </div>
      </div>
    </template>
    <div v-loading="loading">
      <el-tree
          v-if="!loading && categoryTree.length > 0"
          ref="treeRef"
          :data="categoryTree"
          :expand-on-click-node="false"
          :highlight-current="true"
          :props="treeProps"
          node-key="path"
          @node-click="handleNodeClick"
      >
        <template #default="{ node, data }">
          <div class="tree-node">
            <el-icon v-if="data.type === 'category'" class="node-icon">
              <Folder />
            </el-icon>
            <el-icon v-else-if="data.type === 'article'" class="node-icon">
              <Document />
            </el-icon>
            <span class="node-label" :class="{ 'article-node': data.type === 'article' }">
              {{ data.label }}
            </span>
            <span v-if="data.type === 'category' && data.count > 0" class="article-count">
              ({{ data.count }})
            </span>
          </div>
        </template>
      </el-tree>
      <el-empty v-else-if="!loading && categoryTree.length === 0" :image-size="60" description="暂无分类数据">
      </el-empty>
    </div>
  </el-card>
</template>

<script setup>
import {computed, onMounted, ref, watch} from 'vue'
import axios from 'axios'
import {Fold, Folder, Document} from '@element-plus/icons-vue'

const props = defineProps({
  articles: {
    type: Array,
    required: true,
  },
  showCollapseButton: {
    type: Boolean,
    default: false,
  },
  showArticles: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['category-selected', 'collapse', 'article-selected'])

const loading = ref(false)
const categoriesFromDB = ref([])
const treeRef = ref(null)
const currentKey = ref(null)

const API_BASE_URL = '/api'

const treeProps = {
  children: 'children',
  label: 'label',
}

// 获取数据库中的分类数据
const fetchCategories = async () => {
  loading.value = true
  try {
    const response = await axios.get(`${API_BASE_URL}/articles/categories`, {
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    })

    if (response.data && response.data.categories) {
      categoriesFromDB.value = response.data.categories
      console.log(`成功获取 ${categoriesFromDB.value.length} 个分类`)
    }
  } catch (error) {
    console.error('获取分类数据失败:', error)
    categoriesFromDB.value = []
  } finally {
    loading.value = false
  }
}

// 构建分类树
const categoryTree = computed(() => {
  const articlesToProcess = categoriesFromDB.value.length > 0
      ? categoriesFromDB.value.flatMap(cat => (cat.articles || []).map(article => ({...article, category: cat.path})))
      : props.articles

  const root = []
  const map = new Map()

  // 先处理分类结构
  categoriesFromDB.value.forEach(cat => {
    if (!cat.path) return

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
          type: 'category',
          count: cat.count || 0,
          children: [],
        }
        map.set(currentPath, node)
        currentLevel.push(node)
      } else {
        // 更新计数
        node.count = cat.count || 0
      }
      currentLevel = node.children
    })

    // 如果需要显示文章节点，添加文章
    if (props.showArticles && cat.articles) {
      const categoryNode = map.get(cat.path)
      if (categoryNode) {
        cat.articles.forEach(article => {
          categoryNode.children.push({
            label: article.title || article.slug,
            path: `${cat.path}/${article.slug}`,
            type: 'article',
            slug: article.slug,
            category: cat.path,
            title: article.title,
            summary: article.summary,
            date: article.date,
          })
        })
      }
    }
  })

  console.log('构建的分类树:', root)
  return root
})

const handleNodeClick = (data) => {
  // 处理文章节点点击
  if (data.type === 'article') {
    currentKey.value = data.path
    if (treeRef.value) {
      treeRef.value.setCurrentKey(data.path)
    }
    emit('article-selected', {
      category: data.category,
      slug: data.slug,
      title: data.title
    })
    return
  }

  // 处理分类节点点击
  if (currentKey.value === data.path) {
    clearFilter()
  } else {
    currentKey.value = data.path
    if (treeRef.value) {
      treeRef.value.setCurrentKey(data.path)
    }
    emit('category-selected', data.path)
  }
}

const clearFilter = () => {
  currentKey.value = null
  if (treeRef.value) {
    treeRef.value.setCurrentKey(null)
  }
  emit('category-selected', null)
}

const handleCollapse = () => {
  emit('collapse')
}

// 监听articles变化，当articles数据更新时重新获取分类
watch(() => props.articles, (newArticles) => {
  if (newArticles && newArticles.length > 0 && categoriesFromDB.value.length === 0) {
    // 如果还没有从数据库获取到数据，且有新的文章数据，则尝试重新获取
    fetchCategories()
  }
}, {immediate: true})

onMounted(() => {
  fetchCategories()
})
</script>

<style scoped>
.category-tree-card {
  border-radius: 15px;
  border: 1px solid var(--el-border-color-lighter);
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.collapse-button {
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.el-tree {
  background: transparent;
}

.tree-node {
  display: flex;
  align-items: center;
  gap: 6px;
  width: 100%;
}

.node-icon {
  font-size: 14px;
  color: var(--el-text-color-regular);
}

.node-label {
  flex: 1;
  font-size: 14px;
}

.node-label.article-node {
  color: var(--el-text-color-regular);
  font-weight: normal;
}

.article-count {
  font-size: 12px;
  color: var(--el-text-color-placeholder);
  margin-left: auto;
}

:deep(.el-tree-node__content) {
  height: auto;
  min-height: 26px;
  padding: 4px 0;
}

:deep(.el-tree-node__content:hover) {
  background-color: var(--el-color-primary-light-9);
}

:deep(.el-tree-node.is-current > .el-tree-node__content) {
  background-color: var(--el-color-primary-light-8);
  color: var(--el-color-primary);
}
</style>
