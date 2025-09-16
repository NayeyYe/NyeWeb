<template>
  <div class="favorite-images-editor">
    <el-card class="editor-card" shadow="never">
      <template #header>
        <div class="header">
          <span>最喜欢的图片编辑</span>
          <div class="header-actions">
            <el-button @click="refreshImages" :icon="Refresh" circle size="small" />
            <el-button @click="saveImages" type="primary" size="small" :loading="saving">
              保存
            </el-button>
          </div>
        </div>
      </template>

      <div v-loading="loading" class="edit-content">
        <div
          v-for="(image, index) in editImages"
          :key="index"
          class="image-edit-item"
        >
          <div class="item-row">
            <!-- 图片序号 -->
            <div class="item-number">
              图片{{ index + 1 }}
            </div>

            <!-- URL输入框和操作按钮 -->
            <div class="url-container">
              <el-input
                v-model="image.url"
                :placeholder="`请输入图片 ${index + 1} 的URL`"
                clearable
                size="default"
                class="url-input"
              >
                <template #suffix>
                  <div class="action-buttons">
                    <el-button
                      @click="testImageUrl(image)"
                      :loading="image.testing"
                      type="primary"
                      size="small"
                      text
                      title="测试链接"
                    >
                      <el-icon><Check /></el-icon>
                    </el-button>
                    <el-button
                      @click="openUrlInNewTab(image.url)"
                      :disabled="!image.url"
                      type="success"
                      size="small"
                      text
                      title="访问链接"
                    >
                      <el-icon><Link /></el-icon>
                    </el-button>
                  </div>
                </template>
              </el-input>
            </div>
          </div>

          <div v-if="image.error" class="error-text">
            {{ image.error }}
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh, Check, Link } from '@element-plus/icons-vue'
import axios from 'axios'

const loading = ref(false)
const saving = ref(false)
const imagesFromDB = ref([])
const editImages = ref([])

const API_BASE_URL = '/api'

// 获取收藏图片数据
const fetchFavoriteImages = async () => {
  loading.value = true
  try {
    const response = await axios.get(`${API_BASE_URL}/favorite-images`, {
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    })

    if (response.data && Array.isArray(response.data)) {
      imagesFromDB.value = response.data
      console.log(`FavoriteImagesEditor: 成功获取 ${imagesFromDB.value.length} 张收藏图片`)
      initEditImages()
    }
  } catch (error) {
    console.error('FavoriteImagesEditor: 获取收藏图片数据失败:', error)
    ElMessage.error('获取收藏图片失败')
    imagesFromDB.value = []
    initEditImages()
  } finally {
    loading.value = false
  }
}

// 刷新图片
const refreshImages = async () => {
  await fetchFavoriteImages()
  ElMessage.success('图片数据已刷新')
}

// 初始化编辑数据
const initEditImages = () => {
  editImages.value = []
  // 确保有5个图片位置
  for (let i = 0; i < 5; i++) {
    if (imagesFromDB.value[i]) {
      editImages.value.push({
        id: imagesFromDB.value[i].id,
        url: imagesFromDB.value[i].url,
        error: '',
        testing: false,
        showActions: false
      })
    } else {
      editImages.value.push({
        id: null,
        url: '',
        error: '',
        testing: false,
        showActions: false
      })
    }
  }
}

// 测试图片URL是否有效
const testImageUrl = async (image) => {
  if (!image.url) {
    image.error = '请输入图片URL'
    return
  }

  image.testing = true
  image.error = ''

  try {
    const img = new Image()
    img.onload = () => {
      image.error = ''
      ElMessage.success('图片链接有效')
      image.testing = false
    }
    img.onerror = () => {
      image.error = '图片链接无效或无法加载'
      image.testing = false
    }
    img.src = image.url
  } catch (error) {
    image.error = '测试图片链接时发生错误'
    image.testing = false
  }
}

// 在新标签页打开URL
const openUrlInNewTab = (url) => {
  if (!url) {
    ElMessage.warning('图片URL为空')
    return
  }
  window.open(url, '_blank')
}

// 保存图片
const saveImages = async () => {
  // 验证所有图片URL
  const invalidImages = editImages.value.filter((img, index) =>
    img.url && img.error
  )

  if (invalidImages.length > 0) {
    ElMessage.error('请修复无效的图片链接后再保存')
    return
  }

  saving.value = true
  try {
    const requests = []

    for (let i = 0; i < editImages.value.length; i++) {
      const image = editImages.value[i]

      if (image.id && image.url) {
        // 更新现有图片
        requests.push(
          axios.put(`${API_BASE_URL}/favorite-images/${image.id}`, {
            url: image.url
          })
        )
      } else if (image.id && !image.url) {
        // 删除现有图片（URL为空）
        requests.push(
          axios.delete(`${API_BASE_URL}/favorite-images/${image.id}`)
        )
      } else if (!image.id && image.url) {
        // 创建新图片
        requests.push(
          axios.post(`${API_BASE_URL}/favorite-images`, {
            url: image.url
          })
        )
      }
    }

    if (requests.length > 0) {
      await Promise.all(requests)
    }

    ElMessage.success('图片保存成功')
    await fetchFavoriteImages() // 重新获取数据
  } catch (error) {
    console.error('保存图片失败:', error)
    ElMessage.error('保存图片失败')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  fetchFavoriteImages()
})
</script>

<style scoped>
.favorite-images-editor {
  height: 400px;
  display: flex;
  flex-direction: column;
}

.editor-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  border-radius: 12px;
  border: 1px solid #e1e8ed;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.edit-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
}

.image-edit-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.item-row {
  display: flex;
  align-items: center;
  gap: 12px;
  min-height: 40px;
}

.item-number {
  flex-shrink: 0;
  width: 60px;
  font-weight: 500;
  color: #333;
  font-size: 14px;
}

.url-container {
  flex: 1;
  display: flex;
  align-items: center;
}

.url-input {
  flex: 1;
}

.action-buttons {
  display: flex;
  align-items: center;
  gap: 2px;
  padding-right: 4px;
}

.error-text {
  color: #f56c6c;
  font-size: 12px;
  margin-top: 4px;
  margin-left: 72px;
}

/* 自定义滚动条 */
.edit-content::-webkit-scrollbar {
  width: 4px;
}

.edit-content::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 2px;
}

.edit-content::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 2px;
}

.edit-content::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

:deep(.el-card__body) {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding: 0;
}

:deep(.el-card__header) {
  padding: 12px 16px;
  background: #fafafa;
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-input__suffix) {
  display: flex;
  align-items: center;
}

:deep(.el-input__suffix-inner) {
  display: flex;
  align-items: center;
}
</style>
