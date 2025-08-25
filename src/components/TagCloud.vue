<template>
  <el-card class="tag-cloud">
    <template #header>
      <div class="card-header">
        <span>标签云</span>
      </div>
    </template>
    <el-tag
      v-for="tag in tags"
      :key="tag"
      class="tag-item"
      @click="emit('tag-selected', tag)"
    >
      {{ tag }}
    </el-tag>
  </el-card>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  articles: {
    type: Array,
    required: true,
  },
  selectedTag: {
    type: String,
    default: null,
  },
});

const emit = defineEmits(['tag-selected']);

const tags = computed(() => {
  const tagSet = new Set();
  props.articles.forEach((article) => {
    article.tags.forEach((tag) => {
      tagSet.add(tag);
    });
  });
  return Array.from(tagSet);
});
</script>

<style scoped>
.tag-cloud {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tag-item {
  margin: 4px;
  cursor: pointer;
}
</style>
