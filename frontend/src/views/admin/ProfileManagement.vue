<template>
  <div class="management-panel">
    <div class="panel-header">
      <h2>自我信息管理</h2>
      <p>管理个人信息展示内容，包括个人简介、技能展示、联系方式等。</p>
    </div>

    <div class="panel-content">
      <el-card class="content-card">
        <h3>功能列表</h3>
        <ul class="feature-list">
          <li>👤 个人资料编辑</li>
          <li>🖼️ 头像管理</li>
          <li>💼 技能标签管理</li>
          <li>📞 联系方式设置</li>
          <li>🎓 教育经历管理</li>
          <li>💼 工作经历管理</li>
          <li>🏆 成就展示管理</li>
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
// 自我信息管理逻辑将在此处实现
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

