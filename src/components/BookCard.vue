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
        <a :href="`/resources/book/${book.filename}`" download>
          <el-button type="primary" round>下载</el-button>
        </a>
      </div>
    </div>
  </el-card>
</template>

<script setup>
defineProps({
  book: {
    type: Object,
    required: true,
  },
});
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

