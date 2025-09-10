<template>
  <div class="management-panel">
    <div class="panel-header">
      <h2>文章管理</h2>
      <p>管理知识分享文章，包括技术文档、学习笔记、经验分享等内容。</p>
    </div>

    <div class="panel-content">
      <el-card class="content-card">
        <h3>功能列表</h3>
        <ul class="feature-list">
          <li>📄 创建新文章</li>
          <li>✏️ 编辑文章内容</li>
          <li>🗂️ 文章分类管理</li>
          <li>🏷️ 标签管理</li>
          <li>👁️ 文章预览</li>
          <li>📊 阅读统计</li>
          <li>💬 评论管理</li>
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
// 文章管理逻辑将在此处实现
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

