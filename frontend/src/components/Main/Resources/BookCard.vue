<template>
  <el-card :body-style="{ padding: '0px' }" class="book-card" shadow="hover">
    <div class="book-cover">
      <el-image :src="book.cover" class="cover-image" fit="cover"/>
    </div>
    <div class="book-info">
      <h3 class="book-title">{{ book.title }}</h3>
      <p class="book-description">{{ book.description }}</p>
      <div class="bottom-section">
        <div class="book-tags">
          <el-tag v-for="tag in book.tags" :key="tag" size="small" type="info">{{ tag }}</el-tag>
        </div>
        <el-button round type="primary" @click="downloadPdf">下载</el-button>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import {ElMessage} from 'element-plus';

const props = defineProps({
  book: {
    type: Object,
    required: true,
  },
});

const downloadPdf = () => {
  console.log('点击下载按钮，跳转到网盘链接:', props.book.filename);

  try {
    // 验证URL格式
    if (!props.book.filename || !props.book.filename.startsWith(('http://', 'https://'))) {
      ElMessage.error('无效的下载链接');
      return;
    }

    // 在新窗口打开网盘链接
    window.open(props.book.filename, '_blank');
    ElMessage.success('正在跳转到下载页面');
  } catch (error) {
    console.error('跳转失败:', error);
    ElMessage.error('跳转失败，请稍后重试');
  }
};
</script>

<style scoped>
.book-card {
  border-radius: 15px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.book-cover {
  width: 100%;
  height: 180px;
}

.cover-image {
  width: 100%;
  height: 100%;
}

.book-info {
  padding: 20px;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.book-title {
  font-size: 1.2em;
  margin: 0 0 10px 0;
}

.book-description {
  font-size: 0.9em;
  color: #606266;
  flex-grow: 1;
  margin-bottom: 15px;
}

.bottom-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.book-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
</style>
