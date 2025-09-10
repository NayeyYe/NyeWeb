<template>
  <el-card class="carousel-card">
    <template #header>
      <div class="card-header">
        <span>我的收藏</span>
      </div>
    </template>
    <div v-loading="loading">
      <el-carousel :interval="4000" height="200px" v-if="shuffledImages.length > 0" indicator-position="none">
        <el-carousel-item v-for="image in shuffledImages" :key="image.id">
          <img :src="getImageUrl(image.filename)" class="carousel-image" alt="Favorite Image" />
        </el-carousel-item>
      </el-carousel>
      <div v-else-if="!loading" class="empty-state">
        暂无收藏图片
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

const loading = ref(false);
const imagesFromDB = ref([]);

const API_BASE_URL = '/api';

// 获取收藏图片数据
const fetchFavoriteImages = async () => {
  loading.value = true;
  try {
    const response = await axios.get(`${API_BASE_URL}/favorite-images`, {
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    });

    if (response.data && Array.isArray(response.data)) {
      imagesFromDB.value = response.data;
      console.log(`ImageCarousel: 成功获取 ${imagesFromDB.value.length} 张收藏图片`);
    }
  } catch (error) {
    console.error('ImageCarousel: 获取收藏图片数据失败:', error);
    imagesFromDB.value = [];
  } finally {
    loading.value = false;
  }
};

// 将图片数组随机打乱
const shuffledImages = computed(() => {
  return [...imagesFromDB.value].sort(() => Math.random() - 0.5);
});

// 生成图片URL
const getImageUrl = (filename) => {
  return `/favorite/${filename}`;
};

onMounted(() => {
  fetchFavoriteImages();
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
