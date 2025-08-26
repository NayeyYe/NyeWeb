<template>
  <a :href="tool.url" target="_blank" rel="noopener noreferrer" class="tool-card-link">
    <el-card class="tool-card" shadow="hover">
      <div class="card-content">
        <h3 class="tool-title">{{ tool.title }}</h3>
        <p class="tool-description">{{ tool.description }}</p>
        <div class="tool-tags">
          <el-tag
            v-for="tag in tool.tags"
            :key="tag"
            type="info"
            size="small"
            class="tool-tag"
          >
            {{ tag }}
          </el-tag>
        </div>
      </div>
    </el-card>
  </a>
</template>

<script setup>
defineProps({
  tool: {
    type: Object,
    required: true,
    validator: (value) => {
      return (
        typeof value.title === 'string' &&
        typeof value.description === 'string' &&
        Array.isArray(value.tags) &&
        typeof value.url === 'string'
      );
    },
  },
});
</script>

<style scoped>
.tool-card-link {
  text-decoration: none;
  color: inherit;
  display: block;
  height: 100%;
}

.tool-card {
  border-radius: 15px;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
  height: 100%;
}

.tool-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--el-box-shadow-light);
}

.card-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.tool-title {
  font-size: 1.2em;
  font-weight: bold;
  margin: 0 0 10px 0;
}

.tool-description {
  font-size: 0.9em;
  color: var(--el-text-color-secondary);
  flex-grow: 1; /* Pushes tags to the bottom */
  margin-bottom: 15px;
}

.tool-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tool-tag {
  background-color: #f0f2f5;
  border-color: #e0e2e5;
  color: #606266;
}
</style>
