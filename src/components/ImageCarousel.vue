<template>
  <el-card class="carousel-card">
    <template #header>
      <div class="card-header">
        <span>我的收藏</span>
      </div>
    </template>
    <el-carousel :interval="4000" height="200px" v-if="shuffledImages.length > 0" indicator-position="none">
      <el-carousel-item v-for="image in shuffledImages" :key="image">
        <img :src="image" class="carousel-image" alt="Favorite Image" />
      </el-carousel-item>
    </el-carousel>
    <div v-else class="empty-state">
      暂无收藏图片
    </div>
  </el-card>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const allImages = ref([]);

onMounted(async () => {
  try {
    const response = await fetch('/favoriteImages.json');
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const imageFilenames = await response.json();
    // 将文件名列表转换为完整的图片路径列表
    allImages.value = imageFilenames.map(filename => `/favorite/${filename}`);
  } catch (error) {
    console.error('Failed to load favorite images manifest:', error);
    allImages.value = []; // 出错时清空数组
  }
});


// 将图片数组随机打乱
const shuffledImages = computed(() => {
  return [...allImages.value].sort(() => Math.random() - 0.5);
});

</script>

<style scoped>
.carousel-card {
  width: 100%;
}

.card-header span {
  font-weight: bold;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 6px;
}

.el-carousel__item:nth-child(2n) {
  background-color: #f0f2f5;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #e9e9eb;
}

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  color: #909399;
  background-color: #f5f7fa;
  border-radius: 6px;
}
</style>
