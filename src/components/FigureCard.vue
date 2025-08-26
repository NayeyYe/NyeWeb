<template>
  <div class="figure-card">
    <el-image
      :src="`/resources/figure/${figure.filename}`"
      :preview-src-list="[`/resources/figure/${figure.filename}`]"
      :initial-index="0"
      fit="cover"
      class="figure-image"
      hide-on-click-modal
    >
      <template #placeholder>
        <div class="image-slot">加载中<span class="dot">...</span></div>
      </template>
    </el-image>
    <div class="figure-overlay">
      <div class="overlay-content">
        <p class="figure-title">{{ figure.title }}</p>
        <div class="actions">
          <el-button type="primary" circle @click="handlePreview">
            <el-icon><View /></el-icon>
          </el-button>
          <a :href="`/resources/figure/${figure.filename}`" download>
            <el-button type="success" circle>
              <el-icon><Download /></el-icon>
            </el-button>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { View, Download } from '@element-plus/icons-vue';

const props = defineProps({
  figure: {
    type: Object,
    required: true,
  },
});

// This is a bit of a trick to trigger the el-image's internal preview
const handlePreview = (event) => {
  const imageElement = event.currentTarget.closest('.figure-card').querySelector('.el-image__inner');
  if (imageElement) {
    imageElement.click();
  }
};
</script>

<style scoped>
.figure-card {
  position: relative;
  overflow: hidden;
  border-radius: 15px;
  aspect-ratio: 16 / 10;
  background-color: #f5f7fa;
}
.figure-image {
  width: 100%;
  height: 100%;
  transition: transform 0.3s ease;
}
.figure-card:hover .figure-image {
  transform: scale(1.1);
}
.figure-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  display: flex;
  align-items: flex-end;
  opacity: 0;
  transition: opacity 0.3s ease;
  padding: 15px;
  box-sizing: border-box;
}
.figure-card:hover .figure-overlay {
  opacity: 1;
}
.overlay-content {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.figure-title {
  margin: 0;
  font-weight: bold;
}
.actions {
  display: flex;
  gap: 10px;
}
.image-slot {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background: var(--el-fill-color-light);
  color: var(--el-text-color-secondary);
  font-size: 14px;
}
</style>

