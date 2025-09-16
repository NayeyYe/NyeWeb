<!-- filepath: /d:/Nayey/Code/Vue/nyeweb/frontend/src/views/HelloWorld.vue -->
<template>
  <div class="dashboard-layout">
    <AdminSidebar />
    <div class="main-content">
      <router-view v-if="$route.path !== '/admin/dashboard'" />
      <div v-else class="dashboard-container">
        <!-- 第一行：时间线编辑器和右侧占位卡片 -->
        <div class="top-row">
          <div class="top-left">
            <TimelineEditor />
          </div>
          <div class="top-right">
            <el-card class="placeholder-card" shadow="never">
              <template #header>
                <span>右侧内容区域</span>
              </template>
              <div class="placeholder-content">
                <el-empty description="右侧内容待添加" :image-size="80" />
              </div>
            </el-card>
          </div>
        </div>

        <!-- 第二行：预留给其他组件 -->
        <div class="bottom-row">
          <el-card class="future-content-card" shadow="never">
            <template #header>
              <span>下方内容区域</span>
            </template>
            <div class="future-content">
              <el-empty description="下方内容待添加" :image-size="100" />
            </div>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import AdminSidebar from '@/components/Admin/AdminSidebar.vue'
import TimelineEditor from '@/components/Admin/DashBoard/TimelineEditor.vue'
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
</style>