<template>
  <div class="tools-page">
    <div class="header">
      <h1>小工具箱</h1>
      <p>一些实用、有趣、能提升效率的在线小工具集合。</p>
    </div>

    <div class="filter-bar">
      <el-input
        v-model="searchQuery"
        placeholder="搜索工具..."
        clearable
        class="search-input"
        size="large"
      />
      <div class="tags-container">
        <el-tag
          :type="!selectedTag ? '' : 'info'"
          @click="selectedTag = null"
          class="tag-item"
          effect="light"
          size="large"
        >
          全部
        </el-tag>
        <el-tag
          v-for="tag in allTags"
          :key="tag"
          :type="selectedTag === tag ? '' : 'info'"
          @click="selectedTag = tag"
          class="tag-item"
          effect="light"
          size="large"
        >
          {{ tag }}
        </el-tag>
      </div>
    </div>

    <el-row :gutter="20">
      <el-col
        v-for="tool in filteredTools"
        :key="tool.title"
        :xs="24"
        :sm="12"
        :md="8"
        class="tool-col"
      >
        <ToolCard :tool="tool" />
      </el-col>
    </el-row>

    <el-empty v-if="filteredTools.length === 0" description="没有找到匹配的工具"></el-empty>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import ToolCard from '@/components/ToolCard.vue';
import toolsData from '@/data/tools.json';

const searchQuery = ref('');
const selectedTag = ref(null);

const allTags = computed(() => {
  const tags = new Set();
  toolsData.forEach(tool => {
    tool.tags.forEach(tag => tags.add(tag));
  });
  return Array.from(tags).sort();
});

const filteredTools = computed(() => {
  return toolsData.filter(tool => {
    const searchMatch =
      searchQuery.value.trim() === '' ||
      tool.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      tool.description.toLowerCase().includes(searchQuery.value.toLowerCase());

    const tagMatch =
      !selectedTag.value || tool.tags.includes(selectedTag.value);

    return searchMatch && tagMatch;
  });
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
