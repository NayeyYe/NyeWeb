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
          <a
              :class="{ 'is-active': item.id === activeId }"
              :href="`#${item.id}`"
              @click.prevent="scrollTo(item.id)"
          >{{ item.text }}</a>
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
  activeId: {
    type: String,
    default: '',
  },
});

const scrollTo = (id) => {
  const element = document.getElementById(id);
  if (element) {
    // 计算固定头部的高度偏移
    const headerHeight = 55; // 头部实际高度为55px
    const elementPosition = element.getBoundingClientRect().top + window.pageYOffset;
    const offsetPosition = elementPosition - headerHeight;

    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    });
  }
};
</script>

<style scoped>
.outline-card {
  border-radius: 15px;
  border: 1px solid var(--el-border-color-lighter);
  max-height: calc(100vh - 120px); /* 限制最大高度，120px是顶部和底部的留白 */
  display: flex;
  flex-direction: column;
}

.outline-card :deep(.el-card__body) {
  overflow-y: auto;
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
  display: block;
  padding: 2px 0;
}

a:hover {
  color: var(--el-color-primary);
}

a.is-active {
  color: var(--el-color-primary);
  font-weight: bold;
  background-color: var(--el-color-primary-light-9);
  border-radius: 4px;
  padding-left: 5px;
  margin-left: -5px;
}

/* Indent based on heading level */
.toc-level-2 {
  padding-left: 1em;
}

.toc-level-3 {
  padding-left: 2em;
}

.toc-level-4 {
  padding-left: 3em;
}

.toc-level-5 {
  padding-left: 4em;
}

.toc-level-6 {
  padding-left: 5em;
}
</style>
