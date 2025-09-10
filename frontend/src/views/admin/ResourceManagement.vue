<template>
  <div class="management-panel">
    <div class="panel-header">
      <h2>资源管理</h2>
      <p>管理网站提供的下载资源，包括文档、软件、素材等文件资源。</p>
    </div>

    <div class="panel-content">
      <el-card class="content-card">
        <h3>功能列表</h3>
        <ul class="feature-list">
          <li>📁 文件上传管理</li>
          <li>🗂️ 资源分类整理</li>
          <li>🔍 资源搜索功能</li>
          <li>📊 下载统计</li>
          <li>🔐 访问权限管理</li>
          <li>💾 存储空间监控</li>
          <li>🗃️ 资源归档管理</li>
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
// 资源管理逻辑将在此处实现
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

