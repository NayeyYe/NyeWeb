<template>
  <el-card shadow="never">
    <template #header>
      <div class="list-header">
        <span>文章列表</span>
        <span class="article-count">共 {{ articles.length }} 篇文章</span>
      </div>
    </template>
    <el-table
        :data="articles"
        :header-cell-style="{ background: '#fafafa', color: '#333', fontWeight: '600' }"
        class="article-table"
        empty-text="暂无文章数据"
        stripe
    >
      <el-table-column label="文章标题" min-width="200" prop="title" show-overflow-tooltip>
        <template #default="scope">
          <div class="article-title">{{ scope.row.title }}</div>
        </template>
      </el-table-column>
      <el-table-column label="文件名" min-width="150" prop="slug" show-overflow-tooltip>
        <template #default="scope">
          <div class="article-slug">{{ scope.row.slug }}</div>
        </template>
      </el-table-column>
      <el-table-column label="分类" min-width="120" prop="category" show-overflow-tooltip>
        <template #default="scope">
          <span v-if="scope.row.category" class="article-category">{{ scope.row.category }}</span>
          <span v-else class="no-category">未分类</span>
        </template>
      </el-table-column>
      <el-table-column label="标签" min-width="150" prop="tags" show-overflow-tooltip>
        <template #default="scope">
          <div v-if="scope.row.tags && scope.row.tags.length > 0" class="article-tags">
            <el-tag
                v-for="tag in scope.row.tags.slice(0, 3)"
                :key="tag"
                class="tag-item"
                size="small"
                type="info"
            >
              {{ tag }}
            </el-tag>
            <span v-if="scope.row.tags.length > 3" class="more-tags">+{{ scope.row.tags.length - 3 }}</span>
          </div>
          <span v-else class="no-tags">暂无标签</span>
        </template>
      </el-table-column>
      <el-table-column align="center" label="状态" min-width="120" prop="status">
        <template #default="scope">
          <el-select
              :model-value="scope.row.status"
              size="small"
              style="width: 100px"
              @change="(value) => $emit('update-status', scope.row, value)"
          >
            <el-option label="草稿" value="draft"/>
            <el-option label="已发布" value="published"/>
            <el-option label="已回收" value="recycled"/>
          </el-select>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" min-width="120" prop="date">
        <template #default="scope">
          <div class="article-date">{{ formatDate(scope.row.date) }}</div>
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" min-width="200">
        <template #default="scope">
          <div class="action-buttons-table">
            <el-button size="small" type="primary" @click="$emit('edit', scope.row)">编辑</el-button>
            <el-button
                v-if="scope.row.status !== 'recycled'"
                size="small"
                type="warning"
                @click="$emit('quick-update-status', scope.row, 'recycled')"
            >
              回收
            </el-button>
            <el-button
                v-if="scope.row.status === 'recycled'"
                size="small"
                type="success"
                @click="$emit('quick-update-status', scope.row, 'published')"
            >
              恢复
            </el-button>
            <el-button size="small" type="danger" @click="$emit('delete', scope.row)">删除</el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup>
defineProps({
  articles: Array
})

defineEmits(['update-status', 'quick-update-status', 'delete', 'edit'])

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}
</script>

<style scoped>
.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  color: #333;
}

.article-count {
  color: #666;
  font-size: 14px;
  font-weight: normal;
}

.article-table {
  border-radius: 8px;
  overflow: hidden;
}

.article-title {
  font-weight: 500;
  color: #333;
}

.article-slug {
  font-family: 'Monaco', 'Consolas', monospace;
  color: #666;
  font-size: 13px;
}

.article-category {
  color: #666;
}

.article-tags {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 4px;
}

.tag-item {
  margin: 0;
}

.more-tags {
  color: #999;
  font-size: 12px;
  margin-left: 4px;
}

.no-tags {
  color: #999;
  font-style: italic;
}

.article-date {
  color: #666;
  font-size: 13px;
}

.no-category {
  color: #999;
  font-style: italic;
}

.action-buttons-table {
  display: flex;
  gap: 6px;
  justify-content: center;
  flex-wrap: wrap;
}

.action-buttons-table .el-button {
  margin: 2px 0;
}

:deep(.el-card__header) {
  padding: 16px 20px;
  background: #fafafa;
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-card__body) {
  padding: 20px;
}

:deep(.el-table th) {
  background: #fafafa !important;
}

/* 状态下拉框样式 */
:deep(.el-select .el-input__inner) {
  text-align: center;
  padding: 0 8px;
}

:deep(.el-select--small .el-input__inner) {
  height: 28px;
  line-height: 28px;
}
</style>

