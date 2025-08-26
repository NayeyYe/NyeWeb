<template>
  <el-card class="outline-card" shadow="never">
    <template #header>
      <div class="card-header">
        <span>大纲</span>
      </div>
    </template>
    <nav>
      <ul>
        <li v-for="item in outline" :key="item.id" :class="`toc-level-${item.level}`">
          <a :href="`#${item.id}`" @click.prevent="scrollTo(item.id)">{{ item.text }}</a>
        </li>
      </ul>
    </nav>
  </el-card>
</template>

<script setup>
defineProps({
  outline: {
    type: Array,
    required: true,
  },
});

const scrollTo = (id) => {
  const element = document.getElementById(id);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' });
  }
};
</script>

<style scoped>
.outline-card {
  border-radius: 15px;
  border: 1px solid var(--el-border-color-lighter);
  position: sticky;
  top: 100px; /* Adjust based on your header height */
}

.card-header {
  font-weight: bold;
}

ul {
  list-style: none;
  padding-left: 0;
  margin: 0;
}

li {
  margin-bottom: 8px;
}

a {
  text-decoration: none;
  color: var(--el-text-color-regular);
  font-size: 14px;
  transition: color 0.2s;
}

a:hover {
  color: var(--el-color-primary);
}

/* Indent based on heading level */
.toc-level-2 { padding-left: 1em; }
.toc-level-3 { padding-left: 2em; }
.toc-level-4 { padding-left: 3em; }
.toc-level-5 { padding-left: 4em; }
.toc-level-6 { padding-left: 5em; }
</style>
