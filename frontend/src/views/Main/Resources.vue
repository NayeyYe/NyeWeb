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
            class="search-input"
            clearable
            placeholder="搜索资源..."
        />
        <el-select
            v-model="selectedTags"
            class="tag-select"
            filterable
            multiple
            placeholder="按标签筛选"
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
      <div v-if="activeTab === 'books'">
        <el-row :gutter="20">
          <el-col
              v-for="book in filteredItems"
              :key="book.id"
              :md="8" :sm="12" :xs="24"
              class="grid-col"
          >
            <BookCard :book="book"/>
          </el-col>
        </el-row>

        <!-- 书籍分页控件 -->
        <div v-if="!loading && filteredItems.length > 0 && booksTotalPages > 1" class="pagination-container">
          <el-pagination
              v-model:current-page="booksCurrentPage"
              :page-size="booksPageSize"
              :total="booksTotalItems"
              :pager-count="5"
              layout="prev, pager, next, jumper"
              background
              @current-change="handleBooksPageChange"
          />
        </div>
      </div>

      <!-- Gallery Grid -->
      <div v-if="activeTab === 'gallery'">
        <el-row :gutter="20">
          <el-col
              v-for="figure in filteredItems"
              :key="figure.id"
              :md="8" :sm="12" :xs="24"
              class="grid-col"
          >
            <FigureCard :figure="figure"/>
          </el-col>
        </el-row>

        <!-- 图表分页控件 -->
        <div v-if="!loading && filteredItems.length > 0 && figuresTotalPages > 1" class="pagination-container">
          <el-pagination
              v-model:current-page="figuresCurrentPage"
              :page-size="figuresPageSize"
              :total="figuresTotalItems"
              :pager-count="5"
              layout="prev, pager, next, jumper"
              background
              @current-change="handleFiguresPageChange"
          />
        </div>
      </div>

      <el-empty v-if="!loading && filteredItems.length === 0" description="没有找到匹配的资源"></el-empty>
    </div>
  </div>
</template>

<script setup>
import {computed, onMounted, ref, watch} from 'vue';
import axios from 'axios';
import BookCard from '@/components/Main/Resources/BookCard.vue';
import FigureCard from '@/components/Main/Resources/FigureCard.vue';

const activeTab = ref('books');
const searchQuery = ref('');
const selectedTags = ref([]);
const loading = ref(false);

// 数据库数据
const booksFromDB = ref([]);
const bookTagsFromDB = ref([]);
const figuresFromDB = ref([]);
const figureTagsFromDB = ref([]);

// 分页状态
const booksCurrentPage = ref(1);
const booksPageSize = ref(6);
const booksTotalItems = ref(0);
const booksTotalPages = ref(0);

const figuresCurrentPage = ref(1);
const figuresPageSize = ref(6);
const figuresTotalItems = ref(0);
const figuresTotalPages = ref(0);

const API_BASE_URL = '/api';

// 获取书籍数据
const fetchBooks = async () => {
  loading.value = true;
  try {
    const response = await axios.get(`${API_BASE_URL}/books`, {
      params: {
        page: booksCurrentPage.value,
        limit: booksPageSize.value
      },
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    });

    if (response.data && response.data.data) {
      booksFromDB.value = response.data.data;
      booksTotalItems.value = response.data.pagination.total;
      booksTotalPages.value = response.data.pagination.pages;
      console.log(`Resources: 成功获取 ${booksFromDB.value.length} 本书籍，页码: ${booksCurrentPage.value}`);
    }
  } catch (error) {
    console.error('Resources: 获取书籍数据失败:', error);
    booksFromDB.value = [];
    booksTotalItems.value = 0;
    booksTotalPages.value = 0;
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
      params: {
        page: figuresCurrentPage.value,
        limit: figuresPageSize.value
      },
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    });

    if (response.data && response.data.data) {
      figuresFromDB.value = response.data.data;
      figuresTotalItems.value = response.data.pagination.total;
      figuresTotalPages.value = response.data.pagination.pages;
      console.log(`Resources: 成功获取 ${figuresFromDB.value.length} 个图表，页码: ${figuresCurrentPage.value}`);
    }
  } catch (error) {
    console.error('Resources: 获取图表数据失败:', error);
    figuresFromDB.value = [];
    figuresTotalItems.value = 0;
    figuresTotalPages.value = 0;
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

// 切换书籍页码
const handleBooksPageChange = (page) => {
  booksCurrentPage.value = page;
  fetchBooks();
};

// 切换图表页码
const handleFiguresPageChange = (page) => {
  figuresCurrentPage.value = page;
  fetchFigures();
};

// 监听activeTab变化，切换标签时获取对应数据
watch(activeTab, (newTab) => {
  if (newTab === 'books' && booksFromDB.value.length === 0) {
    booksCurrentPage.value = 1;
    fetchBooks();
  } else if (newTab === 'gallery' && figuresFromDB.value.length === 0) {
    figuresCurrentPage.value = 1;
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

.pagination-container {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}
</style>
