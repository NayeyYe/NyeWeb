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

    <div v-loading="loading" class="content-grid">
      <!-- Books Grid -->
      <el-row :gutter="20" v-if="activeTab === 'books'">
        <el-col
          v-for="book in filteredItems"
          :key="book.id"
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
          :key="figure.id"
          :xs="24" :sm="12" :md="8"
          class="grid-col"
        >
          <FigureCard :figure="figure" />
        </el-col>
      </el-row>

      <el-empty v-if="!loading && filteredItems.length === 0" description="没有找到匹配的资源"></el-empty>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import axios from 'axios';
import BookCard from '@/components/BookCard.vue';
import FigureCard from '@/components/FigureCard.vue';

const activeTab = ref('books');
const searchQuery = ref('');
const selectedTags = ref([]);
const loading = ref(false);

// 数据库数据
const booksFromDB = ref([]);
const bookTagsFromDB = ref([]);
const figuresFromDB = ref([]);
const figureTagsFromDB = ref([]);

const API_BASE_URL = 'http://localhost:8080/api';

// 获取书���数据
const fetchBooks = async () => {
  loading.value = true;
  try {
    const response = await axios.get(`${API_BASE_URL}/books`, {
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    });

    if (response.data && Array.isArray(response.data)) {
      booksFromDB.value = response.data;
      console.log(`Resources: 成功获取 ${booksFromDB.value.length} 本书籍`);
    }
  } catch (error) {
    console.error('Resources: 获取书籍数据失败:', error);
    booksFromDB.value = [];
  } finally {
    loading.value = false;
  }
};

// 获取书籍标签数据
const fetchBookTags = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/book-tags`, {
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    });

    if (response.data) {
      bookTagsFromDB.value = response.data.tags || [];
      console.log(`Resources: 成功获取 ${bookTagsFromDB.value.length} 个书籍标签`);
    }
  } catch (error) {
    console.error('Resources: 获取书籍标签数据失败:', error);
    bookTagsFromDB.value = [];
  }
};

// 获取图表数据
const fetchFigures = async () => {
  loading.value = true;
  try {
    const response = await axios.get(`${API_BASE_URL}/figures`, {
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    });

    if (response.data && Array.isArray(response.data)) {
      figuresFromDB.value = response.data;
      console.log(`Resources: 成功获取 ${figuresFromDB.value.length} 个图表`);
    }
  } catch (error) {
    console.error('Resources: 获取图表数据失败:', error);
    figuresFromDB.value = [];
  } finally {
    loading.value = false;
  }
};

// 获取图表标签数据
const fetchFigureTags = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/figure-tags`, {
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    });

    if (response.data) {
      figureTagsFromDB.value = response.data.tags || [];
      console.log(`Resources: 成功获取 ${figureTagsFromDB.value.length} 个图表标签`);
    }
  } catch (error) {
    console.error('Resources: 获取图表标签数据失败:', error);
    figureTagsFromDB.value = [];
  }
};

const allTags = computed(() => {
  const tags = new Set();
  if (activeTab.value === 'books') {
    // 使用数据库书籍数据
    booksFromDB.value.forEach(book => {
      if (book.tags) {
        book.tags.forEach(tag => tags.add(tag));
      }
    });
  } else {
    // 使用数据库图表数据
    figuresFromDB.value.forEach(figure => {
      if (figure.tags) {
        figure.tags.forEach(tag => tags.add(tag));
      }
    });
  }
  return Array.from(tags).sort();
});

const filteredItems = computed(() => {
  const sourceData = activeTab.value === 'books' ? booksFromDB.value : figuresFromDB.value;

  return sourceData.filter(item => {
    const searchMatch =
      searchQuery.value.trim() === '' ||
      item.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      item.description.toLowerCase().includes(searchQuery.value.toLowerCase());

    const tagMatch =
      selectedTags.value.length === 0 ||
      selectedTags.value.every(tag => item.tags && item.tags.includes(tag));

    return searchMatch && tagMatch;
  });
});

// 监听activeTab变化，切换标签时获取对应数据
watch(activeTab, (newTab) => {
  if (newTab === 'books' && booksFromDB.value.length === 0) {
    fetchBooks();
  } else if (newTab === 'gallery' && figuresFromDB.value.length === 0) {
    fetchFigures();
  }
  // 清空搜索和筛选
  searchQuery.value = '';
  selectedTags.value = [];
});

onMounted(async () => {
  // 默认显示书籍，所以首次加载获取书籍数据
  await Promise.all([fetchBooks(), fetchBookTags()]);
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
