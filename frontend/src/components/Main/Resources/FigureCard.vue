<template>
  <div class="figure-card">
    <el-image
        :src="figure.url"
        class="figure-image"
        fit="cover"
    >
      <template #placeholder>
        <div class="image-slot">加载中<span class="dot">...</span></div>
      </template>
    </el-image>
    <div class="figure-overlay">
      <div class="overlay-content">
        <p class="figure-title">{{ figure.title }}</p>
        <div class="actions">
          <el-button circle type="primary" @click="handlePreview">
            <el-icon>
              <View/>
            </el-icon>
          </el-button>
          <a :href="figure.url" download target="_blank">
            <el-button circle type="success">
              <el-icon>
                <Download/>
              </el-icon>
            </el-button>
          </a>
        </div>
      </div>
    </div>
    <el-image-viewer
        v-if="showViewer"
        :initial-index="0"
        :url-list="[figure.url]"
        @close="showViewer = false"
    />
  </div>
</template>

<script setup>
import {ref} from 'vue';
import {Download, View} from '@element-plus/icons-vue';

const props = defineProps({
  figure: {
    type: Object,
    required: true,
  },
});

const showViewer = ref(false);

const handlePreview = () => {
  showViewer.value = true;
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
