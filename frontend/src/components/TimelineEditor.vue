<template>
  <el-card class="timeline-card">
    <template #header>
      <div class="card-header">
        <span>我的历程</span>
        <el-button class="button" type="primary" plain @click="dialogVisible = true">
          添加新条目
        </el-button>
      </div>
    </template>

    <el-dialog v-model="dialogVisible" title="添加新条目" width="500">
      <el-form :model="newItem" label-width="80px">
        <el-form-item label="日期">
          <el-date-picker
            v-model="newItem.timestamp"
            type="date"
            placeholder="选择日期"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="内容">
          <el-input v-model="newItem.content" type="textarea" placeholder="请输入内容" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="addItem"> 确认 </el-button>
        </span>
      </template>
    </el-dialog>

    <el-timeline>
      <el-timeline-item
        v-for="(item, index) in sortedTimelineItems"
        :key="index"
        :timestamp="item.timestamp"
        placement="top"
      >
        <el-tooltip
          :disabled="item.content.length <= 50"
          effect="dark"
          :content="item.content"
          placement="top"
        >
          <p class="timeline-content">
            {{ item.content.length > 30 ? item.content.slice(0, 30) + '...' : item.content }}
          </p>
        </el-tooltip>
      </el-timeline-item>
    </el-timeline>
  </el-card>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import timelineData from '@/data/timeline.json'

// 对话框可见性
const dialogVisible = ref(false)

// 新条目的数据模型
const newItem = ref({
  timestamp: '',
  content: ''
})

// 时间线数据
// todo: 这里应该加入数据库内容
const timelineItems = ref(timelineData)

// 计算属性，用于对时间线项目按日期降序排序
const sortedTimelineItems = computed(() => {
  return [...timelineItems.value].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
})

// 添加新条目
const addItem = () => {
  if (!newItem.value.timestamp || !newItem.value.content) {
    ElMessage.error('日期和内容不能为空！')
    return
  }
  timelineItems.value.push({ ...newItem.value })
  // 清空输入框
  newItem.value.timestamp = ''
  newItem.value.content = ''
  ElMessage.success('添加成功！')
  dialogVisible.value = false // 关闭对话框
}
</script>

<style scoped>
.timeline-card {
  width: 350px;
  box-sizing: border-box; /* 确保宽度包含内边距和边框 */
  border-radius: 15px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.timeline-content {
  margin: 0;
  color: #606266;
}
</style>
