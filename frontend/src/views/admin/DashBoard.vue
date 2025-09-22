<!-- filepath: /d:/Nayey/Code/Vue/nyeweb/frontend/src/views/HelloWorld.vue -->
<template>
  <div class="dashboard-layout">
    <AdminSidebar/>
    <div class="main-content" :class="{ 'mobile-main-content': isMobile }">
      <router-view v-if="$route.path !== '/admin/dashboard'"/>
      <div v-else class="dashboard-container">
        <!-- 第一行：时间线编辑器和最喜欢图片编辑器 -->
        <div class="top-row">
          <div class="top-left">
            <TimelineEditor/>
          </div>
          <div class="top-right">
            <FavoriteImagesEditor/>
          </div>
        </div>

        <!-- 第二行：预留给其他组件 -->
        <div class="bottom-row">
          <el-card class="future-content-card" shadow="never">
            <template #header>
              <span>下方内容区域</span>
            </template>
            <div class="future-content">
              <el-empty :image-size="100" description="下方内容待添加"/>
            </div>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import AdminSidebar from '@/components/Admin/AdminSidebar.vue'
import TimelineEditor from '@/components/Admin/DashBoard/TimelineEditor.vue'
import FavoriteImagesEditor from '@/components/Admin/DashBoard/FavoriteImagesEditor.vue'

const isMobile = ref(false)

// 检查是否为移动设备
const checkIsMobile = () => {
  isMobile.value = window.innerWidth <= 768
}

// 组件挂载时检查屏幕尺寸
onMounted(() => {
  checkIsMobile()
  window.addEventListener('resize', checkIsMobile)
})

// 组件卸载前移除事件监听器
onBeforeUnmount(() => {
  window.removeEventListener('resize', checkIsMobile)
})
</script>

<style scoped>
.dashboard-layout {
  display: flex;
  height: 100vh;
}

.main-content {
  flex: 1;
  margin-left: 250px;
  padding: 20px;
  background-color: #fafbfc;
  overflow-y: auto;
}

.dashboard-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: calc(100vh - 40px);
}

.top-row {
  display: flex;
  gap: 20px;
  height: 400px;
}

.top-left {
  width: 50%;
  height: 100%;
}

.top-right {
  width: 50%;
  height: 100%;
}

.bottom-row {
  flex: 1;
  min-height: 300px;
}

.placeholder-card,
.future-content-card {
  height: 100%;
  border-radius: 12px;
  border: 1px solid #e1e8ed;
}

.placeholder-content,
.future-content {
  height: calc(100% - 60px);
  display: flex;
  align-items: center;
  justify-content: center;
}

:deep(.placeholder-card .el-card__body),
:deep(.future-content-card .el-card__body) {
  height: calc(100% - 60px);
}

:deep(.placeholder-card .el-card__header),
:deep(.future-content-card .el-card__header) {
  padding: 16px 20px;
  background: #fafafa;
  border-bottom: 1px solid #ebeef5;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
    padding: 15px;
  }
  
  .main-content.mobile-main-content {
    margin-left: 0; /* 在移动设备上，侧边栏不再显示，所以不需要左边距 */
  }
  
  .dashboard-container {
    gap: 15px;
    height: calc(100vh - 30px);
  }
  
  .top-row {
    flex-direction: column;
    height: auto;
    gap: 15px;
  }
  
  .top-left,
  .top-right {
    width: 100%;
    height: 300px;
  }
  
  .bottom-row {
    min-height: 250px;
  }
  
  /* 在移动设备上为组件添加额外的内边距 */
  .top-left,
  .top-right,
  .bottom-row {
    padding: 0 5px;
  }
}

@media (max-width: 480px) {
  .main-content {
    padding: 10px;
  }
  
  .main-content.mobile-main-content {
    margin-left: 0; /* 在移动设备上，侧边栏不再显示，所以不需要左边距 */
  }
  
  .dashboard-container {
    gap: 10px;
    height: calc(100vh - 20px);
  }
  
  .top-row {
    gap: 10px;
  }
  
  .top-left,
  .top-right {
    height: 250px;
  }
  
  .bottom-row {
    min-height: 200px;
  }
  
  /* 在小屏幕设备上为组件添加额外的内边距 */
  .top-left,
  .top-right,
  .bottom-row {
    padding: 0 3px;
  }
}
</style>
