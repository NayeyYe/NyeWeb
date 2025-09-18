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
            :type="!selectedTag ? '' : 'info'"
            class="tag-item"
            effect="light"
            size="large"
            @click="selectedTag = null"
        >
          全部
        </el-tag>
        <el-tag
            v-for="tag in allTags"
            :key="tag"
            :type="selectedTag === tag ? '' : 'info'"
            class="tag-item"
            effect="light"
            size="large"
            @click="selectedTag = tag"
        >
          {{ tag }}
        </el-tag>
      </div>
    </div>

    <div v-loading="loading">
      <el-row :gutter="20">
        <el-col
            v-for="tool in filteredTools"
            :key="tool.id"
            :md="8"
            :sm="12"
            :xs="24"
            class="tool-col"
        >
          <ToolCard :tool="tool"/>
        </el-col>
      </el-row>

      <el-empty v-if="!loading && filteredTools.length === 0" description="没有找到匹配的工具"></el-empty>
    </div>
  </div>
</template>

<script setup>
import {computed, onMounted, ref} from 'vue';
import axios from 'axios';
import ToolCard from '@/components/Main/Tools/ToolCard.vue';

const searchQuery = ref('');
const selectedTag = ref(null);
const loading = ref(false);
const toolsFromDB = ref([]);

const API_BASE_URL = '/api';

// 获取工具数据
const fetchTools = async () => {
  loading.value = true;
  try {
    const response = await axios.get(`${API_BASE_URL}/tools`, {
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    });

    if (response.data && Array.isArray(response.data)) {
      toolsFromDB.value = response.data;
      console.log(`Tools: 成功获取 ${toolsFromDB.value.length} 个工具`);
    }
  } catch (error) {
    console.error('Tools: 获取工具数据失败:', error);
    toolsFromDB.value = [];
  } finally {
    loading.value = false;
  }
};

const allTags = computed(() => {
  const tags = new Set();
  toolsFromDB.value.forEach(tool => {
    if (tool.tags) {
      tool.tags.forEach(tag => tags.add(tag));
    }
  });
  return Array.from(tags).sort();
});

const filteredTools = computed(() => {
  return toolsFromDB.value.filter(tool => {
    const searchMatch =
        searchQuery.value.trim() === '' ||
        tool.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        tool.description.toLowerCase().includes(searchQuery.value.toLowerCase());

    const tagMatch =
        !selectedTag.value || (tool.tags && tool.tags.includes(selectedTag.value));

    return searchMatch && tagMatch;
  });
});

onMounted(() => {
  fetchTools();
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
</style>
