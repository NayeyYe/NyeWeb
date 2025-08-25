<template>
  <div class="knowledge-container">
    <div class="header">
      <h1>知识文章</h1>
      <p>探索、学习、分享。这里是我关于技术、科学和思考的笔记。</p>
    </div>
    <div class="main-content">
      <aside class="timeline-sidebar">
        <ArticleTimeline :articles="filteredArticles" />
      </aside>
      <main class="articles-main">
        <div class="articles-grid">
          <TagCloud
            :articles="articles"
            :selectedTag="selectedTag"
            @tag-selected="selectTag"
          />
          <ArticleCard
            v-for="article in visibleFilteredArticles"
            :key="article.slug"
            :article="article"
          />
        </div>
        <div v-if="hasMoreArticles" class="load-more-container">
          <el-button type="primary" plain @click="loadMore">查看更多</el-button>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import ArticleTimeline from '../components/ArticleTimeline.vue';
import ArticleCard from '../components/ArticleCard.vue';
import TagCloud from '../components/TagCloud.vue';

export default {
  components: {
    ArticleTimeline,
    ArticleCard,
    TagCloud,
  },
  data() {
    return {
      articles: [],
      visibleArticles: [],
      articlesPerLoad: 5,
      selectedTag: null,
    };
  },
  mounted() {
    import('../data/articles.json').then((module) => {
      this.articles = module.default;
      this.visibleArticles = this.articles.slice(0, 5);
    });
  },
  computed: {
    filteredArticles() {
      if (!this.selectedTag) {
        return this.articles;
      }
      return this.articles.filter((article) =>
        article.tags.includes(this.selectedTag)
      );
    },
    visibleFilteredArticles() {
      return this.filteredArticles.slice(0, this.visibleArticles.length);
    },
    hasMoreArticles() {
      return this.visibleArticles.length < this.filteredArticles.length;
    },
  },
  methods: {
    loadMore() {
      const nextIndex = this.visibleArticles.length;
      const nextVisibleArticles = this.filteredArticles.slice(
        nextIndex,
        nextIndex + this.articlesPerLoad
      );
      this.visibleArticles = this.visibleArticles.concat(nextVisibleArticles);
    },
    selectTag(tag) {
      this.selectedTag = tag;
      this.visibleArticles = this.filteredArticles.slice(0, 5);
    },
  },
};
</script>

<style scoped>
.knowledge-container {
  padding: 100px 20px 20px;
  max-width: 1200px;
  margin: 0 auto;
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

.main-content {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.timeline-sidebar {
  width: 280px;
  flex-shrink: 0;
}

.articles-main {
  flex-grow: 1;
}

.articles-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.load-more-container {
  margin-top: 20px;
  text-align: center;
}
</style>
