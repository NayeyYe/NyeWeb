<template>
  <div class="tools-page">
    <div class="header">
      <h1>小工具箱</h1>
      <p>一些实用、有趣、能提升效率的在线小工具集合。</p>
    </div>

    <div class="filter-bar">
      <el-input
          v-model="searchQuery"
          class="search-input"
          clearable
          placeholder="搜索工具..."
          size="large"
      />
      <div class="tags-container">
        <el-tag
            :type="selectedTags.length === 0 ? '' : 'info'"
            class="tag-item"
            effect="light"
            size="large"
            @click="selectedTags = []"
        >
          全部
        </el-tag>
        <el-tag
            v-for="tag in allTags"
            :key="tag"
            :type="selectedTags.includes(tag) ? '' : 'info'"
            class="tag-item"
            effect="light"
            size="large"
            @click="toggleTag(tag)"
        >
          {{ tag }}
        </el-tag>
      </div>
    </div>

    <div v-loading="loading">
      <el-row :gutter="20">
        <el-col
            v-for="tool in displayedTools"
            :key="tool.id"
            :md="8"
            :sm="12"
            :xs="24"
            class="tool-col"
        >
          <ToolCard :tool="tool"/>
        </el-col>
      </el-row>

      <el-empty v-if="!loading && displayedTools.length === 0" description="没有找到匹配的工具"></el-empty>

      <!-- 分页控件 -->
      <div v-if="!loading && displayedTools.length > 0 && totalPages > 1" class="pagination-container">
        <el-pagination
            v-model:current-page="currentPage"
            :page-size="pageSize"
            :total="totalItems"
            :pager-count="5"
            layout="prev, pager, next, jumper"
            background
            @current-change="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import {computed, onMounted, ref, watch} from 'vue';
import axios from 'axios';
import ToolCard from '@/components/Main/Tools/ToolCard.vue';

const searchQuery = ref('');
const selectedTags = ref([]);
const loading = ref(false);
const toolsFromDB = ref([]);

const API_BASE_URL = '/api';

// 分页状态
const currentPage = ref(1);
const pageSize = ref(6);
const totalItems = ref(0);
const totalPages = ref(0);

// 获取工具数据
const fetchTools = async () => {
  loading.value = true;
  try {
    const params = {
      page: currentPage.value,
      limit: pageSize.value
    };
    
    // 添加搜索参数
    if (searchQuery.value.trim()) {
      params.search = searchQuery.value.trim();
    }
    
    // 添加标签参数
    if (selectedTags.value.length > 0) {
      params.tags = selectedTags.value.join(',');
    }

    const response = await axios.get(`${API_BASE_URL}/tools`, {
      params: params,
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    });

    if (response.data && response.data.data) {
      toolsFromDB.value = response.data.data;
      totalItems.value = response.data.pagination.total;
      totalPages.value = response.data.pagination.pages;
      console.log(`Tools: 成功获取 ${toolsFromDB.value.length} 个工具，页码: ${currentPage.value}`);
    }
  } catch (error) {
    console.error('Tools: 获取工具数据失败:', error);
    toolsFromDB.value = [];
    totalItems.value = 0;
    totalPages.value = 0;
  } finally {
    loading.value = false;
  }
};

// 切换页码
const handlePageChange = (page) => {
  currentPage.value = page;
  fetchTools();
};

// 监听搜索和标签变化，重新获取数据
watch([searchQuery, selectedTags], () => {
  // 重置到第一页
  currentPage.value = 1;
  fetchTools();
});

// 获取所有工具标签
const allTags = ref([]);
const fetchToolTags = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/tool-tags`, {
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    });
    
    if (response.data && response.data.tags) {
      allTags.value = response.data.tags.sort();
      console.log(`Tools: 成功获取 ${allTags.value.length} 个工具标签`);
    }
  } catch (error) {
    console.error('Tools: 获取工具标签失败:', error);
    allTags.value = [];
  }
};

// 直接使用API返回的数据（筛选已在后端完成）
const displayedTools = computed(() => {
  return toolsFromDB.value;
});

// 切换标签选择状态
const toggleTag = (tag) => {
  const index = selectedTags.value.indexOf(tag);
  if (index === -1) {
    // 添加标签
    selectedTags.value.push(tag);
  } else {
    // 移除标签
    selectedTags.value.splice(index, 1);
  }
};

onMounted(() => {
  fetchTools();
  fetchToolTags();
});
</script>

<style scoped>
.tools-page {
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

.filter-bar {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 40px;
  padding: 20px;
  background-color: #fff;
  border-radius: 15px;
  border: 1px solid var(--el-border-color-lighter);
}

.search-input {
  max-width: 400px;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag-item {
  cursor: pointer;
  user-select: none;
}

.tool-col {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}
</style>
