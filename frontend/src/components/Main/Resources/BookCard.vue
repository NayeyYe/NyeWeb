<template>
  <el-card :body-style="{ padding: '0px' }" class="book-card" shadow="hover">
    <div class="book-cover">
      <el-image :src="book.cover" fit="cover" class="cover-image" />
    </div>
    <div class="book-info">
      <h3 class="book-title">{{ book.title }}</h3>
      <p class="book-description">{{ book.description }}</p>
      <div class="bottom-section">
        <div class="book-tags">
          <el-tag v-for="tag in book.tags" :key="tag" type="info" size="small">{{ tag }}</el-tag>
        </div>
        <el-button type="primary" round @click="downloadPdf">下载</el-button>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import {computed} from 'vue';
import {ElMessage} from 'element-plus';

const props = defineProps({
  book: {
    type: Object,
    required: true,
  },
});

// 确保文件名总是有 .pdf 后缀
const downloadFilename = computed(() => {
  return props.book.filename.endsWith('.pdf') ? props.book.filename : `${props.book.filename}.pdf`;
});

// 构建完整的下载 URL
const pdfUrl = computed(() => {
  return `/resources/book/${encodeURIComponent(downloadFilename.value)}`;
});

const downloadPdf = async () => {
  console.log('开始下载PDF:', downloadFilename.value);
  console.log('请求URL:', pdfUrl.value);

  try {
    const response = await fetch(pdfUrl.value);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // 检查响应的 Content-Type 是否为 PDF
    const contentType = response.headers.get('content-type');
    console.log('响应Content-Type:', contentType);

    if (!contentType || !contentType.includes('application/pdf')) {
      console.error('服务器返回的不是 PDF 文件，而是:', contentType);
      throw new Error('服务器返回的不是 PDF 文件');
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = downloadFilename.value;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);

    ElMessage.success('下载成功');
  } catch (error) {
    console.error('下载失败:', error);
    ElMessage.error('下载失败，请稍后重试');
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
