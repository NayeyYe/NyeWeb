<template>
  <el-card class="category-tree-card" shadow="never">
    <template #header>
      <div class="card-header">
        <span>文章归档</span>
        <el-button link type="primary" @click="clearFilter" v-if="currentKey">清空</el-button>
      </div>
    </template>
    <el-tree
      :data="categoryTree"
      :props="treeProps"
      @node-click="handleNodeClick"
      :highlight-current="true"
      :expand-on-click-node="false"
      node-key="path"
      ref="treeRef"
    />
  </el-card>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  articles: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits(['category-selected'])

const treeRef = ref(null)
const currentKey = ref(null)

const treeProps = {
  children: 'children',
  label: 'label',
}

const categoryTree = computed(() => {
  const root = []
  const map = new Map()

  props.articles.forEach(article => {
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
