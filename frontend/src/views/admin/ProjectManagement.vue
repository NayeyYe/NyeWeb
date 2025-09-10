<template>
  <div class="management-panel">
    <div class="panel-header">
      <h2>项目管理</h2>
      <p>管理网站展示的项目信息，包括项目介绍、技术栈、演示链接等。</p>
    </div>

    <div class="panel-content">
      <el-card class="content-card">
        <h3>功能列表</h3>
        <ul class="feature-list">
          <li>📝 添加新项目</li>
          <li>✏️ 编辑项目信息</li>
          <li>🗑️ 删除项目</li>
          <li>👁️ 预览项目展示效果</li>
          <li>🔄 项目排序管理</li>
          <li>🏷️ 项目标签管理</li>
        </ul>
        <div class="coming-soon">
          <el-alert
            title="开发中"
            type="info"
            description="该功能正在开发中，敬请期待！"
            :closable="false"
            show-icon>
          </el-alert>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
// 项目管理逻辑将在此处实现
</script>

<style scoped>
.management-panel {
  height: 100%;
}

.panel-header {
  margin-bottom: 20px;
}

.panel-header h2 {
  color: #409eff;
  margin: 0 0 10px 0;
}

.panel-header p {
  color: #666;
  margin: 0;
}

.content-card {
  border-radius: 15px;
  box-shadow: 0 2px 8px #f0f1f2;
}

.feature-list {
  list-style: none;
  padding: 0;
}

.feature-list li {
  padding: 10px 0;
  font-size: 16px;
  color: #333;
}

.coming-soon {
  margin-top: 30px;
}
</style>

