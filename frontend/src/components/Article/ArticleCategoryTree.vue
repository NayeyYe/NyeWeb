<template>
  <el-card class="category-tree-card" shadow="never">
    <template #header>
      <div class="card-header">
        <span>文章归档</span>
        <el-button link type="primary" @click="clearFilter" v-if="currentKey">清空</el-button>
      </div>
    </template>
    <div v-loading="loading">
      <el-tree
        v-if="!loading && categoryTree.length > 0"
        :data="categoryTree"
        :props="treeProps"
        @node-click="handleNodeClick"
        :highlight-current="true"
        :expand-on-click-node="false"
        node-key="path"
        ref="treeRef"
      />
      <el-empty v-else-if="!loading && categoryTree.length === 0" description="暂无分类数据" :image-size="60">
      </el-empty>
    </div>
  </el-card>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'

const props = defineProps({
  articles: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits(['category-selected'])

const loading = ref(false)
const categoriesFromDB = ref([])
const treeRef = ref(null)
const currentKey = ref(null)

const API_BASE_URL = 'http://localhost:8080/api'

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
  // 优先使用数据库数据，如果没有则使用传入的articles数据作为备用
  const articlesToProcess = categoriesFromDB.value.length > 0
    ? categoriesFromDB.value.flatMap(cat => cat.articles.map(article => ({ ...article, category: cat.path })))
    : props.articles

  const root = []
  const map = new Map()

  articlesToProcess.forEach(article => {
    if (!article.category) return

    const pathParts = article.category.split('/')
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

  console.log('构建的分类树:', root)
  return root
})

const handleNodeClick = (data) => {
  // 如果点击的是当前已选中的节点，则取消选择
  if (currentKey.value === data.path) {
    clearFilter()
  } else {
    currentKey.value = data.path
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

// 监听articles变化，当articles数据更新时重新获取分类
watch(() => props.articles, (newArticles) => {
  if (newArticles && newArticles.length > 0 && categoriesFromDB.value.length === 0) {
    // 如果还没有从数据库获取到数据，且有新的文章数据，则尝试重新获取
    fetchCategories()
  }
}, { immediate: true })

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

.el-tree {
  background: transparent;
}
</style>
