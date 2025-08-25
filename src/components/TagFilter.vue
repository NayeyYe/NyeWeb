<template>
  <div class="tag-filter-container">
    <el-tag
      :class="{ 'is-active': activeTag === null }"
      class="tag-item"
      type="info"
      effect="light"
      @click="selectTag(null)"
    >
      全部
    </el-tag>
    <el-tag
      v-for="tag in tags"
      :key="tag"
      :class="{ 'is-active': activeTag === tag }"
      class="tag-item"
      effect="light"
      @click="selectTag(tag)"
    >
      {{ tag }}
    </el-tag>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  tags: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits(['tag-selected'])

const activeTag = ref(null)

const selectTag = (tag) => {
  activeTag.value = tag
  emit('tag-selected', tag)
}
</script>

<style scoped>
.tag-filter-container {
  margin-bottom: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag-item {
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  border: 1px solid var(--el-border-color-light);
  padding: 0 15px;
  height: 32px;
  line-height: 30px;
}

.tag-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--el-box-shadow-light);
}

.tag-item.is-active {
  background-color: var(--el-color-primary);
  color: white;
  border-color: var(--el-color-primary);
}
</style>

