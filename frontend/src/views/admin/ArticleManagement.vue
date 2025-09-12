<template>
  <div class="article-management">
    <div class="toolbar">
      <el-button type="primary" @click="openEditor('create')">新建文章</el-button>
      <el-button @click="openUploadDialog">上传文章</el-button>
      <el-button @click="showFilterDialog = true">筛选</el-button>
      <el-button @click="refreshArticles" :icon="Refresh" circle title="刷新" />
    </div>

    <!-- 筛选弹窗 -->
    <el-dialog v-model="showFilterDialog" title="筛选文章" width="500px" append-to-body>
      <el-form :model="filterForm" label-width="80px">
        <el-form-item label="分类">
          <el-tree
            :data="categoryTree"
            :props="treeProps"
            node-key="path"
            highlight-current
            :expand-on-click-node="false"
            @node-click="onCategorySelect"
            :default-expanded-keys="filterForm.category ? [filterForm.category] : []"
            style="max-height: 300px; overflow: auto;"
          />
        </el-form-item>
        <el-form-item label="标签">
          <el-select
            v-model="filterForm.tags"
            multiple
            filterable
            allow-create
            placeholder="选择标签"
            style="width: 100%"
          >
            <el-option
              v-for="tag in allTags"
              :key="tag"
              :label="tag"
              :value="tag"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="标题">
          <el-input v-model="filterForm.title" placeholder="输入标题关键字" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="resetFilter">重置</el-button>
        <el-button type="primary" @click="applyFilter">应用</el-button>
      </template>
    </el-dialog>

    <el-table :data="filteredArticles" stripe border style="margin-top: 20px;">
      <el-table-column prop="title" label="文章名字" min-width="180" />
      <el-table-column prop="slug" label="文件名字" min-width="140" />
      <el-table-column prop="date" label="创建时间" min-width="120" />
      <el-table-column label="操作" min-width="180">
        <template #default="scope">
          <el-button size="small" @click="previewArticle(scope.row)">预览</el-button>
          <el-button size="small" @click="openEditor('edit', scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="deleteArticle(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 文章编辑器 -->
    <ArticleEditor
      v-model="showEditor"
      :mode="editorMode"
      :article="currentArticle"
      @save="onEditorSave"
      @close="showEditor = false"
    />

    <!-- 上传文章对话框 -->
    <UploadArticleDialog
      v-model="showUploadDialog"
      @upload-success="refreshArticles"
    />

    <!-- 文章预览对话框 -->
    <ArticlePreviewDialog
      v-model="showPreviewDialog"
      :article="previewingArticle"
      @edit="openEditor('edit', $event)"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import axios from 'axios'
import ArticleEditor from '@/components/Admin/ArticleEditor.vue'
import UploadArticleDialog from '@/components/Admin/UploadArticleDialog.vue'
import ArticlePreviewDialog from '@/components/Admin/ArticlePreviewDialog.vue'

const articles = ref([])
const allTags = ref([])
const categoryTree = ref([])
const showEditor = ref(false)
const editorMode = ref('create')
const currentArticle = ref(null)
const showUploadDialog = ref(false)
const showPreviewDialog = ref(false)
const previewingArticle = ref(null)
const showFilterDialog = ref(false)
const filterForm = reactive({
  category: '',
  tags: [],
  title: ''
})

const treeProps = {
  children: 'children',
  label: 'label'
}

// 获取文章列表
const fetchArticles = async () => {
  const res = await axios.get('/api/articles')
  articles.value = res.data
}

// 获取标签
const fetchTags = async () => {
  const res = await axios.get('/api/tags')
  allTags.value = res.data.tags || []
}

// 获取分类树
const fetchCategories = async () => {
  const res = await axios.get('/api/articles/categories')
  categoryTree.value = convertToTree(res.data.categories)
}

// 转换为树结构
function convertToTree(categories) {
  // categories: [{ path: 'a/b', ... }]
  const root = []
  const map = new Map()
  categories.forEach(cat => {
    const parts = cat.path.split('/')
    let cur = root
    let curPath = ''
    parts.forEach((part, idx) => {
      curPath += (idx > 0 ? '/' : '') + part
      let node = map.get(curPath)
      if (!node) {
        node = { label: part, path: curPath, children: [] }
        map.set(curPath, node)
        cur.push(node)
      }
      cur = node.children
    })
  })
  return root
}

// 文章筛选
const filteredArticles = computed(() => {
  let arr = articles.value
  if (filterForm.category) {
    arr = arr.filter(a => a.category && a.category.startsWith(filterForm.category))
  }
  if (filterForm.tags && filterForm.tags.length) {
    arr = arr.filter(a => a.tags && filterForm.tags.every(tag => a.tags.includes(tag)))
  }
  if (filterForm.title) {
    arr = arr.filter(a => a.title && a.title.includes(filterForm.title))
  }
  return arr
})

// 分类树节点点击
const onCategorySelect = (node) => {
  filterForm.category = node.path
}

// 筛选弹窗操作
const resetFilter = () => {
  filterForm.category = ''
  filterForm.tags = []
  filterForm.title = ''
}
const applyFilter = () => {
  showFilterDialog.value = false
}

// 文章操作
const openEditor = (mode, article = null) => {
  editorMode.value = mode
  currentArticle.value = article
  showEditor.value = true
}
const openUploadDialog = () => {
  showUploadDialog.value = true
}
const previewArticle = (article) => {
  previewingArticle.value = article
  showPreviewDialog.value = true
}
const deleteArticle = async (article) => {
  try {
    await ElMessageBox.confirm('确定要删除该文章吗？', '提示', { type: 'warning' })
    await axios.delete(`/api/articles/${article.id}`)
    ElMessage.success('删除成功')
    refreshArticles()
  } catch {}
}
const onEditorSave = () => {
  showEditor.value = false
  refreshArticles()
}
const refreshArticles = () => {
  fetchArticles()
  fetchTags()
  fetchCategories()
}

// 初始化
onMounted(() => {
  refreshArticles()
})
</script>

<style scoped>
.article-management {
  padding: 20px;
}
.toolbar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}
</style>
