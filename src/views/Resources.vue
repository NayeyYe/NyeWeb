<template>
  <div class="resources-page">
    <div class="header">
      <h1>资源中心</h1>
      <p>精心整理的书籍、图库和其他学习资源，助你更上一层楼。</p>
    </div>

    <div class="controls-container">
      <el-radio-group v-model="activeTab" size="large">
        <el-radio-button label="books">书籍</el-radio-button>
        <el-radio-button label="gallery">图库</el-radio-button>
      </el-radio-group>

      <div class="filter-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索资源..."
          clearable
          class="search-input"
        />
        <el-select
          v-model="selectedTags"
          multiple
          filterable
          placeholder="按标签筛选"
          class="tag-select"
        >
          <el-option
            v-for="tag in allTags"
            :key="tag"
            :label="tag"
            :value="tag"
          />
        </el-select>
      </div>
    </div>

    <div class="content-grid">
      <!-- Books Grid -->
      <el-row :gutter="20" v-if="activeTab === 'books'">
        <el-col
          v-for="book in filteredItems"
          :key="book.title"
          :xs="24" :sm="12" :md="8"
          class="grid-col"
        >
          <BookCard :book="book" />
        </el-col>
      </el-row>

      <!-- Gallery Grid -->
      <el-row :gutter="20" v-if="activeTab === 'gallery'">
        <el-col
          v-for="figure in filteredItems"
          :key="figure.title"
          :xs="24" :sm="12" :md="8"
          class="grid-col"
        >
          <FigureCard :figure="figure" />
        </el-col>
      </el-row>

      <el-empty v-if="filteredItems.length === 0" description="没有找到匹配的资源"></el-empty>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import BookCard from '@/components/BookCard.vue';
import FigureCard from '@/components/FigureCard.vue';
import booksData from '@/data/books.json';
import figuresData from '@/data/figures.json';

const activeTab = ref('books');
const searchQuery = ref('');
const selectedTags = ref([]);

const allTags = computed(() => {
  const tags = new Set();
  const currentData = activeTab.value === 'books' ? booksData : figuresData;
  currentData.forEach(item => {
    item.tags.forEach(tag => tags.add(tag));
  });
  return Array.from(tags).sort();
});

const filteredItems = computed(() => {
  const sourceData = activeTab.value === 'books' ? booksData : figuresData;

  return sourceData.filter(item => {
    const searchMatch =
      searchQuery.value.trim() === '' ||
      item.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      item.description.toLowerCase().includes(searchQuery.value.toLowerCase());

    const tagMatch =
      selectedTags.value.length === 0 ||
      selectedTags.value.every(tag => item.tags.includes(tag));

    return searchMatch && tagMatch;
  });
});
</script>

<style scoped>
.resources-page {
  max-width: 1200px;
  margin: 100px auto 40px;
  padding: 0 20px;
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

.header h1 {
  font-size: 2.5em;
  margin-bottom: 10px;
}

.header p {
  font-size: 1.1em;
  color: #606266;
}

.controls-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 40px;
}

.filter-bar {
  display: flex;
  gap: 15px;
  flex-grow: 1;
  justify-content: flex-end;
}

.search-input {
  max-width: 250px;
}

.tag-select {
  max-width: 300px;
  width: 100%;
}

.content-grid {
  min-height: 300px;
}

.grid-col {
  margin-bottom: 20px;
}
</style>

